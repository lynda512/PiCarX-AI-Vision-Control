from .camera_interface import CameraInterface
from .preprocessing import preprocess_image
from .detection import CheckpointDetector, ObjectDetector

class VisionSystem:
    """Top-level Vision controller that integrates capture and detection."""

    def __init__(self):
        self.camera = CameraInterface()
        self.checkpoint_detector = CheckpointDetector()
        self.object_detector = ObjectDetector()

    def get_prediction(self):
        """Acquire image, preprocess, and run detection."""
        frame = self.camera.get_image()
        if frame is None:
            return {"status": "no_frame"}

        processed = preprocess_image(frame)
        checkpoints = self.checkpoint_detector.detect(processed)
        objects = self.object_detector.detect(processed)

        return {
            "checkpoints": checkpoints,
            "objects": objects,
        }

    def shutdown(self):
        """Gracefully release hardware."""
        self.camera.release()
