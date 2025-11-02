"""
run_model.py
------------
Main control script for the RoboEye + PicarX system.

This program integrates:
- A PicarX robot (robot car with motors and servos)
- A RoboEye camera for real-time video capture
- YOLO object detection for identifying objects in view
- Flask-based web streaming via Display
- Optional on-screen overlays for detections

It continuously captures frames, runs YOLO inference, and 
updates the display with bounding boxes and object info.
"""

# --- Imports ----------------------------------------------------------------

from picarx import Picarx                # Controls the physical robot (motors, servos)
from camera import Camera                # Handles video capture and frame management
from display import Display              # Provides both local and web-based video display
from pygame import time                  # Used for frame rate timing
from pygame import mixer                 # For potential sound effects (not used here)
from robot_hat import PWM, Music, Buzzer, set_volume, enable_speaker, disable_speaker
                                         # Hardware control and audio (speaker, PWM, etc.)
import os
import numpy as np
import cv2                               # For image resizing and frame encoding
from ultralytics import YOLO             # YOLOv8 object detection model

# --- Constants ---------------------------------------------------------------

# These might control servo steering angles for PicarX movement
STEERING_MIN = -35
STEERING_MAX = 35


# --- Object Detection Function ----------------------------------------------

def detect_objects(model, frame):
    """
    Detect objects in a given camera frame using a YOLO model.

    Args:
        model: A YOLOv8 model loaded via ultralytics.YOLO
        frame: The current image frame from the camera (NumPy array, 640x480)

    Returns:
        detections (list of dict): Each entry has:
            {
                'bbox': (x1, y1, x2, y2),     # bounding box coordinates in original image space
                'center': (cx, cy),           # object center point
                'confidence': float            # detection confidence (0.0–1.0)
            }
    """
    # Resize frame to YOLO input size
    resized_frame = cv2.resize(frame, (416, 416))
    
    # Run YOLO inference (silent mode, confidence threshold = 0.7)
    results = model(resized_frame, verbose=False, conf=0.7)
    
    detections = []
    for result in results:
        boxes = result.boxes
        if boxes is not None:
            for box in boxes:
                # Extract bounding box coordinates from YOLO output (in 416x416 space)
                x1, y1, x2, y2 = box.xyxy[0].cpu().numpy()
                confidence = box.conf[0].cpu().numpy()
                
                # Convert coordinates back to original camera resolution (640x480)
                orig_x1 = int(x1 * 640 / 416)
                orig_y1 = int(y1 * 480 / 416)
                orig_x2 = int(x2 * 640 / 416)
                orig_y2 = int(y2 * 480 / 416)
                
                # Calculate center point
                center_x = (orig_x1 + orig_x2) // 2
                center_y = (orig_y1 + orig_y2) // 2
                
                detections.append({
                    'bbox': (orig_x1, orig_y1, orig_x2, orig_y2),
                    'center': (center_x, center_y),
                    'confidence': confidence
                })
    
    return detections


# --- Main Control Loop ------------------------------------------------------

def main():
    """
    Main loop for running YOLO detection on the RoboEye camera feed
    and streaming it through the Display interface.
    """

    # Initialize robot car and frame timing
    px = Picarx()
    clock = time.Clock()
    FPS = 30  # Desired frame rate

    # Load YOLOv8 model (using the small 'n' version)
    print("Loading YOLO model...")
    model = YOLO('yolov8n.pt')
    print("Model loaded successfully!")
    
    timer = 0  # Used to limit how often detections run

    try:
        # Initialize and start the RoboEye camera
        camera = Camera(
            size=(640, 480),
            vflip=True,    # Vertical flip for correct orientation
            hflip=True     # Horizontal flip (mirror)
        )

        print("Starting camera...")
        camera.start()                     # Begin capturing frames
        camera.show_fps(True)              # Display FPS overlay
        camera.enable_detection_overlay(confidence=True)  # Enable bounding box overlay

        # Initialize the display system (local + web)
        display = Display(camera)
        display.show(
            local=True,                    # Show live stream on the local display
            web=True,                      # Enable web streaming
            port=9000                      # Stream available at http://<ip>:9000
        )

        # Reset camera pan/tilt servos
        px.set_cam_tilt_angle(0)
        px.set_cam_pan_angle(0)
        
        # --- Main Loop ---
        while True:
            if timer > 30:  # Run detection every ~1 second (30 frames @ 30fps)
                photo = camera.get_image()
                
                if photo is not None:
                    # Run YOLO detection
                    detections = detect_objects(model, photo)
                    camera_detections = []

                    if detections:
                        print(f"Objects detected: {len(detections)}")
                        for i, detection in enumerate(detections):
                            center_x, center_y = detection['center']
                            confidence = detection['confidence']
                            x1, y1, x2, y2 = detection['bbox']

                            # Store detections for overlay display
                            camera_detections.append((x1, y1, x2, y2, confidence))

                            print(f"  Object {i+1}: Center=({center_x}, {center_y}), Confidence={confidence:.2f}")

                        # Update the camera display with bounding boxes
                        camera.update_detections(camera_detections)
                timer = 0
            else:
                timer += 1  # Wait before next detection
            
            # Maintain stable frame rate
            clock.tick(FPS)

    except KeyboardInterrupt:
        # Graceful shutdown if user presses Ctrl+C
        print("\nExiting...")

    except Exception as e:
        # Catch and print any unexpected runtime error
        print(f"Error: {e}")

    finally:
        # Ensure hardware cleanup and resource release
        print("Cleaning up...")
        disable_speaker()
        display.close()
        camera.stop()


# --- Entry Point -------------------------------------------------------------

if __name__ == "__main__":
    # When the script is run directly, start the system
    main()
