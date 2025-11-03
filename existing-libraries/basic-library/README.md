# RoboEye Library

RoboEye is a Python library for camera management, real-time object detection using YOLO, and displaying video streams locally or via web streaming.

---

## object_detection.py

This module implements real-time object detection functionality using a YOLO model.

- **Class `ObjectDetection`**

  - Connects to a camera instance.
  - Loads a YOLO object detection model (configurable model file and input image size).
  - Runs object detection asynchronously in a separate thread.
  - Provides detected objects with bounding boxes, confidence scores, and class IDs.
  - Can update and annotate the current camera frame with detection bounding boxes and confidence.

- **Key Methods**

  - `start()`: Starts the detection thread and begins detection on camera frames.
  - `stop()`: Stops detection and joins the thread.
  - `_object_detection_loop()`: Internal loop loading the model and processing frames.
  - `detect_objects(frame)`: Runs detection on a given frame.
  - `update_current_frame(frame)`: Annotates detections on the frame.

---

## camera.py

This module handles camera operations using the Picamera2 library with libcamera.

- **Class `Camera`**

  - Configures and starts the camera with specified resolution and flips.
  - Runs capture loop in a separate thread for continuous frame acquisition.
  - Provides frame access and optional drawing of FPS and detection overlays.
  - Supports taking photos and saving them to disk.
  - Allows setting and getting camera hardware controls.

- **Key Methods**

  - `start()`: Starts the camera capture thread.
  - `stop()`: Stops the camera gracefully.
  - `_camera_loop()`: Runs the capture and frame processing.
  - `get_image()`: Returns the latest captured frame.
  - `take_photo(filename, path)`: Saves the current frame as a photo.
  - Methods for FPS and detection overlay configuration.

---

## display.py

This module manages display of camera frames locally and via web streaming.

- **Class `Display`**

  - Takes a `Camera` instance to fetch frames.
  - Supports local display in an OpenCV window with FPS and detection overlays.
  - Supports web streaming on a configurable port.
  - Runs display and streaming in separate threads.

- **Key Methods**

  - `show_local(enable, window_name)`: Enable or disable local window display.
  - `show_web(enable, port)`: Enable or disable web streaming.
  - `show(local, web, port)`: Enable both local display and web streaming.
  - `close()`: Closes all displays and streaming servers gracefully.

---
### `__init__.py`
This file serves as the **main package initializer** for the `RoboEye` library.

- **Purpose:**
    - It defines which components are directly available when importing from the package (e.g., `from RoboEye import Camera`).
    - It provides a brief docstring description of the library.
- **Key Contents:**
    - Imports and exposes the `Camera` and `Display` classes as the public interface of the library.
---

### `streaming.py`
This module implements the **web video streaming server** using the Flask framework and OpenCV.

- **Key Functions:**
    - `create_streaming_server(camera)`: Creates a **Flask application instance** that serves the camera's current frame.
        - The `/video_feed` route provides a **Motion JPEG (MJPEG) stream** using a generator function.
        - The `/still.jpg` route provides a single, non-streaming **still JPEG image**.
    - `generate_frames()`: A generator that fetches the latest frame, encodes it to JPEG, and yields it with the required headers for the video stream.
    - `start_streaming_server(app, port=9000)`: Starts the created Flask app on the specified host and port.
---
### `utils.py`
This module provides **utility functions** for system interaction, environment checks, and network information.

- **Key Functions:**
    - `run_command(cmd)`: Runs a specified shell command and returns the **exit status** and the **decoded output**.
    - `get_ip_addresses()`: Retrieves and returns the IP addresses for the `wlan0` (Wi-Fi) and `eth0` (Ethernet) network interfaces.
    - `check_machine_type()`: Determines the system's architecture (e.g., `armv7l` or `aarch64`) and returns the **bit size** and the **machine type string**.

---

## 💡 Example Scripts

These files showcase how to use the RoboEye library for various robotic tasks.

### `run_camera.py`
This script demonstrates basic camera setup, audio functionality, and **scheduled photo capture**.

- **Features:**
    - Initializes the `Picarx` robot and audio components (`pygame.mixer`, `robot_hat.Music`).
    - Starts the `Camera` and `Display` (local and web streaming on port 9000).
    - Periodically captures and saves photos (every 30 frames) to a dataset, breaking the loop after 100 images.
    - Plays background music and a sound effect when a photo is taken.

### `pid.py`
This script demonstrates a basic **line-following implementation** using a PID controller and camera input.

- **Class `PIDController`:** Implements the PID control algorithm with Proportional ($K_p=0.5$), Integral ($K_i=0.1$), and Derivative ($K_d=0$) gains. It includes integral clamping to prevent wind-up.
- **Function `update_steering`:** Calculates the steering angle by defining the error as the difference between the average pixel brightness of the left and right halves of a specific image row (`photo[240]`). The PID output is then clamped to the steering limits ($\mathbf{-35}$ to $\mathbf{35}$).
- **Control Loop:** Runs the PicarX forward at a speed of 50 and continuously adjusts the steering servo angle based on the line detection via the PID output.

### `run_model.py`
This script implements **real-time object detection** using a pre-trained YOLO model (e.g., `yolov8n.pt`).

- **Function `detect_objects(model, frame)`:**
    - Resizes the camera frame to the model's input size (e.g., 416x416).
    - Runs YOLO inference and maps the detected bounding box coordinates back to the original 640x480 resolution.
    - Returns a list of detections with bounding box coordinates, center points, and confidence scores.
- **Control Loop:**
    - Loads the YOLO model and starts the camera with the detection overlay enabled.
    - Periodically gets a frame, runs `detect_objects`, and updates the camera's internal detections (`camera.update_detections`) so bounding boxes are drawn onto the live stream.
