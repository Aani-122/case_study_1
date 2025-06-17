# Video Analysis and Summarization System

## Overview
This system analyzes videos by combining visual and audio information to generate comprehensive summaries using AI models.

## Prerequisites

### 1. Get Your Gemini API Key
To use this application, you need a Gemini API key from Google AI Studio:

1. Visit [Google AI Studio](https://ai.google.dev/gemini-api/docs/api-key) to get your API key
2. Set up your API key as an environment variable:(if you wnat to run notebook[experiments])
   - **Windows**: Search for "Environment Variables" in system settings and add `GEMINI_API_KEY=your_key_here`
3.paste your api key as it is in the sidebar in app.
   

## Installation

### 1. Install Base Requirements
```bash
pip install -r requirements.txt
```

### 2. Install Streamlit Requirements
```bash
pip install -r requirements_streamlit.txt
```

## Running the Application

Start the Streamlit application:
```bash
streamlit run streamlit_video_summary.py
```

## Features

### 1. Local Video Summary
- Upload and analyze local video files
- Generate comprehensive summaries using AI models

### 2. YouTube Video Summary
- Provide YouTube video URL
- Extract transcript from YouTube video
- Generate summary based on the video transcript
