import os
import pandas as pd

# Define the paths
excel_path = r'C:\Users\rashi\Downloads\youtube_video_metadata.xlsx'  # Path to your Excel file
source_folder = r'C:\Users\rashi\Downloads\Upload_videos'  # Folder where the files are located
destination_folder = r'C:\Users\rashi\Downloads\Moved_Files'  # Folder to move files to

# Create the destination folder if it doesn't exist
os.makedirs(destination_folder, exist_ok=True)

# Load the Excel file
df = pd.read_excel(excel_path)

# Check each file in the "Actual File Name" column
for _, row in df.iterrows():
    file_name = row['Actual File Name']  # Assuming the column is named "Actual File Name"
    file_path = os.path.join(source_folder, file_name)
    
    # Check if the file exists in the source folder
    if os.path.exists(file_path):
        # Define the destination path
        destination_path = os.path.join(destination_folder, file_name)
        
        # Use os.rename() to move the file
        try:
            os.rename(file_path, destination_path)
            print(f"Moved {file_name} to {destination_folder}")
        except Exception as e:
            print(f"Error moving {file_name}: {e}")
    else:
        print(f"File {file_name} not found in {source_folder}")
