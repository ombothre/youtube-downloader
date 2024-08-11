# YouTube Downloader

A simple FastAPI application to download YouTube videos or audio as MP3 files using `yt-dlp`.

## Features

- Download audio (MP3) or video (MP4)
- User-friendly interface with Bootstrap
- Loading spinner during file processing
- Error handling for invalid URLs

## Requirements

- Python 3.7+
- FastAPI
- Uvicorn
- yt-dlp
- FFmpeg

## Installation

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd <repository-directory>
Install dependencies:

bash
Copy code
pip install fastapi uvicorn yt-dlp
Install FFmpeg:
Download and install FFmpeg from FFmpeg's website.

Usage
Run the application:

bash
Copy code
uvicorn main:app --reload
Access the app:
Open your browser and go to http://127.0.0.1:8000.

Directory Structure
graphql
Copy code
/YouTube-Downloader
│
├── main.py              # FastAPI application
├── templates            # Folder for HTML templates
│   ├── index.html       # Main page for the downloader
│   └── error.html       # Error page for invalid URLs
└── downloads            # Folder for downloaded files
License
This project is open-source under the MIT License.

javascript
Copy code

Feel free to replace `<repository-url>` and `<repository-directory>` with your actual reposit