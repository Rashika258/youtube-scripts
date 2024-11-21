import os
from moviepy.editor import VideoFileClip, AudioFileClip
import random

# Paths
video_directory = r'C:\Users\rashi\Downloads\Video_Folder'  # Update with your video folder path
audio_directory = r'C:\Users\rashi\Downloads\Audio_Folder'  # Update with your audio folder path
output_directory = r'C:\Users\rashi\Downloads\Output_Videos'  # Update with your output path

# Create output directory if it doesn't exist
if not os.path.exists(output_directory):
    os.makedirs(output_directory)

# Collect all video and audio file paths
video_files = []
audio_files = []

# Gather video files
for root, _, files in os.walk(video_directory):
    for file in files:
        if file.lower().endswith(('.mp4', '.mov', '.avi', '.mkv')):
            video_files.append(os.path.join(root, file))

# Gather audio files
for root, _, files in os.walk(audio_directory):
    for file in files:
        if file.lower().endswith(('.mp3', '.wav')):
            audio_files.append(os.path.join(root, file))

# Dictionary to store matched pairs
matched_pairs = []

# Match audio files to video files based on duration
for video_path in video_files:
    video_clip = VideoFileClip(video_path)
    video_duration = video_clip.duration  # Duration in seconds

    # Filter audio files based on length (within a range)
    matching_audio = [audio for audio in audio_files if abs(AudioFileClip(audio).duration - video_duration) < 0.5]
    
    if matching_audio:
        # Randomly select one matching audio file
        selected_audio = random.choice(matching_audio)
        matched_pairs.append((video_path, selected_audio))

        # Remove selected audio from the list to avoid reuse
        audio_files.remove(selected_audio)

        # Combine audio and video
        audio_clip = AudioFileClip(selected_audio)
        combined_video_path = os.path.join(output_directory, f"{os.path.basename(video_path).split('.')[0]}_with_audio.mp4")

        # Set the audio to the video
        video_with_audio = video_clip.set_audio(audio_clip)
        video_with_audio.write_videofile(combined_video_path, codec='libx264', audio_codec='aac')

        print(f"Combined {os.path.basename(video_path)} with {os.path.basename(selected_audio)}")

    # Close the video clip
    video_clip.close()

print("Finished combining audio with videos.")
