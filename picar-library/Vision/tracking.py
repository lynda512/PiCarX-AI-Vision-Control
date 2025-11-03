import cv2

class ObjectTracker:
    """Track object positions over frames."""

    def __init__(self):
        self.tracker = cv2.legacy.TrackerKCF_create()

    def init(self, frame, bbox):
        """Initialize tracker with bounding box."""
        self.tracker.init(frame, bbox)

    def update(self, frame):
        """Update tracked position and return bbox."""
        success, bbox = self.tracker.update(frame)
        return success, bbox
