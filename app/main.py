from fastapi import FastAPI, HTTPException
from fastapi.responses import StreamingResponse
import yt_dlp
import tempfile
import os

app = FastAPI()

@app.get("/download")
async def download_video(url: str):
    try:
        # Use yt-dlp to extract the audio
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
            'outtmpl': os.path.join(tempfile.gettempdir(), '%(title)s.%(ext)s'),  # Save to a temporary file
        }

        # Use a temporary file to store the downloaded audio
        with tempfile.NamedTemporaryFile(delete=True, suffix=".mp3") as temp_file:
            ydl_opts['outtmpl'] = temp_file.name  # Use the temp file for output

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])  # Download the audio to the temp file

            # Seek to the beginning of the file for streaming
            temp_file.seek(0)

            # Create a StreamingResponse and set the filename for download
            response = StreamingResponse(temp_file, media_type="audio/mpeg")
            response.headers["Content-Disposition"] = f"attachment; filename={os.path.basename(temp_file.name)}"
            return response

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
