import os
import requests

# Freesound API key and base URL
api_key = ""  # Replace with your actual API key
base_url = "https://freesound.org/apiv2/search/text/"

# Destination directory for downloaded audio files
destination_folder = r"C:\Users\rashi\Downloads\audio3"
if not os.path.exists(destination_folder):
    os.makedirs(destination_folder)

# Define search parameters
params = {
    "query": "music",
    "filter": "duration:[30 TO *]",  # Filter for audio files longer than 30 seconds
    "fields": "id,name,previews,duration",
    "sort": "rating_desc",
    "token": api_key,
    "page_size": 150  # Maximum results per page (as limited by Freesound)
}

# Download audio files
file_count = 6000
page = 1
while file_count < 7000:
    # Set the page number for each request
    params["page"] = page
    response = requests.get(base_url, params=params)

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
        # if file_count >= 1700:  # Ensure it does not exceed 4000 files
        #     break

        sound_name = sound["name"]
        # Sanitize the filename by replacing invalid characters
        sanitized_name = "".join(c for c in sound_name if c.isalnum() or c in (" ", "_")).rstrip()  # Keep alphanumeric and spaces
        preview_url = sound["previews"]["preview-hq-mp3"]

        # Check if the preview URL is available
        if not preview_url:
            print(f"No preview available for {sound_name}. Skipping...")
            continue
        
        # Save the audio file with a unique filename
        file_name = f"{file_count + 1}_{sanitized_name}.mp3"  # Use sanitized name
        file_path = os.path.join(destination_folder, file_name)

        try:
            audio_data = requests.get(preview_url)
            audio_data.raise_for_status()  # Raise an error for bad responses

            # Save the audio file
            with open(file_path, "wb") as file:
                file.write(audio_data.content)

            file_count += 1
            print(f"Downloaded: {file_name}")
        except Exception as e:
            print(f"Failed to download {sound_name}: {e}")

    # Go to the next page of results
    page += 1

print("Download complete.")
