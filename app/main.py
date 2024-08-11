from fastapi import FastAPI, Form, HTTPException
from fastapi.responses import HTMLResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles
import yt_dlp
import tempfile
import os

app = FastAPI()

# Serve static files for the HTML page
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/", response_class=HTMLResponse)
async def read_root():
    return HTMLResponse(content=open("static/index.html").read())

@app.post("/download")
async def download(url: str = Form(...), file_type: str = Form(...)):
    try:
        # Set the output format based on the selected file type
        if file_type == 'audio':
            suffix = ".mp3"
            ydl_opts = {
                'format': 'bestaudio/best',
                'extractaudio': True,
                'audioformat': 'mp3',
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                }],
                'quiet': True,
                'outtmpl': os.path.join(tempfile.gettempdir(), '%(title)s' + suffix),  # Save to a temp file
            }
        else:
            suffix = ".mp4"
            ydl_opts = {
                'format': 'bestvideo+bestaudio/best',
                'outtmpl': os.path.join(tempfile.gettempdir(), '%(title)s' + suffix),  # Save to a temp file
            }

        # Download the file using yt-dlp
        with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as temp_file:
            ydl_opts['outtmpl'] = temp_file.name  # Use the temp file for output

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])  # Download the audio/video to the temp file

            temp_file.seek(0)  # Seek to the start of the file for reading

        # Return the file for download
        media_type = "audio/mpeg" if file_type == "audio" else "video/mp4"
        return StreamingResponse(temp_file, media_type=media_type, headers={"Content-Disposition": f"attachment; filename={os.path.basename(temp_file.name)}"})

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
