# leaf_detector.py
import torch
import cv2

class LeafDetector:
    def __init__(self, model_path=None):
        """
        If a custom model_path is provided, load it.
        Otherwise, load the default YOLOv5s model.
        """
        if model_path:
            # Load a custom fine-tuned model for leaf detection.
            self.model = torch.hub.load('ultralytics/yolov5', 'custom', path=model_path, force_reload=True)
        else:
            # Load a pre-trained YOLOv5s model.
            self.model = torch.hub.load('ultralytics/yolov5', 'yolov5s', pretrained=True)
    
    def detect(self, image):
        results = self.model(image)  # Run detection
        detections = []

        for det in results.xyxy[0]:  # Extract detections
            x1, y1, x2, y2, conf, cls = det.tolist()
            
            # Apply confidence and IoU threshold manually
            if conf >= 0.4:  # Confidence threshold
                bbox = [int(x1), int(y1), int(x2 - x1), int(y2 - y1)]
                detections.append({
                    'bbox': bbox,
                    'confidence': conf,
                    'label': results.names[int(cls)]  # Get class label from model
                })

        return detections


def get_leaf_detector(model_path=None):
    return LeafDetector(model_path)
