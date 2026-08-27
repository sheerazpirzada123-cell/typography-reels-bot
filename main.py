import os
import random
import requests
from moviepy.editor import TextClip, AudioFileClip, VideoFileClip, CompositeVideoClip
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

# ElevenLabs Realistic Voice Function
def generate_elevenlabs_audio(text, output_filename="voiceover.mp3"):
    api_key = os.environ.get("ELEVENLABS_API_KEY")
    voice_id = "pNInz6obpgDQGcFmaJgB" # Deep Male Voice "Adam"
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"

    headers = {
        "Accept": "audio/mpeg",
        "Content-Type": "application/json",
        "xi-api-key": api_key
    }

    data = {
        "text": text,
        "model_id": "eleven_multilingual_v2",
        "voice_settings": {
            "stability": 0.4,
            "similarity_boost": 0.85
        }
    }

    response = requests.post(url, json=data, headers=headers)
    if response.status_code == 200:
        with open(output_filename, "wb") as f:
            f.write(response.content)
        return output_filename
    else:
        raise Exception(f"ElevenLabs API Error: {response.text}")

def download_background_video():
    video_urls = [
        "https://assets.mixkit.co/videos/preview/mixkit-starry-night-sky-4128-large.mp4",
        "https://assets.mixkit.co/videos/preview/mixkit-deep-space-with-stars-and-nebula-41544-large.mp4",
        "https://assets.mixkit.co/videos/preview/mixkit-time-lapse-of-clouds-over-a-mountain-range-4286-large.mp4"
    ]
    url = random.choice(video_urls)
    r = requests.get(url)
    with open("bg.mp4", "wb") as f:
        f.write(r.content)
    return "bg.mp4"

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
            "tags": ["Shorts", "Facts", "Mysterious", "Hinglish"],
            "categoryId": "27"
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
    # Short & High-Impact Scripts (~250 Characters for 20-25 sec videos)
    scripts = [
        "Kya aapko pata hai ki hum raat ko jo taare dekhte hain, wo shayad kab ke khatam ho chuke hain? Unki roshni ko zameen tak pahunchne mein lakho saal lagte hain. Aap aasmaan mein past dekh rahe hote hain. Think about it.",
        "Psychology kehti hai ki agar aap kisi ke baare mein bina waja soch rahe hain, toh 80 percent chance hai ki wo insan bhi aapke baare mein soch raha hai. Humara mind connected hota hai.",
        "Zindagi ki sabse badi theory: Hum duniya ko waise nahi dekhte jaisi wo hai, balki waise dekhte hain jaise hum khud hain. Mindset badlo, duniya badal jayegi."
    ]
    
    script_text = random.choice(scripts)
    print(f"Selected Script Length: {len(script_text)} characters")

    # Generate Realistic Voice
    audio_path = generate_elevenlabs_audio(script_text)
    audio_clip = AudioFileClip(audio_path)
    duration = audio_clip.duration

    # Download & Adjust BG Video
    bg_video_path = download_background_video()
    bg_clip = VideoFileClip(bg_video_path)
    
    if bg_clip.duration < duration:
        bg_clip = bg_clip.loop(duration=duration)
    else:
        bg_clip = bg_clip.subclip(0, duration)
        
    bg_clip = bg_clip.resize(newsize=(1080, 1920))

    # Styled Text Overlay
    txt_clip = TextClip(
        script_text, 
        fontsize=52, 
        color='#FFD700', 
        font='DejaVu-Sans-Bold', 
        stroke_color='black',
        stroke_width=3,
        size=(920, 1500), 
        method='caption', 
        align='center'
    ).set_duration(duration).set_position('center')

    # Merge Video + Audio
    final_video = CompositeVideoClip([bg_clip, txt_clip])
    final_video = final_video.set_audio(audio_clip)

    output_video = "final_reel.mp4"
    final_video.write_videofile(output_video, fps=24, codec='libx264', audio_codec='aac')

    # Upload
    upload_to_youtube(
        video_path=output_video,
        title=f"{script_text[:45]}... #Shorts #Mysterious",
        description=f"{script_text}\n\n#Shorts #Mindset #Hinglish\n\nVoice by ElevenLabs"
    )

if __name__ == "__main__":
    generate_typography_video()
