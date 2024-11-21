import os

def count_files_in_directory(directory):
    try:
        # List all files in the given directory
        files = os.listdir(directory)
        # Count only files (not directories)
        file_count = sum(os.path.isfile(os.path.join(directory, file)) for file in files)
        return file_count
    except Exception as e:
        print(f"An error occurred: {e}")
        return 0

# Replace with your directory path
# directory_path = r'C:\Users\rashi\Downloads\Output2' 
# directory_path = r'C:\Users\rashi\Downloads\Processed_Videos' 
# directory_path = r'C:\Users\rashi\Downloads\Output_Videos' 
# directory_path = r'C:\Users\rashi\Downloads\Upload_videos' 
# directory_path = r'C:\Users\rashi\Downloads\Freesound_Audio' 
directory_path = r'C:\Users\rashi\Downloads\Output3' 
# directory_path = r'C:\Users\rashi\Downloads\Moved_Files' 

total_files = count_files_in_directory(directory_path)
print(f"Total files in '{directory_path}': {total_files}")
