import os

# Define the folder to scan
folder_path = r'C:\Users\rashi\Downloads\Output2'  # Replace with your folder path

# List all files in the folder
for filename in os.listdir(folder_path):
    # Check if "Copy" is in the filename (case-sensitive)
    if 'Copy' in filename:
        file_path = os.path.join(folder_path, filename)
        
        # Ensure it's a file (not a folder)
        if os.path.isfile(file_path):
            try:
                # Delete the file
                os.remove(file_path)
                print(f"Deleted {filename}")
            except Exception as e:
                print(f"Error deleting {filename}: {e}")
