"""
Core camera functionality for the RoboEye library
"""

import os
import time
import threading
import cv2
import numpy as np

from ultralytics import YOLO


class ObjectDetection:

    def __init__(self, camera, model_filename, model_image_size=(224, 224), is_image_thread=False):

        self.camera = camera
        self.is_running = False
        self.object_detection_thread = None
        self.model = None
        self.model_filename = model_filename
        self.model_image_size = model_image_size
        self.is_image_thread = is_image_thread

        # Frame storage - accessible from outside the class
        self.detected_objects = []
        self.detected_classes = {}
        self.current_frame = None

    def start(self):
        self.object_detection_thread = threading.Thread(target=self._object_detection_loop, daemon=True)
        self.object_detection_thread.start()

        # Wait for camera to start
        start_time = time.time()
        while not self.is_running and time.time() - start_time < 5:
            time.sleep(0.1)

        if not self.is_running:
            raise RuntimeError("Failed to start object detection")


    def stop(self):
        if not self.is_running:
            return

        self.is_running = False
        if self.object_detection_thread:
            self.object_detection_thread.join(timeout=3)
            self.object_detection_thread = None

    def _object_detection_loop(self):
        try:

            print("Loading YOLO model...")
            self.model = YOLO(self.model_filename)
            print(f"Model classes: {self.model.names}")
            print("Model loaded successfully!")

            self.is_running = True

            while self.is_running:
                frame = self.camera.get_image()

                if frame is not None:
                    detections = self.detect_objects(frame)
                    detected_objects = []
                    detected_classes = set()
                    if detections:
                        print(f"Objects detected: {len(detections)}")
                        for i, detection in enumerate(detections):
                            confidence = detection['confidence']
                            object_class = detection['class']
                            detected_classes.add(object_class)
                            bbox = detection['bbox']
                            detected_objects.append((i, object_class, confidence, bbox))

                    self.detected_objects = detected_objects
                    self.detected_classes = detected_classes
                    print(self.detected_classes)
                    if self.is_image_thread:
                        self.update_current_frame(frame)


        except Exception as e:
            print(f"Object detection error: {e}")
            self.is_running = False

    def detect_objects(self, frame):
        resized_frame = cv2.resize(frame, (224, 224))

        results = self.model(resized_frame, verbose=False, conf=0.8)

        detections = []
        for result in results:
            boxes = result.boxes
            if boxes is not None:
                for box in boxes:
                    class_name = box.cls.cpu().numpy()[0].astype(np.int16)

                    x1, y1, x2, y2 = box.xyxy[0].cpu().numpy()
                    confidence = box.conf[0].cpu().numpy()

                    # Map coordinates back to original 640x480 frame
                    orig_x1 = int(x1 * 640 / self.model_image_size[0])
                    orig_y1 = int(y1 * 480 / self.model_image_size[1])
                    orig_x2 = int(x2 * 640 / self.model_image_size[0])
                    orig_y2 = int(y2 * 480 / self.model_image_size[1])

                    detections.append({
                        'bbox': (orig_x1, orig_y1, orig_x2, orig_y2),
                        'confidence': confidence,
                        'class': class_name
                    })

        return detections

    def update_current_frame(self, frame, color=(0, 255, 0), thickness=2):
        if frame is not None and self.detected_objects:

            for detected_object in self.detected_objects:
                i, object_class, confidence, bbox = detected_object
                x1, y1, x2, y2 = bbox
                cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), color, thickness)
                cv2.putText(
                    frame,
                    f"C: {confidence:.2f}",
                    (int(x2), int(y1)),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.4,
                    color,
                    1,
                    cv2.LINE_AA
                )

        self.current_frame = frame
