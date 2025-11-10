from detection import CheckpointDetector
from status.prediction import Prediction


class VisionSystem:
    """Top-level vision controller that integrates capture and detection."""

    def __init__(self):
        self.checkpoint_detector = CheckpointDetector()

    def make_prediction(self, frame):
        """
        Process the image frame and feed it to the model.

        Args:
            frame: The raw image frame from the camera.

        Returns:
            prediction: Prediction object containing frame and detected checkpoints.
        """
        if frame is None:
            return {"status": "no_frame"} #TODO implement better handler

        # TODO passes the frame through preprocessing steps and feed the result to the model
        processed = self.preprocess_image(frame)
        checkpoints = self.checkpoint_detector.detect(processed)

        prediction = Prediction(frame, checkpoints)
        return prediction

    def preprocess_image(self, frame):
        """
        Preprocess the image frame for model input.

        Args:
            frame: The raw image frame from the camera.

        Returns:
            processed_frame: The preprocessed image frame.
        """
        processed_frame = frame
        return processed_frame
