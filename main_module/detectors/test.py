import os
import cv2
from leaf_detector import get_leaf_detector

def main():
    # Determine the project root
    PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    image_path = os.path.join(PROJECT_ROOT, 'zidane.jpg')
    image = cv2.imread(image_path)
    if image is None:
        print("Image not found:", image_path)
        return

    detector = get_leaf_detector()  # Load YOLOv5 model (default)
    detections = detector.detect(image)
    print("Detections:", detections)
    
    # Draw the detections on the image
    for det in detections:
        x, y, w, h = det['bbox']
        cv2.rectangle(image, (x, y), (x+w, y+h), (0, 255, 0), 2)
        label = f"{det['label']} {det['confidence']:.2f}"
        cv2.putText(image, label, (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
    
    # Save the annotated image to disk
    output_path = os.path.join(PROJECT_ROOT, 'annotated_zidane.jpg')
    cv2.imwrite(output_path, image)
    print(f"Annotated image saved to: {output_path}")

if __name__ == '__main__':
    main()
