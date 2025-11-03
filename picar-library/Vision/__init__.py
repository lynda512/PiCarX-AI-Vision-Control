"""
Vision Module for PiCarX-AI-Vision-Control

Provides computer vision capabilities including:
- Camera interface (image capture)
- Preprocessing (filtering, normalization)
- Detection (checkpoints, letters, obstacles)
- Tracking (object motion tracking)
- VisionSystem (high-level interface for Controller)

Usage Example:
---------------
from Vision import VisionSystem

vision = VisionSystem()
data = vision.get_prediction()
print(data)
vision.shutdown()
"""

from .vision_system import VisionSystem
from .camera_interface import CameraInterface
from .detection import CheckpointDetector, ObjectDetector
from .tracking import ObjectTracker
from .preprocessing import preprocess_image, enhance_contrast

__all__ = [
    "VisionSystem",
    "CameraInterface",
    "CheckpointDetector",
    "ObjectDetector",
    "ObjectTracker",
    "preprocess_image",
    "enhance_contrast",
]
