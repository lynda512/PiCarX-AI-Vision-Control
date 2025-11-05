from status.action import Action
from vision.vision_system import VisionSystem

class CameraController:
    """Controller for managing camera in PiCarX-AI-vision-Control."""
    def __init__(self):
        self.vision = VisionSystem()

    def predict_action(self):
        """
        Make driving decisions based on vision model predictions

        Returns:
            Action: The action decided based on vision prediction.
        """
        prediction = self.vision.get_prediction()

        # TODO Decision-making logic can be implemented here
        # prediction value converted into action
        return Action