import streamlit as st
import time
import google.generativeai as genai
from IPython.display import Markdown
import os
from IPython.display import Video
from youtube_transcript_api import YouTubeTranscriptApi


def get_video_id(url_link):
  return url_link.split("watch?v=")[-1]

def video_summary_local(video_path):
    genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

    model = genai.GenerativeModel("gemini-2.0-flash-001")

    uploaded_video = genai.upload_file(path=video_path, mime_type="video/mp4")

    while uploaded_video.state.name != "ACTIVE":
        print(f"Waiting for file to be ACTIVE. Current state: {uploaded_video.state.name}")
        time.sleep(2)
        uploaded_video = genai.get_file(uploaded_video.name)

    prompt = """
    give me a summary of the given video, don't include any other text.
    """

    response = model.generate_content([prompt, uploaded_video])
    return response.text

def video_summary_yt(video_url):
    genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

    model = genai.GenerativeModel("gemini-2.0-flash-001")
    video_id = get_video_id(video_url)  
    transcript = YouTubeTranscriptApi.get_transcript(video_id)

    text = " ".join([entry['text'] for entry in transcript])
    #print(text)

    response = model.generate_content(f"Summarize this video transcript:\n\n{text}")
    return response.text

def main():
    st.title(" Video Summary Generator")
    st.write("Upload a video, provide a video path, or enter a YouTube link to get an AI-generated summary")
    
    with st.sidebar:
        st.header(" API Configuration")
        api_key = st.text_input("Enter your Google API Key", type="password")
        if api_key:
            os.environ["GOOGLE_API_KEY"] = api_key
            st.success("API Key set successfully!")
        else:
            st.warning("Please enter your Google API Key to continue")
    
    st.header(" Video Input")
    
    input_method = st.radio(
        "Choose input method:",
        ["Upload Video File", "Enter Video Path", "YouTube Link"]
    )
    
    if input_method == "Upload Video File":
        uploaded_file = st.file_uploader(
            "Choose a video file",
            type=['mp4'],
            help="Supported formats: MP4"
        )
        
        if uploaded_file is not None:
            temp_path = f"temp_{uploaded_file.name}"
            with open(temp_path, "wb") as f:
                f.write(uploaded_file.getbuffer())
            
            video_path = temp_path
            st.success(f"File uploaded: {uploaded_file.name}")
            
    elif input_method == "Enter Video Path":
        video_path = st.text_input(
            "Enter the full path to your video file",
            placeholder="C:\\path\\to\\your\\video.mp4",
            help="Enter the complete file path including drive letter and file extension"
        )
    
    else:  
        youtube_url = st.text_input(
            "Enter YouTube video URL",
            placeholder="https://www.youtube.com/watch?v=VIDEO_ID",
            help="Enter the complete YouTube video URL"
        )
        
        if youtube_url:
            try:
                if "watch?v=" in youtube_url:
                    video_id = get_video_id(youtube_url)
                    st.success(f"YouTube video ID: {video_id}")
                    
                    try:
                        transcript = YouTubeTranscriptApi.get_transcript(video_id)
                        st.info(f" Transcript available ({len(transcript)} segments)")
                    except Exception as e:
                        st.warning(f" Could not fetch transcript: {str(e)}")
                else:
                    st.error("Please enter a valid YouTube URL with 'watch?v='")
            except Exception as e:
                st.error(f"Invalid YouTube URL: {str(e)}")
    
    if st.button(" Generate Summary", type="primary"):
        if not api_key:
            st.error("Please enter your Google API Key in the sidebar first!")
        elif input_method == "YouTube Link":
            if 'youtube_url' not in locals() or not youtube_url:
                st.error("Please provide a YouTube URL first!")
            else:
                try:
                    with st.spinner(" Processing YouTube video transcript... This may take a few minutes"):
                        summary = video_summary_yt(youtube_url)
                    
                    st.header("Video Summary")
                    st.write(summary)
                    
                except Exception as e:
                    st.error(f" Getting fllowing erro: {str(e)}")
        else:
            if 'video_path' not in locals() or not video_path:
                st.error("Please provide a video file or path first!")
            else:
                try:
                    with st.spinner(" Processing video... This may take a few minutes"):
                        summary = video_summary_local(video_path)
                    
                    st.header(" Video Summary")
                    st.write(summary)

                    
                except Exception as e:
                    st.error(f" Getting this erro: {str(e)}")
    #remove any tem file if there id any
    if 'temp_path' in locals():
        try:
            os.remove(temp_path)
        except:
            pass

if __name__ == "__main__":
    main() 