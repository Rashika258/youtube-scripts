import os
import pandas as pd
import logging
from moviepy.editor import VideoFileClip, AudioFileClip
from shutil import move

# Set up logging
logging.basicConfig(
    filename='media_matching.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# Paths for organizing media
used_audio_directory = r'C:\Users\rashi\Downloads\Used_Audios'
processed_video_directory = r'C:\Users\rashi\Downloads\Processed_Videos'
output_directory = r'C:\Users\rashi\Downloads\Output5'

# Create necessary directories if they don’t exist
os.makedirs(output_directory, exist_ok=True)
os.makedirs(used_audio_directory, exist_ok=True)
os.makedirs(processed_video_directory, exist_ok=True)

# Function to load media files from sorted Excel files
def load_sorted_media(audio_excel_path, video_excel_path):
    audio_df = pd.read_excel(audio_excel_path)
    video_df = pd.read_excel(video_excel_path)
    return video_df, audio_df

# Function to match videos with the nearest audio files
def match_videos_with_audio(video_df, audio_df, output_directory, audio_excel_path, video_excel_path):
    used_audio = set()  # Track used audio files
    matches = []  # Store matched pairs for Excel update
    processed_video_indices = []  # Track processed video rows
    processed_audio_indices = []  # Track processed audio rows

    for video_idx, video in video_df.iterrows():
        video_duration = video['Duration']
        video_path = video['File Path']
        
        # Find the nearest audio that has duration >= video duration
        matching_audio = audio_df[(audio_df['Duration'] >= video_duration) & 
                                  (~audio_df['File Path'].isin(used_audio))]
        
        if not matching_audio.empty:
            # Select the audio with the least duration that meets the condition
            selected_audio_idx = matching_audio['Duration'].idxmin()
            selected_audio = matching_audio.loc[selected_audio_idx]
            audio_path = selected_audio['File Path']
            used_audio.add(audio_path)  # Mark this audio as used
            
            # Combine audio with video and save
            try:
                with VideoFileClip(video_path) as video_clip, AudioFileClip(audio_path) as audio_clip:
                    # Trim the audio to match the video's duration
                    trimmed_audio = audio_clip.subclip(0, video_duration)
                    
                    # Combine the trimmed audio with the video
                    video_with_audio = video_clip.set_audio(trimmed_audio)
                    
                    # Output file path
                    output_path = os.path.join(
                        output_directory, f"{os.path.splitext(os.path.basename(video_path))[0]}_with_audio.mp4"
                    )
                    video_with_audio.write_videofile(output_path, codec='libx264', audio_codec='aac')
                    
                    # Add to matches list
                    matches.append({
                        "Video File": os.path.basename(video_path),
                        "Audio File": os.path.basename(audio_path),
                        "Output File": os.path.basename(output_path)
                    })

                    # Move used audio file to the Used_Audios folder
                    move(audio_path, os.path.join(used_audio_directory, os.path.basename(audio_path)))
                    
                    # Move processed video file to the Processed_Videos folder
                    move(video_path, os.path.join(processed_video_directory, os.path.basename(video_path)))

                    # Log successful match
                    logging.info(f"Matched {video['File Name']} with {selected_audio['File Name']}")

                    # Record indices to remove from DataFrames
                    processed_video_indices.append(video_idx)
                    processed_audio_indices.append(selected_audio_idx)
            except Exception as e:
                logging.error(f"Error merging {video['File Name']} with {selected_audio['File Name']}: {e}")

        else:
            logging.warning(f"No matching audio found for video {video['File Name']} with duration {video_duration:.2f}s")

    # Remove processed rows from DataFrames and save updated Excel files
    updated_video_df = video_df.drop(index=processed_video_indices)
    updated_audio_df = audio_df.drop(index=processed_audio_indices)
    updated_video_df.to_excel(video_excel_path, index=False)
    updated_audio_df.to_excel(audio_excel_path, index=False)

    # Return all matched pairs
    return matches

# Paths to the sorted Excel files
audio_excel_path = r'C:\Users\rashi\Downloads\audio_sorted.xlsx'  # Update with your audio Excel file path
video_excel_path = r'C:\Users\rashi\Downloads\video_sorted.xlsx'  # Update with your video Excel file path

# Load media files from sorted Excel files
video_df, audio_df = load_sorted_media(audio_excel_path, video_excel_path)

# Match videos with audio and save results
matches = match_videos_with_audio(video_df, audio_df, output_directory, audio_excel_path, video_excel_path)

# Optionally save match results to another Excel file
match_df = pd.DataFrame(matches)
match_output_path = os.path.join(output_directory, 'matched_videos_with_audio.xlsx')
match_df.to_excel(match_output_path, index=False)
logging.info(f"Saved matched video-audio pairs to {match_output_path}")
