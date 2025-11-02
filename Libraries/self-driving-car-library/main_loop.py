import cv2
import numpy as np
from camera import Camera
from picarx import Picarx
from pygame import time
from display import Display
from ultralytics import YOLO
from object_detection import ObjectDetection

WIDTH = 640
HEIGHT = 480

Y = HEIGHT - 10
REGION_HEIGHT = 150
CENTER = WIDTH // 2

FPS = 30

MAX_STEERING = 35
STEERING_MULTIPLIER = 40
MAX_ERROR = WIDTH // 2


class PID:
    """Simple PID controller for steering correction.

    The PID controller computes a control output from the current error and elapsed time (dt)
    using proportional, integral, and derivative gains.

    Attributes:
        kp (float): Proportional gain. Scales the current error.
        ki (float): Integral gain. Scales the accumulated error to remove steady-state offsets.
        kd (float): Derivative gain. Scales the rate of change of the error for damping/predictive action.
        prev_error (float): Last error value used to compute the derivative term.
        integral (float): Accumulated integral of past errors.

    Notes:
        - The integral term is clamped to [-100, 100] to mitigate integral wind-up.
        - If dt <= 0, the derivative term is treated as zero to avoid division by zero.
        - The controller returns a raw output that the caller should scale/clip to actuator ranges
          (for example converting to servo angle or motor command).
    """
    def __init__(self, kp, ki, kd):
        """Initialize the PID controller.

        Args:
            kp (float): Proportional gain.
            ki (float): Integral gain.
            kd (float): Derivative gain.
        """
        self.kp = kp
        self.ki = ki
        self.kd = kd
        self.prev_error = 0
        self.integral = 0

    def compute(self, error, dt):
        """Compute the PID output for a given error and timestep.

        Args:
            error (float): Current error (e.g., target position - current position).
            dt (float): Time elapsed since last compute call in seconds.

        Returns:
            float: The PID controller output (P + I + D).

        Behavior details:
            - Updates the integral by adding error * dt and clamps it to [-100, 100].
            - Computes derivative as (error - prev_error) / dt when dt > 0.
            - Updates prev_error with the current error for the next iteration.
        """
        self.integral += error * dt
        # Optional: Clamp the integral to avoid wind-up
        self.integral = max(min(self.integral, 100), -100)

        derivative = (error - self.prev_error) / dt if dt > 0 else 0

        output = (
                self.kp * error +
                self.ki * self.integral +
                self.kd * derivative
        )

        self.prev_error = error
        return output


def process_frame(frame):
    """Detect a horizontal line in the bottom region of the frame and compute lateral error.

    Args:
        frame (np.ndarray or None): Input image (expected RGB) or None.

    Returns:
        tuple:
            error (int or None): Signed pixel error = CENTER - line_center.
                Positive -> line is left of image center, Negative -> line is right of center.
                None if no line was detected or input frame was invalid.
            frame (np.ndarray or None): The original frame passed in (unchanged).

    Behavior:
        - Converts frame to grayscale and extracts a horizontal region near the bottom (Y:Y+REGION_HEIGHT).
        - Applies Gaussian blur and Canny edge detection.
        - Finds edge column indices; if at least two columns present, computes line_center as midpoint
          between min and max edge column and returns CENTER - line_center as the error.
        - If frame is None or insufficient edges are found, returns (None, frame).
    """
    if frame is None:
        print("Warning")
        return None, frame

    # Convert to grayscale (frame expected in RGB)
    gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)

    # Region of interest near the bottom of the image
    region = gray[Y:Y + REGION_HEIGHT, :]

    # Reduce noise before edge detection
    blurred = cv2.GaussianBlur(region, (5, 5), 0)

    # Canny edge detection
    edges = cv2.Canny(blurred, 50, 150)

    # Get column indices where edges were detected
    edge_indices = np.where(edges > 0)[1]

    if len(edge_indices) >= 2:
        # Compute center of detected line within the ROI (column index)
        line_center = (np.min(edge_indices) + np.max(edge_indices)) // 2
        print(f"line_center: {line_center}")

        # Compute signed error relative to the image CENTER
        error = CENTER - line_center
        print(f"error: {error}")

        return error, frame
    else:
        return None, frame


pid = PID(kp=0.9, ki=0, kd=0)

running = True

px = Picarx()
clock = time.Clock()

camera = Camera(
    size=(640, 480),  # Resolution (width, height)
    vflip=True,  # Vertical flip
    hflip=True  # Horizontal flip
)
camera.start()
camera.show_fps(False)



object_detection = ObjectDetection(
    camera=camera,
    model_filename='my_yolo.pt',
    model_image_size=(224, 224),
    is_image_thread=True
)

display = Display(object_detection)
display.show(
    local=False,  # Show in local window
    web=True,  # Enable web streaming
    port=9000  # Port for web streaming
)

object_detection.start()

timer = 0
frame = None
dt = 0
stopped = False
parked = False
while running:

    if timer > 10:



        if 0 in object_detection.detected_classes:
            px.forward(0)
            if not parked:
                print('PARKING')
                parked = True
        elif 1 in object_detection.detected_classes:
            px.forward(0)
            if not stopped:
                print('STOPPING')
                stopped = True
        else:
            stopped = False
            parked = False

            frame = camera.get_image()
            error, processed_frame = process_frame(frame)

            if error is not None:
                px.forward(0.1)
                raw_steering = pid.compute(error, dt)
                print(f"raw_steering: {raw_steering}")
                scaled_steering = np.clip((raw_steering / MAX_ERROR) * STEERING_MULTIPLIER, -MAX_STEERING, MAX_STEERING)
                px.set_dir_servo_angle(-scaled_steering)
                print(f"scaled_steering: {scaled_steering}")
            else:
                print("Line not detected")
                px.set_dir_servo_angle(0)
                px.forward(0)





    timer += 1

    dt = clock.tick(FPS) / 1000
