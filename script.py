import os
import shutil
from random import shuffle

# Paths
source_directory = r'C:\Users\rashi\Downloads\2_Youtube_videos'  # Raw string path
destination_directory = r'C:\Users\rashi\Downloads\suffled_videos'  # Raw string path

# Collect all video file paths
all_videos = []
for root, _, files in os.walk(source_directory):
    for file in files:
        print(file, root)
        if file.lower().endswith(('.mp4', '.mov', '.avi', '.mkv')):  # Add other video formats if needed
            all_videos.append(os.path.join(root, file))

# Shuffle the video list to get a random order
shuffle(all_videos)

# Move and rename files
if not os.path.exists(destination_directory):
    os.makedirs(destination_directory)

for idx, video_path in enumerate(all_videos, start=1):
    new_name = f"{idx}.mp4"  # Assuming .mp4 extension; you can modify as needed
    new_path = os.path.join(destination_directory, new_name)
    shutil.copy2(video_path, new_path)  # Use copy2 to preserve metadata

print(f"Successfully moved and renamed {len(all_videos)} videos.")
