from hardware.camera import Camera
from status.prediction import Prediction
from vision.vision_system import VisionSystem

class CameraController:
    """Controller for managing camera in PiCarX-AI-vision-Control."""
    def __init__(self):
        self.vision = VisionSystem()
        self.camera = Camera()

    def get_camera_image(self):
        """
        Capture a real time image from the camera.

        Returns:
            frame: The captured image frame.
        """
        return self.camera.get_frame()

    def make_prediction(self) -> Prediction:
        """
        Takes a camera image and passes it to the vision system as input to the model.

        Returns:
            prediction: Prediction object containing frame and detected checkpoints.
        """
        frame = self.get_camera_image()

        return self.vision.make_prediction(frame)