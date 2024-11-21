import os
import requests
import pandas as pd

# Replace with your Freesound API key
API_KEY = ''  # Use your actual API key
# Directory where your downloaded audio files are stored
audio_directory = r'C:\Users\rashi\Downloads\Freesound_Audio'  # Update with your audio folder path
output_excel_path = r'C:\Users\rashi\Downloads\audio_info.xlsx'  # Path to save the Excel file

def search_sound_by_name(name):
    url = "https://freesound.org/apiv2/search/text/"
    headers = {'Authorization': f'Token {API_KEY}'}
    params = {
        'query': name,
        'page_size': 1,  # Limit results to 1 to get the first match
    }
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed to search for '{name}': {response.status_code} - {response.text}")
        return None

def get_sound_info(freesound_id):
    url = f"https://freesound.org/apiv2/sounds/{freesound_id}/"
    headers = {'Authorization': f'Token {API_KEY}'}
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        data = response.json()
        print(f"Data for ID {freesound_id}: {data}")  # Debug print

        # Extracting the required fields
        sound_info = {
            "ID": data.get('id'),
            "Name": data.get('name'),
            "License": data.get('license'),  # License URL
            "Type": data.get('type'),
            "Username": data.get('username'),
            "Download": data.get('download'),  # API link for download
            "Similar Sounds": data.get('similar_sounds')  # API link for similar sounds
        }
        return sound_info
    else:
        print(f"Failed to fetch data for ID {freesound_id}: {response.status_code} - {response.text}")
        return None

# Initialize a list to hold results
results = []

# Iterate through files in the specified directory
for filename in os.listdir(audio_directory):
    if filename.lower().endswith(('.mp3', '.wav', '.ogg', '.flac')):  # Add other formats as needed
        # Remove the file extension to use for search
        name_without_extension = os.path.splitext(filename)[0]
        
        # Search for the sound
        search_result = search_sound_by_name(name_without_extension)
        
        if search_result and search_result['results']:
            sound_id = search_result['results'][0]['id']
            sound_info = get_sound_info(sound_id)
            if sound_info:
                # Append sound info to results list
                results.append(sound_info)
        else:
            print(f"No results found for '{filename}'")

# Create a DataFrame and save to Excel
if results:  # Only save if there are results
    df = pd.DataFrame(results)
    df.to_excel(output_excel_path, index=False)
    print(f"Successfully saved sound information to {output_excel_path}.")
else:
    print("No sound information was collected.")
