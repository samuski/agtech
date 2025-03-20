# annotation.py
import cv2

def annotate_image(image, detections):
    """
    Draw bounding boxes and labels on the image.
    """
    for det in detections:
        x, y, w, h = det['bbox']
        label = det['label']
        confidence = det['confidence']
        cv2.rectangle(image, (x, y), (x+w, y+h), (0, 255, 0), 2)
        text = f"{label}: {confidence:.2f}"
        cv2.putText(image, text, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX,
                    0.5, (0, 255, 0), 2)
    return image
