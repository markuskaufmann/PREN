from __future__ import print_function
import cv2
import numpy as np
from imutils.video import FPS
from imutils.video import WebcamVideoStream

IMAGESIZE_X = 640
IMAGESIZE_Y = 480
TARGETRANGE = 15
TARGETOFFSET = 0


vs = WebcamVideoStream(src=0).start()

fps = FPS().start()


def get_center(contour):
    moments = cv2.moments(contour)
    center_x = int(moments["m10"] / moments["m00"])
    center_y = int(moments["m01"] / moments["m00"])
    return center_x, center_y


def check_x(loc_x) -> bool:
    upper = IMAGESIZE_X/2 + TARGETRANGE + TARGETOFFSET
    lower = IMAGESIZE_X/2 - TARGETRANGE + TARGETOFFSET
    if lower <= loc_x <= upper:
        return True
    else:
        return False


def find_target(centers_array):
    for i, v in enumerate(centers_array[0:-2]):
        center_matches = 0
        for w in centers_array[i + 1:]:
            diff = np.abs(v - w)
            if diff[0] <= 10 and diff[1] <= 10:
                center_matches += 1
                if center_matches >= 2:
                    return v[0], v[1]
    return -1, -1


while True:
    image = vs.read()
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
                cX, cY = get_center(c)
                center_array.append(np.array((cX, cY)))
    cX, cY = find_target(center_array)
    if not cX == -1:
        print("Target found at: " + str(cX) + "," + str(cY))
        cv2.drawMarker(image, (cX, cY), (0, 255, 0), cv2.MARKER_CROSS, 15, cv2.LINE_AA)
        if check_x(cX):
            print("Drop location : " + str(cX) + "," + str(cY))
            cv2.drawMarker(image, (cX, cY), (0, 0, 255), cv2.MARKER_TRIANGLE_DOWN,15, cv2.LINE_AA)

    cv2.imshow("image", image)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    fps.update()

fps.stop()
print("[INFO] elapsed time: {:.2f}".format(fps.elapsed()))
print("[INFO] approx. FPS: {:.2f}".format(fps.fps()))

cv2.destroyAllWindows()
vs.stop()
