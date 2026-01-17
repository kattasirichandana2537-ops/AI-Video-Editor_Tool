  
  
   #  AI  Smart Video Editor

Project Track: Generative AI & Media Tools
Status: Completed

##  Project Overview
This tool utilizes Artificial Intelligence to automate the video editing process. By combining **OpenAI Whisper** (for transcription) and **Llama 3 via Groq** (for semantic understanding), the system "watches" long-form video content and automatically extracts standalone, viral-worthy 30-60 second clips.

The goal is to reduce the time content creators spend scrubbing through footage by 90%.

---

##  Repository Structure
**Note for Evaluators:** The primary evaluation artifact is the Jupyter Notebook.

- **`Project_Report.ipynb`**   
  *The Main Submission.* Contains the full problem definition, system architecture, logic explanation, and evaluation metrics required for grading.
  
- **`main.py`**   
  *The Functional Application.* A Streamlit web app that allows users to upload videos and interact with the AI pipeline in real-time.

- **`requirements.txt`**   
  List of all Python dependencies required to run the project.

---

#  Tech Stack
- "Frontend:" Streamlit
- "ASR (Speech-to-Text):" OpenAI Whisper (Base Model)
- "LLM (Logic):" Llama-3-70b-versatile (via Groq API)
- "Video Processing:" MoviePy

---

# How to Run the Application

 to test the live application (main.py), follow these steps:

# 1. Installation
Ensure you have Python installed. It is recommended to use a virtual environment.

pip install -r requirements.txt

2. API Key Setup
Open main.py and replace the placeholder API key with your valid Groq API key:

GROQ_API_KEY = "groq_api_key_here"

3. Run the following command in terminal:

streamlit run main.py

FFmpeg: This project requires FFmpeg to be installed on the system for moviepy and whisper to function correctly.

Processing Power: Transcription (Whisper) runs locally. Performance depends on your CPU/GPU.