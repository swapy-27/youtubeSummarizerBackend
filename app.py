# YouTube Video Summarizer using Groq API (Free)
# Requires: pytube, openai (for Groq), flask

import os
from flask import Flask, request, jsonify
from groq import Groq
from flask_cors import CORS
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.formatters import TextFormatter
from urllib.parse import urlparse, parse_qs
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# --- Configurations ---
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
client = None
MODEL = "llama-3.3-70b-versatile"

# Initialize Groq client only if API key is available
if GROQ_API_KEY:
    try:
        client = Groq(api_key=GROQ_API_KEY)
    except Exception as e:
        print(f"Failed to initialize Groq client: {e}")
        client = None
else:
    print("Warning: GROQ_API_KEY not set. Summarization will not work.")

app = Flask(__name__)
CORS(app)


def extract_video_id(url):
    try:
        parsed = urlparse(url)
        if 'youtube' in parsed.netloc:
            return parse_qs(parsed.query).get('v', [None])[0]
        elif 'youtu.be' in parsed.netloc:
            return parsed.path.lstrip('/')
    except Exception as e:
        print("Video ID extraction error:", e)
        return None

def get_video_transcript(url):
    try:
        video_id = extract_video_id(url)
        print("Video ID:", video_id)
        if not video_id:
            print("Invalid YouTube URL")
            return ""

        # Get transcript
        transcript_list = YouTubeTranscriptApi().list(video_id)

        transcript = None
        try:
            transcript = transcript_list.find_transcript(['en', 'en-GB'])
        except:
            transcript = transcript_list.find_transcript(['a.en'])  # auto-generated

        transcript_data = transcript.fetch()
        formatter = TextFormatter()
        return formatter.format_transcript(transcript_data)

    except Exception as e:
        print("Transcript error:", e)
        return ""

# --- Helper: Summarize using Groq ---
def summarize_text(text):
    try:
        response = client.chat.completions.create(
            model=MODEL,
            messages=[
                {"role": "system", "content": "You are a helpful assistant that summarizes YouTube transcripts."},
                {"role": "user", "content": f"Summarize this video transcript:\n\n{text}"}
            ],
            temperature=0.3,
            max_tokens=1024
        )
        return response.choices[0].message.content
    except Exception as e:
        print("Groq summarization error:", e)
        return "Summary failed"

# --- API Endpoints ---
@app.route('/', methods=['GET'])
def health_check():
    return jsonify({
        "status": "healthy",
        "message": "YouTube Video Summarizer API",
        "api_key_configured": bool(GROQ_API_KEY)
    })

@app.route('/summarize', methods=['POST'])
def summarize():
    # Check if Groq client is available
    if not client:
        return jsonify({"error": "Groq API not configured. Please set GROQ_API_KEY environment variable."}), 500
    
    data = request.get_json()
    url = data.get("url")
    if not url:
        return jsonify({"error": "URL missing"}), 400
    print("Getting transcript for URL:", url)
    transcript = get_video_transcript(url)
    print("Transcript:", transcript)
    if not transcript:
        return jsonify({"error": "Transcript not found"}), 404

    summary = summarize_text(transcript[:5000])  # Avoid token overflow
    return jsonify({"summary": summary})

# --- Run locally ---
if __name__ == '__main__':
    app.run(debug=True, port=5000) 