import os
import pandas as pd
from moviepy.editor import VideoFileClip, AudioFileClip

# Function to get video files information
def get_video_files_info(folder_path):
    video_files_info = []

    for filename in os.listdir(folder_path):
        if filename.endswith('.mp4'):  # Assuming only mp4 videos
            file_path = os.path.join(folder_path, filename)
            try:
                with VideoFileClip(file_path) as video:
                    duration = video.duration  # Duration in seconds
                video_files_info.append({
                    'File Name': filename,
                    'File Path': file_path,
                    'Type': 'video',
                    'Duration': duration
                })
            except Exception as e:
                print(f"Error processing {filename}: {e}")
                continue
    
    # Sort files by duration
    video_files_info.sort(key=lambda x: x['Duration'])
    return video_files_info

# Function to get audio files information (using AudioFileClip from moviepy)
def get_audio_files_info(folder_path):
    audio_files_info = []

    for filename in os.listdir(folder_path):
        if filename.endswith(('.mp3', '.wav', '.flac')):  # Adjust file types as needed
            file_path = os.path.join(folder_path, filename)
            try:
                with AudioFileClip(file_path) as audio:
                    duration = audio.duration  # Duration in seconds
                audio_files_info.append({
                    'File Name': filename,
                    'File Path': file_path,
                    'Type': 'audio',
                    'Duration': duration
                })
            except Exception as e:
                print(f"Error processing {filename}: {e}")
                continue
    
    # Sort files by duration
    audio_files_info.sort(key=lambda x: x['Duration'])
    return audio_files_info

# Function to save data to Excel
def save_to_excel(files_info, output_file):
    # Create a DataFrame from the file information
    df = pd.DataFrame(files_info)

    # Save to Excel
    df.to_excel(output_file, index=False)
    print(f"Excel file saved as {output_file}")

# Paths for the audio and video folders
audio_folder_path = r'C:\Users\rashi\Downloads\Freesound_Audio'  # Replace with your audio folder path
video_folder_path = r'C:\Users\rashi\Downloads\Upload_videos'  # Replace with your video folder path

# Get audio and video file information
audio_files_info = get_audio_files_info(audio_folder_path)
video_files_info = get_video_files_info(video_folder_path)

# Save audio and video information to separate Excel files, sorted by duration
save_to_excel(audio_files_info, r'C:\Users\rashi\Downloads\audio_sorted.xlsx')
save_to_excel(video_files_info, r'C:\Users\rashi\Downloads\video_sorted.xlsx')
