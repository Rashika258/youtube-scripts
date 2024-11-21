import os
import requests
import pandas as pd

# Freesound API key and base URL
API_KEY = ''  # Replace with your actual API key
BASE_URL = "https://freesound.org/apiv2/search/text/"
# Destination directory for downloaded audio files
DESTINATION_FOLDER = r"C:\Users\rashi\Downloads\audio2"
EXCEL_PATH = r"C:\Users\rashi\Downloads\audio_info1.xlsx"

# Create the destination folder if it doesn't exist
if not os.path.exists(DESTINATION_FOLDER):
    os.makedirs(DESTINATION_FOLDER)

# Define search parameters
params = {
    "query": "music",
    "filter": "duration:[30 TO *]",  # Filter for audio files longer than 30 seconds
    "fields": "id,name,previews,duration,license",  # Include license in fields
    "sort": "rating_desc",
    "token": API_KEY,
    "page_size": 150  # Maximum results per page (as limited by Freesound)
}

# Initialize list to store audio metadata
audio_metadata = []

# Download audio files and store metadata
file_count = 2927
page = 1

while file_count < 5000:
    # Set the page number for each request
    params["page"] = page
    response = requests.get(BASE_URL, params=params)

    # Check for successful request
    if response.status_code != 200:
        print("Error fetching data:", response.status_code)
        break

    # Process the JSON response data
    data = response.json()
    sounds = data.get("results", [])
    if not sounds:
        print("No more results.")
        break

    # Download each sound's audio preview
    for sound in sounds:
        # if file_count >= 1700:  # Ensure it does not exceed 1700 files
        #     break

        sound_id = sound["id"]
        sound_name = sound["name"]
        license_info = sound["license"]
        preview_url = sound["previews"].get("preview-hq-mp3")

        # Check if the preview URL is available
        if not preview_url:
            print(f"No preview available for {sound_name}. Skipping...")
            continue
        
        # Sanitize the filename by removing invalid characters
        sanitized_name = "".join(c for c in sound_name if c.isalnum() or c in (" ", "_")).rstrip()
        file_name = f"{file_count + 1}_{sanitized_name}.mp3"
        file_path = os.path.join(DESTINATION_FOLDER, file_name)

        # Download and save the audio file
        try:
            audio_data = requests.get(preview_url)
            audio_data.raise_for_status()

            # Save the audio file
            with open(file_path, "wb") as file:
                file.write(audio_data.content)

            # Store metadata for Excel
            audio_metadata.append({
                "ID": sound_id,
                "Name": sound_name,
                "License": license_info,
                "File Path": file_path
            })

            file_count += 1
            print(f"Downloaded: {file_name}")
        except Exception as e:
            print(f"Failed to download {sound_name}: {e}")

    # Go to the next page of results
    page += 1

# Save metadata to Excel file
df = pd.DataFrame(audio_metadata)
df.to_excel(EXCEL_PATH, index=False)
print(f"Download complete. Audio information saved to {EXCEL_PATH}.")
