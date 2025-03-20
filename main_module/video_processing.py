# video_processing.py
import os
import cv2
from object_detection import get_object_detector
from annotation import annotate_image

def process_video(video_path, frames_output_dir):
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print("Error: could not open video")
        return [], 0.0

    fps = cap.get(cv2.CAP_PROP_FPS)
    frame_count = 0
    annotated_frames = []

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Run your detector on the frame here:
        detections = detector.detect(frame)
        # Draw bounding boxes, labels, etc.
        for det in detections:
            x, y, w, h = det['bbox']
            label = f"{det['label']} {det['confidence']:.2f}"
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
            cv2.putText(frame, label, (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

        frame_filename = f"{frames_output_dir}/frame_{frame_count:04d}.jpg"
        cv2.imwrite(frame_filename, frame)
        annotated_frames.append(frame_filename)
        frame_count += 1

    cap.release()
    return annotated_frames, fps

def reassemble_video(frames_dir, output_video_path, fps):
    import glob
    frame_files = sorted(glob.glob(f"{frames_dir}/frame_*.jpg"))
    if not frame_files:
        return False

    first_frame = cv2.imread(frame_files[0])
    height, width, _ = first_frame.shape
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_video_path, fourcc, fps, (width, height))
    
    for frame_file in frame_files:
        frame = cv2.imread(frame_file)
        out.write(frame)
    out.release()
    return True

