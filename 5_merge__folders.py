import os
from random import shuffle

# Paths
source_directory = r'C:\Users\rashi\Downloads\2_Youtube_videos'  # Update with your source path
destination_directory = r'C:\Users\rashi\Downloads\shuffled_videos'  # Update with your destination path

# Collect all video/audio file paths along with their folder names
all_videos = []
skipcount = 0
for root, _, files in os.walk(source_directory):
    for file in files:
        if file.lower().endswith(('.mp4', '.mov', '.avi', '.mkv', '.mp3', '.wav')):
            folder_name = os.path.basename(root)
            all_videos.append((os.path.join(root, file), folder_name))

# Verify total collected files
print(f"Total audio/video files collected: {len(all_videos)}")

# Shuffle the list of video paths
shuffle(all_videos)

# Create destination directory if it doesn't exist
if not os.path.exists(destination_directory):
    os.makedirs(destination_directory)

# Function to copy files using os
def copy_file(src, dst):
    try:
        with open(src, 'rb') as fsrc, open(dst, 'wb') as fdst:
            while True:
                buf = fsrc.read(1024 * 1024)  # Read in 1MB chunks
                if not buf:
                    break
                fdst.write(buf)
        print(f"Copied: {dst}")
    except Exception as e:
        print(f"Error copying file from {src} to {dst}: {e}")

# Move and rename files
for idx, (video_path, folder_name) in enumerate(all_videos, start=1):
    clean_folder_name = "".join(c for c in folder_name if c.isalnum() or c in ('_', '-'))
    file_extension = os.path.splitext(video_path)[1]
    new_name = f"{idx}_{clean_folder_name}{file_extension}"
    new_path = os.path.join(destination_directory, new_name)

    # Check for existing files
    if os.path.exists(new_path):
        skipcount += 1
        print(f"Warning: File {new_name} already exists. Skipping.")
        continue

    # Use the custom copy function
    copy_file(video_path, new_path)

print(f"Successfully moved and renamed {len(all_videos) - skipcount} videos.")
print(f"Skipped {skipcount} files due to name conflicts.")
