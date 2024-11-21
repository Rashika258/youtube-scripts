import os
import pandas as pd
from moviepy.editor import VideoFileClip, AudioFileClip
import random
import logging
import bisect

# Set up logging
logging.basicConfig(
    filename='video_audio_merger.log',
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# Paths
video_directory = r'C:\Users\rashi\Downloads\Upload_videos'
audio_directory = r'C:\Users\rashi\Downloads\Freesound_Audio'
output_directory = r'C:\Users\rashi\Downloads\Output_Videos'
used_audio_directory = r'C:\Users\rashi\Downloads\Used_Audios'
processed_video_directory = r'C:\Users\rashi\Downloads\Processed_Videos'
excel_output_path = r'C:\Users\rashi\Downloads\merged_files.xlsx'

# Create necessary directories if they don’t exist
os.makedirs(output_directory, exist_ok=True)
os.makedirs(used_audio_directory, exist_ok=True)
os.makedirs(processed_video_directory, exist_ok=True)

# Collect all video and audio file paths
video_files = []
audio_files = {}

# Gather video files (limit to the first 10)
for root, _, files in os.walk(video_directory):
    for file in files:
        if file.lower().endswith(('.mp4', '.mov', '.avi', '.mkv')):
            video_files.append(os.path.join(root, file))
            print(file, "file1")
            if len(video_files) >= 10:  # Limit to the first 10 video files
                break
    if len(video_files) >= 10:
        break

logging.info(f"Found {len(video_files)} video files.")

# Gather and pre-sort audio files by duration
for root, _, files in os.walk(audio_directory):
    for file in files:
        if file.lower().endswith(('.mp3', '.wav')):
            audio_path = os.path.join(root, file)
           
            try:
                audio_duration = AudioFileClip(audio_path).duration
                print(file, "file1", audio_duration)
                audio_files[audio_path] = audio_duration
                logging.error(f"Length of audio file {file}: {audio_duration}")
            except Exception as e:
                logging.error(f"Error loading audio file {file}: {e}")

# Sort audio files by duration
sorted_audio_files = sorted(audio_files.items(), key=lambda item: item[1])
durations = [duration for _, duration in sorted_audio_files]

logging.info(f"Loaded and sorted {len(audio_files)} audio files.")

# Function to find the smallest audio file >= video duration
def find_matching_audio(video_duration):
    index = bisect.bisect_left(durations, video_duration)
    if index < len(durations):
        return sorted_audio_files[index][0]  # Return matching audio file path
    return None

# List to track merged video-audio pairs
merged_files = []

# Match audio files to video files based on duration
for video_path in video_files:
    video_clip = None
    audio_clip = None

    try:
        video_clip = VideoFileClip(video_path)
        video_duration = video_clip.duration
        logging.info(f"Processing video: {os.path.basename(video_path)}, Duration: {video_duration:.2f}s")

        # Find a matching audio file with duration >= video duration
        matching_audio = find_matching_audio(video_duration)

        if matching_audio:
            audio_files.pop(matching_audio)  # Remove selected audio to avoid reuse
            audio_clip = AudioFileClip(matching_audio)
            combined_video_path = os.path.join(
                output_directory, f"{os.path.splitext(os.path.basename(video_path))[0]}_with_audio.mp4"
            )

            # Set the audio to the video
            video_with_audio = video_clip.set_audio(audio_clip)
            video_with_audio.write_videofile(combined_video_path, codec='libx264', audio_codec='aac')

            # Append video-audio pair to merged_files list
            merged_files.append({
                "Video File": os.path.basename(video_path),
                "Audio File": os.path.basename(matching_audio)
            })

            # Move used audio file to the Used_Audios folder
            used_audio_path = os.path.join(used_audio_directory, os.path.basename(matching_audio))
            os.rename(matching_audio, used_audio_path)

            # Move processed video file to the Processed_Videos folder
            processed_video_path = os.path.join(processed_video_directory, os.path.basename(video_path))
            os.rename(video_path, processed_video_path)

            logging.info(f"Combined {os.path.basename(video_path)} with {os.path.basename(matching_audio)}")

        else:
            logging.warning(f"No matching audio found for {os.path.basename(video_path)} (Duration: {video_duration:.2f}s)")

    except Exception as e:
        logging.error(f"Error processing video {video_path}: {e}")
    finally:
        if video_clip:
            video_clip.close()
        if audio_clip:
            audio_clip.close()

# Save merged pairs to Excel
if merged_files:
    df = pd.DataFrame(merged_files)
    df.to_excel(excel_output_path, index=False)
    logging.info(f"Successfully saved merged video-audio pairs to {excel_output_path}")
else:
    logging.info("No merged files to save.")

logging.info("Finished combining audio with videos.")
