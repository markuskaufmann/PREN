from threading import Thread

from picamera import PiCamera
from picamera.array import PiRGBArray


class PiVideoStream:
    def __init__(self, resolution, framerate):
        self.camera = PiCamera()
        self.camera.resolution = resolution
        self.camera.framerate = framerate
        self.camera.video_stabilization = True
        self.raw_capture = PiRGBArray(self.camera, size=resolution)
        self.stream = self.camera.capture_continuous(self.raw_capture, format="bgr", use_video_port=True)
        self.frame = None
        self.stopped = False

    def start(self):
        t = Thread(target=self.update, name="ImageProcessor_Stream")
        t.start()

    def update(self):
        for f in self.stream:
            self.frame = f.array
            self.raw_capture.truncate(0)
            if self.stopped:
                self.stream.close()
                self.raw_capture.close()
                self.camera.close()
                return

    def read(self):
        return self.frame

    def stop(self):
        self.stopped = True
