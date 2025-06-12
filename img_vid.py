from dotenv import load_dotenv
import os
import google.generativeai as genai
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.schema import HumanMessage

load_dotenv()

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def process_image_direct_api(image_path, prompt="Caption this image."):
    """Process image using direct Google Generative AI API"""
    try:
        # Read the image file
        with open(image_path, 'rb') as f:
            image_bytes = f.read()
        
        # Create the model
        model = genai.GenerativeModel('gemini-pro-vision')
        
        # Generate content
        response = model.generate_content([image_bytes, prompt])
        return response.text
    except Exception as e:
        return f"Error processing image: {str(e)}"


if __name__ == "__main__":
    image_path = "C:\projects\case_study_1\image.png"  
    
    print("Using direct API:")
    result_direct = process_image_direct_api(image_path)
    print(result_direct)
    
