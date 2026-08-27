import os
import random
from gtts import gTTS
from moviepy.editor import TextClip, AudioFileClip
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

def upload_to_youtube(video_path, title, description):
    client_id = os.environ.get("YOUTUBE_CLIENT_ID")
    client_secret = os.environ.get("YOUTUBE_CLIENT_SECRET")
    refresh_token = os.environ.get("YOUTUBE_REFRESH_TOKEN")

    creds = Credentials(
        None,
        refresh_token=refresh_token,
        token_uri="https://oauth2.googleapis.com/token",
        client_id=client_id,
        client_secret=client_secret,
        scopes=["https://www.googleapis.com/auth/youtube.upload"]
    )

    youtube = build("youtube", "v3", credentials=creds)

    body = {
        "snippet": {
            "title": title,
            "description": description,
            "tags": ["Shorts", "Motivation", "Quotes", "Typography"],
            "categoryId": "22"
        },
        "status": {
            "privacyStatus": "public",
            "selfDeclaredMadeForKids": False
        }
    }

    media = MediaFileUpload(video_path, chunksize=-1, resumable=True)
    request = youtube.videos().insert(part="snippet,status", body=body, media_body=media)
    response = request.execute()
    print(f"Video uploaded successfully! Video ID: {response['id']}")

def generate_typography_video():
    quotes = [
        "Success is not final, failure is not fatal.",
        "Do something today that your future self will thank you for.",
        "Hard times build strong people.",
        "Your only limit is your mind."
    ]
    text = random.choice(quotes)
    print(f"Selected Quote: {text}")

    tts = gTTS(text=text, lang='en', slow=False)
    audio_path = "voiceover.mp3"
    tts.save(audio_path)

    audio_clip = AudioFileClip(audio_path)
    duration = audio_clip.duration

    txt_clip = TextClip(text, fontsize=70, color='white', font='Arial-Bold', 
                        size=(1080, 1920), method='caption', align='center')
    txt_clip = txt_clip.set_duration(duration)

    video = txt_clip.set_audio(audio_clip)
    output_video = "final_reel.mp4"
    video.write_videofile(output_video, fps=24, codec='libx264', audio_codec='aac')

    upload_to_youtube(
        video_path=output_video,
        title=f"{text[:50]} #Shorts #Motivation",
        description=f"{text}\n\n#Shorts #Typography #Motivation"
    )

if __name__ == "__main__":
    generate_typography_video()
