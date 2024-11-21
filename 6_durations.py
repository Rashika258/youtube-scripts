import os
import pandas as pd
from moviepy.editor import VideoFileClip, AudioFileClip
import logging

# Set up logging
logging.basicConfig(
    filename='media_durations.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# Function to get durations of audio files
def get_audio_durations(audio_directory):
    audio_data = []
    for root, _, files in os.walk(audio_directory):
        for file in files:
            if file.lower().endswith(('.mp3', '.wav')):
                audio_path = os.path.join(root, file)
                try:
                    audio_duration = AudioFileClip(audio_path).duration
                    audio_data.append({
                        "File Name": file,
                        "File Path": audio_path,
                        "Type": "Audio",
                        "Duration (seconds)": round(audio_duration, 2)
                    })
                    logging.info(f"Loaded audio file {file} with duration: {audio_duration:.2f}s")
                except Exception as e:
                    logging.error(f"Error loading audio file {file}: {e}")
    return audio_data

# Function to get durations of video files
def get_video_durations(video_directory):
    video_data = []
    for root, _, files in os.walk(video_directory):
        for file in files:
            if file.lower().endswith(('.mp4', '.mov', '.avi', '.mkv')):
                video_path = os.path.join(root, file)
                try:
                    video_duration = VideoFileClip(video_path).duration
                    video_data.append({
                        "File Name": file,
                        "File Path": video_path,
                        "Type": "Video",
                        "Duration (seconds)": round(video_duration, 2)
                    })
                    logging.info(f"Loaded video file {file} with duration: {video_duration:.2f}s")
                except Exception as e:
                    logging.error(f"Error loading video file {file}: {e}")
    return video_data

# Main function to combine data and save to Excel
def save_durations_to_excel(audio_directory, video_directory, output_excel_path):
    # Get data for both audio and video files
    audio_data = get_audio_durations(audio_directory)
    # video_data = get_video_durations(video_directory)
    
    # Combine both lists
    all_media_data = audio_data
    # audio_data + video_data
    
    # Convert to DataFrame
    df = pd.DataFrame(all_media_data)
    
    # Save to Excel
    df.to_excel(output_excel_path, index=False)
    logging.info(f"Successfully saved media durations to {output_excel_path}")

# Paths
audio_directory = r'C:\Users\rashi\Downloads\audio2'
video_directory = r'C:\Users\rashi\Downloads\Processed_Videos'
output_excel_path = r'C:\Users\rashi\Downloads\audio2.xlsx'

# Run the function
save_durations_to_excel(audio_directory, video_directory, output_excel_path)
