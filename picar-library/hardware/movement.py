from picarx import Picarx
from status.action import Action


class Movement:
    """Low level class responsible for the movement of the car."""
    def __init__(self):
        self.picar = Picarx()

    def stop(self):
        """Stops the car"""
        print("Stopping the car")
        self.picar.stop()


    def forward(self):
        """Moves the car forward"""
        print("Moving forward")
        self.picar.set_dir_servo_angle(0)
        self.picar.forward(80)

    def backward(self):
        """Moves the car backward"""
        print("Moving backward")
        self.picar.set_dir_servo_angle(0)
        self.picar.backward(80)

    def turn(self, direction, angle):
        """Turns the car in the specified direction by the given angle"""
        print(f"Turning {direction} by {angle} degrees")
        if direction == Action.LEFT:
            self.picar.set_dir_servo_angle(-35)
            self.picar.forward(80)
        elif direction == Action.RIGHT:
            self.picar.set_dir_servo_angle(35)
            self.picar.forward(80)