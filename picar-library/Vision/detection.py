import cv2
import numpy as np

class CheckpointDetector:
    """Detects visual checkpoints or letters on track."""

    def __init__(self, model=None):
        self.model = model  # Optional ML/CNN model for classification

    def detect(self, frame):
        """
        Returns a list of detected checkpoints:
        [ {'label': 'A', 'position': (x, y), 'confidence': 0.9}, ... ]
        """
        detections = []
        # Example: use contours or ArUco markers
        # detections.append({...})
        return detections


class ObjectDetector:
    """Detects obstacles or target objects for stop condition."""

    def __init__(self, model=None):
        self.model = model

    def detect(self, frame):
        """Return list of detected objects with bounding boxes."""
        return []
