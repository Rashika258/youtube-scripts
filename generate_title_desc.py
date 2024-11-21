import os
import cv2
import numpy as np
import pandas as pd
import moviepy.editor as mp

video_directory = r'C:\Users\rashi\Downloads\Upload_videos'  # Path to your video folder
output_excel_path = r'C:\Users\rashi\Downloads\video_details.xlsx'  # Path to save the Excel file

# Load the EAST text detector model
net = cv2.dnn.readNet("frozen_east_text_detection.pb")  # Path to the EAST model file

def decode_predictions(scores, geometry):
    # Grab the number of rows and columns from the scores volume, then initialize
    # our set of bounding box rectangles and corresponding confidence scores
    (num_rows, num_cols) = scores.shape[2:4]
    boxes = []
    confidences = []

    # Loop over the number of rows
    for y in range(num_rows):
        # Extract the scores (probabilities) and the geometrical data
        scores_data = scores[0][0][y]
        x0_data = geometry[0][0][y]
        x1_data = geometry[0][1][y]
        x2_data = geometry[0][2][y]
        x3_data = geometry[0][3][y]
        angles_data = geometry[0][4][y]
        
        for x in range(num_cols):
            if scores_data[x] < 0.5:
                continue

            # Compute the offset factor as the respective ratio of the
            # width and height of the 4D map
            offset_x, offset_y = (x * 4.0, y * 4.0)
            angle = angles_data[x]
            cos_a = np.cos(angle)
            sin_a = np.sin(angle)

            h = x0_data[x] + x2_data[x]
            w = x1_data[x] + x3_data[x]

            # Compute the bounding box
            p1 = int(offset_x + (cos_a * x1_data[x]) + (sin_a * x2_data[x])), int(offset_y - (sin_a * x1_data[x]) + (cos_a * x2_data[x]))
            p2 = int(offset_x - (sin_a * x3_data[x]) + (cos_a * x2_data[x])), int(offset_y + (cos_a * x3_data[x]) + (sin_a * x2_data[x]))

            # Append the bounding box and associated probability
            boxes.append((p1[0], p1[1], p2[0], p2[1]))
            confidences.append(float(scores_data[x]))

    return (boxes, confidences)

def extract_text_from_video(video_path):
    print(f"Extracting text from {video_path}...")
    video_clip = mp.VideoFileClip(video_path)
    extracted_text = []

    for frame_number in range(0, int(video_clip.fps * video_clip.duration), int(video_clip.fps)):
        frame = video_clip.get_frame(frame_number / video_clip.fps)
        orig = frame.copy()
        frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
        height, width = frame.shape[:2]
        
        # Create a blob from the image and perform a forward pass of
        # the model to obtain the two output layer sets
        blob = cv2.dnn.blobFromImage(frame, 1.0, (width, height),
                                      (123.68, 116.78, 103.94), swapRB=True, crop=False)
        net.setInput(blob)
        (scores, geometry) = net.forward(["feature_fusion/Conv_7/Sigmoid",
                                           "feature_fusion/concat_3"])

        (boxes, confidences) = decode_predictions(scores, geometry)
        indices = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.4)

        for i in indices:
            (x0, y0, x1, y1) = boxes[i[0]]
            # Crop the detected text region and apply OCR
            cropped = orig[y0:y1, x0:x1]
            text = pytesseract.image_to_string(cropped)
            if text.strip():
                extracted_text.append(text.strip())
    
    return extracted_text

# Rest of your processing code remains the same...
