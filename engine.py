import os
import asyncio
import requests
import edge_tts
from moviepy.editor import VideoFileClip, AudioFileClip
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

PEXELS_API_KEY = os.environ.get("PEXELS_API_KEY")
YT_CLIENT_ID = os.environ.get("YT_CLIENT_ID")
YT_CLIENT_SECRET = os.environ.get("YT_CLIENT_SECRET")
YT_REFRESH_TOKEN = os.environ.get("YT_REFRESH_TOKEN")

TEXT = "Success starts with discipline and daily action. Keep building your future every single day."
TITLE = "Daily Motivation #Shorts"
DESCRIPTION = "Automated Short #Shorts #Motivation"

async def generate_audio():
    communicate = edge_tts.Communicate(TEXT, "en-US-ChristopherNeural")
    await communicate.save("voice.mp3")

def download_video():
    headers = {"Authorization": PEXELS_API_KEY}
    url = "https://api.pexels.com/videos/search?query=luxury+motivation&orientation=portrait&per_page=1"
    res = requests.get(url, headers=headers).json()
    video_url = res["videos"][0]["video_files"][0]["link"]
    with open("bg.mp4", "wb") as f:
        f.write(requests.get(video_url).content)

def create_short():
    audio = AudioFileClip("voice.mp3")
    video = VideoFileClip("bg.mp4").subclip(0, audio.duration)
    final = video.set_audio(audio)
    final.write_videofile("final_short.mp4", fps=24, codec="libx264", audio_codec="aac")

def upload_to_youtube():
    creds = Credentials(
        token=None,
        refresh_token=YT_REFRESH_TOKEN,
        token_uri="https://oauth2.googleapis.com/token",
        client_id=YT_CLIENT_ID,
        client_secret=YT_CLIENT_SECRET
    )
    youtube = build("youtube", "v3", credentials=creds)
    body = {
        "snippet": {
            "title": TITLE,
            "description": DESCRIPTION,
            "categoryId": "22"
        },
        "status": {"privacyStatus": "public"}
    }
    media = MediaFileUpload("final_short.mp4", chunksize=-1, resumable=True)
    request = youtube.videos().insert(part="snippet,status", body=body, media_body=media)
    response = request.execute()
    print("Uploaded Video ID:", response["id"])

if __name__ == "__main__":
    asyncio.run(generate_audio())
    download_video()
    create_short()
    upload_to_youtube()
