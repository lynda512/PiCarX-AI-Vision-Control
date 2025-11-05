from hardware.camera import Camera

class CameraInterface:
    """Interface between vision module and hardware.Camera."""

    def __init__(self, resolution=(640, 480)):
        self.camera = Camera(resolution=resolution)

    def get_image(self):
        """Return latest image frame from camera."""
        return self.camera.capture_frame()

    def get_video(self):
        """Return video stream from camera."""
        return self.camera.capture_video()

    def release(self):
        """Release camera hardware."""
        self.camera.release()
