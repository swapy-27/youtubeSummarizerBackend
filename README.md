# YouTube Video Summarizer

A Flask-based web application that summarizes YouTube videos using the Groq API and YouTube transcript API.

## Features

- Extract transcripts from YouTube videos
- Generate AI-powered summaries using Groq's Llama model
- RESTful API endpoint for video summarization
- CORS enabled for frontend integration

## API Usage

Send a POST request to `/summarize` with a JSON body containing the YouTube URL:

```json
{
  "url": "https://www.youtube.com/watch?v=VIDEO_ID"
}
```

## Requirements

- Python 3.11+
- Flask
- Groq API key
- YouTube transcript API

## Local Development

1. Install dependencies: `pip install -r requirements-dev.txt`
2. Set your Groq API key in environment variable: `GROQ_API_KEY`
3. Run: `python app.py`
4. Server starts at `http://localhost:5000`

## Production Deployment

For Railway deployment, use the lightweight `requirements.txt` which excludes heavy packages like `torch` and `openai-whisper` that are not needed for the core YouTube summarization functionality.

## Railway Deployment

1. Set `GROQ_API_KEY` environment variable in Railway dashboard
2. Deploy using the provided configuration files
