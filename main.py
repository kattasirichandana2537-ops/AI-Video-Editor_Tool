import streamlit as st
import whisper
from groq import Groq
from moviepy import VideoFileClip 
import os

# 1. SETUP & HELPER FUNCTIONS

#  API KEY IS PRE-LOADED HERE
GROQ_API_KEY = "PASTE_GROQ_API_KEY"
client = Groq(api_key=GROQ_API_KEY)

SUPER_PROMPT = """
You are a master social media editor. Analyze this transcript and find 7 standalone viral moments.
RULES:
1. Start exactly at the beginning of a sentence.
2. End immediately after a period/punctuation.
3. Length: 30-60 seconds.
4. IMPORTANT: Return timestamps in TOTAL SECONDS (e.g. use 90, NOT 1:30).
5. Format: start,end|start,end|start,end

TRANSCRIPT: {transcript}
"""

def parse_time(time_str):
    try:
        time_str = str(time_str).strip()
        time_str = time_str.lower().replace("s", "").replace("sec", "")
        
        if ":" in time_str:
            parts = time_str.split(":")
            if len(parts) == 2:
                return float(parts[0]) * 60 + float(parts[1])
            elif len(parts) == 3:
                return float(parts[0]) * 3600 + float(parts[1]) * 60 + float(parts[2])
        return float(time_str)
    except:
        return 0.0

# 2. UI & MEMORY MANAGEMENT

st.set_page_config(page_title="Simple Snippet Tool", layout="wide")
st.title("⚡ Simple Snippet Tool (No Crop)")

if 'clips_data' not in st.session_state:
    st.session_state['clips_data'] = []
if 'video_processed' not in st.session_state:
    st.session_state['video_processed'] = False

with st.sidebar:
    st.header("Settings")
    user_focus = st.text_input("Topic Focus", placeholder="e.g. funny moments")
    st.info("💡 Vertical Crop has been removed for stability.")

uploaded_file = st.file_uploader("Upload Video", type=["mp4"])

if uploaded_file:
    # Save file locally
    with open("temp_video.mp4", "wb") as f:
        f.write(uploaded_file.getbuffer())

    if st.button("🚀 Analyze & Find Clips"):
        status = st.empty()
        try:
            status.info("👂 Transcribing...")
            model = whisper.load_model("base")
            result = model.transcribe("temp_video.mp4", fp16=False)
            
            status.info("🧠 Analyzing...")
            prompt = SUPER_PROMPT.format(transcript=result['text'])
            if user_focus:
                prompt += f"\nFocus on: {user_focus}"
                
            completion = client.chat.completions.create(
                messages=[{"role": "user", "content": prompt}],
                model="llama-3.3-70b-versatile",
            )
            
            # - PARSING LOGIC -
            raw_data = completion.choices[0].message.content.strip()
            parsed_clips = []
            
            chunks = raw_data.split('|')
            for item in chunks:
                item = item.strip()
                parts = item.split(',')
                
                # Safety Check: Do we have at least 2 numbers?
                if len(parts) >= 2:
                    s_str = parts[0].strip()
                    e_str = parts[1].strip()
                    
                    s_val = parse_time(s_str)
                    e_val = parse_time(e_str)
                    
                    if s_val < e_val:
                        parsed_clips.append({'start': s_val, 'end': e_val})
            
            st.session_state['clips_data'] = parsed_clips
            st.session_state['video_processed'] = True
            
            if len(parsed_clips) > 0:
                status.success(f"Found {len(parsed_clips)} clips! Scroll down to edit.")
            else:
                status.error("AI couldn't find valid timestamps. Try again.")
            
        except Exception as e:
            st.error(f"Error: {e}")

# 3. THE RENDER LOOP
if st.session_state['video_processed'] and st.session_state['clips_data']:
    st.divider()
    cols = st.columns(len(st.session_state['clips_data']))
    
    for i, clip_info in enumerate(st.session_state['clips_data']):
        with cols[i]:
            st.subheader(f"Snippet {i+1}")
            
            adj_start = st.number_input(f"Start Time (Sec)", value=clip_info['start'], step=0.5, key=f"s_{i}")
            adj_end = st.number_input(f"End Time (Sec)", value=clip_info['end'], step=0.5, key=f"e_{i}")
            
            process_btn = st.button(f"✂️ Render Clip {i+1}", key=f"btn_{i}")
            
            if process_btn:
                output_name = f"snippet_{i+1}.mp4"
                try:
                    with VideoFileClip("temp_video.mp4") as video:
                        # 1. Cut Video
                        new_clip = video.subclipped(max(0, adj_start), adj_end)
                        g
                        
                        new_clip.write_videofile(output_name, codec="libx264", audio_codec="aac", logger=None)
                    
                    # 2. Display Video
                    with open(output_name, "rb") as v_file:
                        st.video(v_file.read())
                    
                    with open(output_name, "rb") as d_file:
                        st.download_button("Download", d_file, file_name=output_name, key=f"dl_{i}")
                        
                except Exception as e:
                    st.error(f"Render Error: {e}")