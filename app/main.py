from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
import yt_dlp
import os

app = FastAPI()

# Serve static files for the HTML page
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/", response_class=HTMLResponse)
async def read_root():
    return HTMLResponse(content=open("static/index.html").read())

@app.post("/download")
async def download(url: str = Form(...), file_type: str = Form(...)):
    output_path = "downloads"
    os.makedirs(output_path, exist_ok=True)

    ydl_opts = {
        'outtmpl': f'{output_path}/%(title)s.%(ext)s',
    }

    if file_type == 'audio':
        ydl_opts['format'] = 'bestaudio/best'
        ydl_opts['postprocessors'] = [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }]
    else:
        ydl_opts['format'] = 'bestvideo+bestaudio/best'
        ydl_opts['postprocessors'] = [{
            'key': 'FFmpegVideoConvertor',
            'preferedformat': 'mp4',
        }]

    # Download the file
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

    # Get the downloaded file path
    downloaded_file = max([os.path.join(output_path, f) for f in os.listdir(output_path)], key=os.path.getctime)

    return {"message": "Download complete", "path": f"/download/{os.path.basename(downloaded_file)}"}

@app.get("/download/{file_name}")
async def serve_file(file_name: str):
    file_path = os.path.join("downloads", file_name)
    return FileResponse(file_path)