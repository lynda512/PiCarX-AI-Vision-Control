from navigation.navigation import Navigation
from status.action import Action
from status.prediction import Prediction


class NavigationController:
    """Controller for managing navigation"""
    def __init__(self):
        self.navigation = Navigation()

    def perform_action(self, prediction: Prediction):
        """ Takes a prediction and passes it to the navigation system to perform the correspondent action
        Args:
            prediction: Prediction object containing frame and detected checkpoints.
        """
        action = self.navigation.decide_action(prediction)
        self.navigation.perform_action(action, prediction)