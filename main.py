import os
import random
from gtts import gTTS
from moviepy.editor import TextClip, AudioFileClip, CompositeVideoClip

def generate_typography_video():
    # 1. Random Motivational Quotes (Pakistan aur Global youth mein bohot chalte hain)
    quotes = [
        "Success is not final, failure is not fatal.",
        "Do something today that your future self will thank you for.",
        "Hard times build strong people.",
        "Your only limit is your mind."
    ]
    text = random.choice(quotes)
    print(f"Selected Quote: {text}")

    # 2. Generate Voiceover (Audio)
    tts = gTTS(text=text, lang='en', slow=False)
    audio_path = "voiceover.mp3"
    tts.save(audio_path)

    # 3. Create Typography Video (Reels/Shorts Size: 1080x1920)
    audio_clip = AudioFileClip(audio_path)
    duration = audio_clip.duration

    # Stylish text overlay for Reels/TikTok
    txt_clip = TextClip(text, fontsize=70, color='white', font='Arial-Bold', 
                        size=(1080, 1920), method='caption', align='center')
    txt_clip = txt_clip.set_duration(duration)

    # Combine Audio and Visuals
    video = txt_clip.set_audio(audio_clip)
    output_video = "final_reel.mp4"
    video.write_videofile(output_video, fps=24, codec='libx264', audio_codec='aac')
    
    print("Typography video generated successfully!")
    return output_video

if __name__ == "__main__":
    generate_video()
