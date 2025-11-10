class Prediction:
    """Class representing a frame and the correspondant checkpoints obtained by the vision system."""
    def __init__(self, frame, checkpoints):
        self.frame = frame
        self.checkpoints = checkpoints

    def get_frame(self):
        return self.frame
    
    def get_checkpoints(self):
        return self.checkpoints