from typing import Any

from hardware.movement import Movement
from status.action import Action
from status.prediction import Prediction


class Navigation:
    """High level class responsible for the movement of the car"""

    def __init__(self):
        self.movement = Movement()

    def decide_action(self, prediction: Prediction) -> Action:
        """
            Decides action according to the given prediction

        Args:
            prediction: Prediction object containing frame and detected checkpoints.

        Returns:
            action: Decided Action
        """

        # TODO implement how to decide action according to prediction here
        action = Action.FORWARD

        return action

    def perform_action(self, action: Action, prediction: Prediction):
        """
            Performs action according to the predicted action

            Args:
                action: Action to perform
                prediction: Prediction object containing frame and detected checkpoints
        """
        if action == Action.FORWARD:
            self.forward()
        elif action == Action.BACKWARD:
            self.backward()
        elif action == Action.LEFT:
            angle = self.angle_retrieval(action, prediction)
            self.turn(Action.LEFT, angle)
        elif action == Action.RIGHT:
            angle = self.angle_retrieval(action, prediction)
            self.turn(Action.RIGHT, angle)
        self.stop()

    def angle_retrieval(self, action: Action, prediction: Prediction) -> int:
        """
            Handler for steering angle prediction according to the given action

        Args:
            action: Action to perform
            prediction: Prediction object containing frame and detected checkpoints.

        Returns:
            angle: Angle in degrees to turn
        """
        angle = 10
        # TODO implement how to handle angle creation here
        return angle

    def stop(self):
        """Stops the car"""
        self.movement.stop()

    def forward(self):
        """Moves the car forward"""
        self.movement.forward()

    def backward(self):
        """Moves the car backward"""
        self.movement.backward()

    def turn(self, direction, angle):
        """
            Turns the car in the specified direction by the given angle

        Args:
            direction (Action): Direction to turn ('LEFT' or 'RIGHT')
            angle (int): Angle in degrees to turn
        """
        self.movement.turn(direction, angle)