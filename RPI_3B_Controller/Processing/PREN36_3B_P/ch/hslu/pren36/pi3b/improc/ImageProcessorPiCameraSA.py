from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import cv2
import numpy


class ImageProcessorPiCameraSA:

    def start_capture(self):
        camera = PiCamera()
        camera.resolution = (640, 480)
        camera.framerate = 32
        camera.video_stabilization = True
        raw_capture = PiRGBArray(camera, size=(640, 480))
        time.sleep(0.1)
        try:
            for frame in camera.capture_continuous(raw_capture, format="bgr", use_video_port=True):
                image = frame.array
                greyed = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
                blurred = cv2.GaussianBlur(greyed, (5, 5), 0)
                edged = cv2.Canny(blurred, 100, 200)
                new_image, contours, hierarchy = cv2.findContours(edged.copy(), cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE)
                self.verify_contours(image, contours)
                raw_capture.truncate(0)
        except KeyboardInterrupt:
            camera.close()
            cv2.destroyAllWindows()

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
                        approximations.append(approximation)
                        lastdimensions.append((w, h))
                        centers.append(numpy.array((cx, cy)))
        cv2.imshow("Image", image)
        cv2.waitKey(1)
