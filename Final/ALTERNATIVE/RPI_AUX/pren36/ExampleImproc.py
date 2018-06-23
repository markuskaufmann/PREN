import time
import cv2
import numpy as np
from picamera import PiCamera
from picamera.array import PiRGBArray


class ImageProcessorPiCamera:
    IMAGESIZE_X = 640
    IMAGESIZE_Y = 480
    TARGETRANGE = 10
    TARGETOFFSET = 0

    stopped = False

    def stop(self):
        self.stopped = True

    def start_capture(self):
        camera = PiCamera()
        camera.resolution = (ImageProcessorPiCamera.IMAGESIZE_X, ImageProcessorPiCamera.IMAGESIZE_Y)
        camera.framerate = 32
        camera.video_stabilization = True
        raw_capture = PiRGBArray(camera, size=(ImageProcessorPiCamera.IMAGESIZE_X, ImageProcessorPiCamera.IMAGESIZE_Y))
        stream = camera.capture_continuous(raw_capture, format="bgr", use_video_port=True)
        time.sleep(0.1)
        for frame in stream:
            if self.stopped:
                stream.close()
                raw_capture.close()
                camera.close()
                cv2.destroyAllWindows()
                return
            image = frame.array
            raw_capture.truncate(0)
            operate = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            operate = cv2.GaussianBlur(operate, (3, 3), 0)
            _, operate = cv2.threshold(operate, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
            _, contours, _ = cv2.findContours(operate.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
            contours = sorted(contours, key=cv2.contourArea, reverse=True)[:9]
            center_array = []
            square_array = []

            for c in contours:
                peri = cv2.arcLength(c, True)
                approx = cv2.approxPolyDP(c, 0.02 * peri, True)
                if len(approx) == 4:
                    (x, y, w, h,) = cv2.boundingRect(approx)
                    ratio = w / float(h)
                    if 0.9 <= ratio <= 1.1:
                        square_array.append(c)
                        c_x, c_y = self.get_center(c)
                        center_array.append(np.array((c_x, c_y)))

            c_x, c_y = self.find_target(center_array)

            if not c_x == -1:
                print("Target found at: " + str(c_x) + "," + str(c_y))
                cv2.drawMarker(image, (c_x, c_y), (0, 255, 0), cv2.MARKER_CROSS, 15, cv2.LINE_AA)
                if self.check_x(c_x):
                    print("Drop location: " + str(c_x) + "," + str(c_y))
                    cv2.drawMarker(image, (c_x, c_y), (0, 0, 255), cv2.MARKER_TRIANGLE_DOWN, 15, cv2.LINE_AA)
            cv2.imshow("image", image)
            cv2.waitKey(1)

    def get_center(self, contour):
        moments = cv2.moments(contour)
        center_x = int(moments["m10"] / moments["m00"])
        center_y = int(moments["m01"] / moments["m00"])
        return center_x, center_y

    def check_x(self, loc_x) -> bool:
        upper = ImageProcessorPiCamera.IMAGESIZE_X / 2 + ImageProcessorPiCamera.TARGETRANGE + \
                ImageProcessorPiCamera.TARGETOFFSET
        lower = ImageProcessorPiCamera.IMAGESIZE_X / 2 - ImageProcessorPiCamera.TARGETRANGE + \
                ImageProcessorPiCamera.TARGETOFFSET
        if lower <= loc_x <= upper:
            return True
        else:
            return False

    def find_target(self, centers_array):
        for i, v in enumerate(centers_array[0:-2]):
            center_matches = 0
            for w in centers_array[i + 1:]:
                diff = np.abs(v - w)
                if diff[0] <= 10 and diff[1] <= 10:
                    center_matches += 1
                    if center_matches >= 2:
                        return v[0], v[1]
        return -1, -1


if __name__ == '__main__':
    improcpicam = None
    try:
        improcpicam = ImageProcessorPiCamera()
        improcpicam.start_capture()
    except KeyboardInterrupt:
        improcpicam.stop()
