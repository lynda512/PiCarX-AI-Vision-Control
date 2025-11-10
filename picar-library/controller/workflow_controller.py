from controller.camera_controller import CameraController
from controller.navigation_controller import NavigationController


class WorkflowController:
    """Controller managing communication between CameraController and NavigationController."""
    def __init__(self):
        self.camera_controller = CameraController()
        self.navigation_controller = NavigationController()

    def start_workflow(self):
        """Start the workflow by getting prediction from CameraController and passing it to NavigationController."""
        prediction = self.camera_controller.make_prediction()

        self.navigation_controller.perform_action(prediction)