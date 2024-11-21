import os
import pandas as pd
from moviepy.editor import VideoFileClip

# Paths
video_folder = r'C:\Users\rashi\Downloads\Output_Videos'  # Folder containing the original video files
metadata_file = r'C:\Users\rashi\Downloads\video_durations.xlsx'  # Excel file with filename and target duration

# Read the metadata file
metadata_df = pd.read_excel(metadata_file)
rows_to_drop = []

# Process each entry in the Excel file
for index, row in metadata_df.iterrows():
    filename = row['File Name']
    target_duration = row['Duration (seconds)']  # Duration to trim to, in seconds

    # Modify filename: Remove .mp4 and add _with_audio.mp4
    modified_filename = filename.replace('.mp4', '_with_audio.mp4')

    # Path to the video file
    file_path = os.path.join(video_folder, modified_filename)

    # Check if the video file exists
    if os.path.exists(file_path):
        try:
            # Load the video
            video = VideoFileClip(file_path)
            
            # Only trim if the video's actual duration is longer than the specified duration
            if video.duration > target_duration:
                # Trim the video
                trimmed_video = video.subclip(0, target_duration)

                # Overwrite the original video file
                trimmed_video.write_videofile(file_path, codec="libx264")

                print(f"Trimmed video saved and replaced original: {file_path}")
            else:
                rows_to_drop.append(index)  # Mark this row for removal

                print(f"Video '{modified_filename}' is shorter than or equal to the target duration; no trimming needed.")
        
        except Exception as e:
            print(f"Error processing {modified_filename}: {e}")
    else:
        print(f"File not found: {modified_filename}")

metadata_df.drop(rows_to_drop, inplace=True)
metadata_df.to_excel(metadata_file, index=False)



print("Video trimming process completed.")
