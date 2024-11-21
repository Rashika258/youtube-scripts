import os
import pandas as pd
from moviepy.editor import VideoFileClip
from shutil import move

# Folder containing the video files
video_folder = r'C:\Users\rashi\Downloads\Output_Videos'  # Adjust path as needed
error_folder = os.path.join(video_folder, 'error_videos')  # Folder for problematic videos

# Ensure the error folder exists
os.makedirs(error_folder, exist_ok=True)

# Initialize a list to store metadata for each video
video_metadata = []

# Default metadata values
default_title = "My Video Title"
default_description = "This is a default description for the video."
default_category = "22"  # Category ID for 'People & Blogs' on YouTube
default_tags = "default, tags, for, video"

# Process each video file in the folder
for filename in os.listdir(video_folder):
    if filename.endswith('.mp4'):  # Filter for .mp4 files; adjust if needed
        file_path = os.path.join(video_folder, filename)

        
        # Generate modified filename by removing '_with_audio' if present and ensuring '.mp4' extension
        modified_filename = filename.replace('_with_audio', '').replace('.mp4', '') + '.mp4'
        modified_file_path = os.path.join(video_folder, modified_filename)

        print(f"Processing {filename}... ${modified_filename}")

        
        # Collect metadata information
        try:
            video = VideoFileClip(file_path)
            
            # Add metadata for the modified file
            video_metadata.append({
                "Actual File Name": modified_filename,
                "File Name": filename,
                "File Path": modified_file_path,
                "Duration (seconds)": round(video.duration, 2),
                "File Size (MB)": round(os.path.getsize(file_path) / (1024 * 1024), 2),
                "Title": default_title,
                "Description": default_description,
                "Tags": default_tags,
                "Category": default_category,
            })
        except Exception as e:
            print(f"Error processing {filename}: {e}")
            # Move file to error folder
            error_path = os.path.join(error_folder, filename)
            move(file_path, error_path)  # Move problematic file to error folder
            continue  # Skip this file and don't add it to the metadata list

# Convert to DataFrame
metadata_df = pd.DataFrame(video_metadata)

# Save metadata to an Excel file
output_file = os.path.join(video_folder, 'metadata.xlsx')
metadata_df.to_excel(output_file, index=False)

print(f"Metadata Excel file generated: {output_file}")
