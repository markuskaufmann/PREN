from threading import Thread
from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import cv2
import numpy
from ch.hslu.pren36.pi3b.improc.ImageProcessorEvent import ImageProcessorEvent
from ch.hslu.pren36.pi3b.main.ControllerEvent import ControllerEvent


class ImageProcessorPiCamera:
    proc_conn = None
    t_notify = None
    t_wait = None
    existing = True
    idle = True
    stopped = True
    notify_existing = True
    notify_idle = True
    wait_running = True

    def start_idle(self, conn):
        self.proc_conn = conn
        self.t_wait = Thread(target=self.wait, name="ImageProcessor_Wait")
        self.t_wait.start()
        self.t_notify = Thread(target=self.notify_observers, name="ImageProcessor_Notify")
        self.t_notify.start()
        while self.existing:
            while self.idle:
                time.sleep(0.02)
            self.start_capture()

    def run(self):
        self.stopped = False
        self.idle = False

    def stop(self):
        self.idle = True
        self.stopped = True

    def extinguish(self):
        self.stop()
        self.existing = False

    def send_event(self):
        self.notify_idle = False

    def notify_observers(self):
        while self.notify_existing:
            while self.notify_idle:
                time.sleep(0.02)
            event = ImageProcessorEvent(ImageProcessorEvent.event_args_found)
            self.proc_conn.send(event)
            self.notify_idle = True

    def wait(self):
        while self.wait_running:
            controllerevent = self.proc_conn.recv()
            args = controllerevent.args
            if args == ControllerEvent.event_args_improc_start:
                self.run()
            elif args == ControllerEvent.event_args_main_stop:
                self.stop()

    def start_capture(self):
        camera = PiCamera()
        camera.resolution = (640, 480)
        camera.framerate = 32
        camera.video_stabilization = True
        raw_capture = PiRGBArray(camera, size=(640, 480))
        time.sleep(0.1)
        for frame in camera.capture_continuous(raw_capture, format="bgr", use_video_port=True):
            if self.stopped:
                camera.close()
                cv2.destroyAllWindows()
                return
            image = frame.array
            greyed = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            blurred = cv2.GaussianBlur(greyed, (5, 5), 0)
            edged = cv2.Canny(blurred, 100, 200)
            new_image, contours, hierarchy = cv2.findContours(edged.copy(), cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE)
            self.verify_contours(image, contours)
            raw_capture.truncate(0)

    def verify_contours(self, image, contours):
        centers = []
        approximations = []
        lastdimensions = []
        matches = []
        found = False
        for contour in contours:
            perimeter = cv2.arcLength(contour, True)
            approximation = cv2.approxPolyDP(contour, (0.05 * perimeter), True)
            if len(approximation) == 4:
                (x, y, w, h) = cv2.boundingRect(approximation)
                if h == 0:
                    h = 0.01
                aspectratio = w / float(h)
                if 0.8 <= aspectratio <= 1.2:
                    m = cv2.moments(approximation)
                    m00 = m['m00']
                    if m00 == 0:
                        m00 = 0.05
                    cx = int(m['m10'] / m00)
                    cy = int(m['m01'] / m00)
                    found = False
                    offset = 3
                    for lastdimension in lastdimensions:
                        if (lastdimension[0] + offset) >= w >= (lastdimension[0] - offset):
                            found = True
                            break
                        if (lastdimension[1] + offset) >= h >= (lastdimension[1] - offset):
                            found = True
                            break
                    if not found:
                        temp = 0
                        first_match = True
                        for center in centers:
                            distance = numpy.linalg.norm(numpy.array((cx, cy)) - center)
                            if distance <= 10:
                                if first_match:
                                    matches.clear()
                                    matches.append(approximations[temp])
                                    first_match = False
                                else:
                                    cv2.drawContours(image, [approximation], -1, (0, 255, 0), 4)
                                    cv2.drawContours(image, [matches[0]], -1, (0, 0, 255), 4)
                                    cv2.drawContours(image, [approximations[temp]], -1, (255, 0, 0), 4)
                            temp += 1
                        if len(centers) >= 6:
                            self.send_event()
                        approximations.append(approximation)
                        lastdimensions.append((w, h))
                        centers.append(numpy.array((cx, cy)))
        cv2.imshow("Image", image)
        cv2.waitKey(1)
