from Hardware.camera import Camera

class CameraInterface:
    """Interface between Vision module and Hardware.Camera."""

    def __init__(self, resolution=(640, 480)):
        self.camera = Camera(resolution=resolution)

    def get_image(self):
        """Return latest image frame from camera."""
        return self.camera.capture_frame()

    def release(self):
        """Release camera hardware."""
        self.camera.release()
