import os
import datetime
import pandas as pd
from moviepy.editor import VideoFileClip
from google.oauth2 import service_account
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

# Set paths
CLIENT_SECRET_FILE = r'C:\Users\rashi\Downloads\client_secret.json'  # Path to your OAuth 2.0 credentials JSON file
SCOPES = ['https://www.googleapis.com/auth/youtube.upload']
video_folder = r'C:\Users\rashi\Downloads\Output_Videos'  # Path to the folder containing video files
metadata_file = r'C:\Users\rashi\Downloads\metadata.xlsx'  # Path to your Excel metadata file
duration_file = r'C:\Users\rashi\Downloads\video_durations.xlsx'  # Path to the Excel file containing file names and their durations
category_id = '22'  # Example: '22' is for People & Blogs
tags = ['shorts', 'facts', 'motivation']

# Authenticate with OAuth 2.0 user flow (explicit port set to 8080)
flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRET_FILE, SCOPES)
credentials = flow.run_local_server(port=8080)  # Set the port to 8080 explicitly
youtube = build('youtube', 'v3', credentials=credentials)

# Function to upload and schedule video
def upload_video(file_path, title, description, category_id, tags, scheduled_time):
    body = {
        'snippet': {
            'title': title,
            'description': description,
            'tags': tags,
            'categoryId': category_id
        },
        'status': {
            'privacyStatus': 'private',  # Set to 'private' for scheduled videos
            'publishAt': scheduled_time.isoformat() + 'Z'  # Schedule for publish time in UTC
        }
    }
    
    media = MediaFileUpload(file_path, chunksize=-1, resumable=True)

    # Call the API to upload the video
    try:
        request = youtube.videos().insert(
            part="snippet,status",
            body=body,
            media_body=media
        )
        response = request.execute()
        print(f"Video uploaded: {response['id']} (Title: {title})")
    except Exception as e:
        print(f"Failed to upload {file_path}: {e}")

# Read metadata and duration data from Excel
metadata_df = pd.read_excel(metadata_file)
duration_df = pd.read_excel(duration_file)  # This Excel should contain 'File Name' and 'Duration'

# Schedule videos for upload in batches of 10
schedule_start_time = datetime.datetime.utcnow()  # Start scheduling from now

# List of video files to be uploaded
video_files = [filename for filename in os.listdir(video_folder) if filename.lower().endswith(('.mp4', '.mov', '.avi', '.mkv'))]

# Ensure videos are scheduled in batches of 10
for i in range(0, len(video_files), 10):
    # Get the batch of 10 videos
    batch = video_files[i:i+10]
    
    # Schedule the videos for the current day or the next day
    scheduled_time = schedule_start_time + datetime.timedelta(days=i//10)  # Increment by 1 day for each batch
    
    for j, filename in enumerate(batch):
        file_path = os.path.join(video_folder, filename)

        # Retrieve title and description from metadata DataFrame using File Name
        video_metadata = metadata_df[metadata_df['File Name'].str.lower() == filename.lower()]

        # Retrieve video duration from the duration file using Actual File Name
        actual_file_name = video_metadata['Actual File Name'].values[0]  # Get the Actual File Name from metadata
        video_duration = duration_df[duration_df['File Name'].str.lower() == actual_file_name.lower()]

        if not video_metadata.empty:
            title = video_metadata['Title'].values[0]
            description = video_metadata['Description'].values[0]

            # Check if the filename is present in the duration file
            if not video_duration.empty:
                # Get the duration from the duration Excel file
                max_duration = video_duration['Duration (seconds)'].values[0]

                with VideoFileClip(file_path) as video:
                    if video.duration > max_duration:
                        print(f"Trimming {filename} to {max_duration} seconds.")
                        video = video.subclip(0, max_duration)  # Trim the video if necessary
                        trimmed_file_path = os.path.join(video_folder, f"{filename}")
                        video.write_videofile(trimmed_file_path, codec='libx264', audio_codec='aac')

                        # Update the file path to the trimmed video
                        file_path = trimmed_file_path
                    else:
                        print(f"No trimming needed for {filename}.")
            
            # Upload and schedule the video with the fixed scheduled time
            # upload_video(file_path, title, description, category_id, tags, scheduled_time)
        else:
            print(f"No metadata found for {filename}. Skipping.")

    print(f"Batch {i//10 + 1} of videos scheduled.")

print("Bulk scheduling of videos completed.")
