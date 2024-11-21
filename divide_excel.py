import pandas as pd

# Load data from the existing Excel file
input_file_path =r'C:\Users\rashi\Downloads\media_durations.xlsx' # Update this to your file path
df = pd.read_excel(input_file_path)

# Print the column names for debugging
print("Columns in the DataFrame:", df.columns.tolist())

# Strip any leading or trailing spaces from column names
df.columns = df.columns.str.strip()

# Check if the 'Type' and 'Duration' columns are present
if 'Type' not in df.columns or 'Duration (seconds)' not in df.columns:
    raise ValueError("Input Excel file must contain 'Type' and 'Duration' columns.")

# Sort by duration
df_sorted = df.sort_values(by='Duration (seconds)')

# Save the sorted data to separate Excel files
audio_df = df_sorted[df_sorted['Type'] == 'Audio']
video_df = df_sorted[df_sorted['Type'] == 'Video']  # Assuming there are some video entries

audio_output_file = 'audio_sorted.xlsx'
video_output_file = 'video_sorted.xlsx'

# Save all columns to the output files
audio_df.to_excel(audio_output_file, index=False)
video_df.to_excel(video_output_file, index=False)  # This will be empty if no video data is available

print(f"Excel files created: '{audio_output_file}' and '{video_output_file}'")
