import os
from time import strftime, localtime, time

from vilib import Vilib


class Camera:
    """Camera hardware interface."""

    def __init__(self, resolution=(640, 480)):
        self.resolution = resolution
        Vilib.camera_start(vflip=False, hflip=False)
        Vilib.display(local=True, web=True)

    def capture_frame(self):
        """Capture a single frame from the camera."""
        _time = strftime('%Y-%m-%d-%H-%M-%S', localtime(time()))
        name = 'frame_%s' % _time

        path = "./data_samples/images"
        Vilib.take_photo(name, path)
        print('photo save as %s%s.jpg' % (path, name))

    def capture_video(self):
        """Capture a video from the camera."""
        path = "./data_samples/videos/"
        Vilib.rec_video_set["path"] = path

        video_name = strftime("%Y-%m-%d-%H.%M.%S", localtime())
        Vilib.rec_video_set["name"] = f"video_{video_name}"
        # start record
        Vilib.rec_video_run()
        Vilib.rec_video_start()
        print('video recording started: %s%s.h264' % (path, video_name))


    def release(self):
        """Release the camera hardware."""

        # TODO Implement actual release logic
        # self.cap.release()
        pass  # Placeholder for actual implementation