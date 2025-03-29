# video_processing.py
import cv2
from PIL import Image

SKIP_FRAMES = 5

def process_video(video_path, frames_output_dir, detector, output_gif_path):
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

        if frame_count % SKIP_FRAMES != 0:
            frame_count += 1
            continue
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
    if not annotated_frames:
            return False
    images = [Image.open(f).convert("RGB") for f in annotated_frames]
    images[0].save(
        output_gif_path,
        save_all=True,
        append_images=images[1:],
        duration=100,  # ms per frame (adjust as needed)
        loop=0
    )
    return True