import os
import pandas as pd
from pytube import Playlist

# Function to download audio from a YouTube playlist
def download_audio_from_playlist(playlist_url, output_directory):
    # Create the output directory if it doesn't exist
    os.makedirs(output_directory, exist_ok=True)

    # Create a playlist object
    playlist = Playlist(playlist_url)

    # Prepare a list to hold video details
    video_details = []

    print(f"Downloading audio from {playlist.title}...${playlist.length} {playlist.videos} videos")

    # Iterate over each video in the playlist
    for video in playlist.videos:
        try:
            print(f"Downloading audio from {video.title}...")
    # Extract title and description
            title = video.title
            description = video.description
            # Get the audio stream
            stream = video.streams.filter(only_audio=True).first()

            # Download the audio file
            audio_file = stream.download(output_path=output_directory)

        

            # Create a dictionary with the title, description, and audio file name
            video_details.append({
                "File Name": os.path.basename(audio_file),
                "Title": title,
                "Description": description
            })

            print(f"Downloaded: {title} -> {audio_file}")

        except Exception as e:
            print(f"Failed to download {video.title}: {e}")

    # Save video details to Excel
    if video_details:
        df = pd.DataFrame(video_details)
        excel_path = os.path.join(output_directory, "video_details.xlsx")
        df.to_excel(excel_path, index=False)
        print(f"Successfully saved video details to {excel_path}.")

# Replace with your playlist URL
playlist_url = 'https://www.youtube.com/playlist?list=PLzCxunOM5WFJ7sbHi_9Zwq2xOwtkYeZlx'
output_directory = r'C:\Users\rashi\Downloads\YouTube_Audio'  # Change this to your desired output directory

download_audio_from_playlist(playlist_url, output_directory)
