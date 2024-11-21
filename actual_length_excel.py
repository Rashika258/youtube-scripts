import os
import pandas as pd
from moviepy.editor import VideoFileClip

# Folder path containing the video files
folder_path = r'C:\Users\rashi\Downloads\Processed_Videos'  # Replace with your folder path

# Function to get video file durations
def get_video_durations(folder_path):
    file_info = []
    
    for filename in os.listdir(folder_path):
        if filename.lower().endswith(('.mp4', '.mov', '.avi', '.mkv')):  # Modify file types if needed
            file_path = os.path.join(folder_path, filename)
            
            try:
                # Open video file and get duration
                with VideoFileClip(file_path) as video:
                    duration = video.duration  # Duration in seconds
                    file_info.append({
                        'File Name': filename,
                        'File Path': file_path,
                        'Duration (seconds)': duration
                    })
            except Exception as e:
                print(f"Error processing {filename}: {e}")

    return file_info

# Get the video durations
file_info = get_video_durations(folder_path)

# Convert the information to a DataFrame
file_info_df = pd.DataFrame(file_info)

# Save the DataFrame to Excel
output_file = r'C:\Users\rashi\Downloads\video_durations.xlsx'  # Specify the path to save the Excel file
file_info_df.to_excel(output_file, index=False)

print(f"Video durations saved to {output_file}")
