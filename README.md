import os
import asyncio
import edge_tts
from moviepy.editor import ColorClip, AudioFileClip
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

YT_CLIENT_ID = os.environ.get("YT_CLIENT_ID")
YT_CLIENT_SECRET = os.environ.get("YT_CLIENT_SECRET")
YT_REFRESH_TOKEN = os.environ.get("REFRESH_TOKEN") or os.environ.get("YT_REFRESH_TOKEN")

TEXT = "Success starts with discipline and daily action. Keep building your future every single day."
TITLE = "Daily Motivation #Shorts"
DESCRIPTION = "Automated Short #Shorts #Motivation"

async def generate_audio():
    communicate = edge_tts.Communicate(TEXT, "en-US-ChristopherNeural")
    await communicate.save("voice.mp3")

def create_short():
    audio = AudioFileClip("voice.mp3")
    video = ColorClip(size=(1080, 1920), color=(15, 15, 25), duration=audio.duration)
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
    create_short()
    upload_to_youtube()
