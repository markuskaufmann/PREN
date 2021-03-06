import numpy as np
import cv2
import time

cap = cv2.VideoCapture(0)


start_time = time.time()

image_counter = 0

while cap.isOpened():
    loopTime = time.time()
    ret, image = cap.read()
    if not ret:
        break
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    gray = cv2.blur(gray, (3, 3))

    # detect edges in the image
    edged = cv2.Canny(gray, 150, 255)

    # find contours (i.e. the 'outlines') in the image
    new_image, contours, hierarchy = cv2.findContours(edged.copy(), cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE)

    centers = []
    approximations = []
    lastDimensions = []
    matches = []
    found = False
    for contour in contours:
        # approximate the contour
        peri = cv2.arcLength(contour, True)
        approx = cv2.approxPolyDP(contour, 0.02 * peri, True)

        # if the approximated contour has four points its a rectangle
        if len(approx) == 4:
            (x, y, w, h) = cv2.boundingRect(approx)
            if h == 0:
                h = 0.01
            aspect_Ratio = w / float(h)
            if 0.85 <= aspect_Ratio <= 1.15:
                M = cv2.moments(approx)
                m00 = M['m00']
                if m00 == 0:
                    m00 = 0.05
                cx = int(M['m10'] / m00)
                cy = int(M['m01'] / m00)
                found = False
                offset = 3
                for lastDimension in lastDimensions:
                    if (lastDimension[0] + offset) >= w >= (lastDimension[0] - offset):
                        found = True
                        break

                    if (lastDimension[1] + offset) >= h >= (lastDimension[1] - offset):
                        found = True
                        break
                if not found:
                    temp = 0
                    first_match = True
                    for center in centers:
                        distance = np.linalg.norm(np.array((cx, cy)) - center)
                        if distance <= 10:
                            if first_match:
                                matches.clear()
                                matches.append(approximations[temp])
                                first_match = False
                            else:
                                cv2.drawContours(image, [approx], -1, (0, 255, 0), 4)
                                cv2.drawContours(image, [matches[0]], -1, (0, 0, 255), 4)
                                cv2.drawContours(image, [approximations[temp]], -1, (255, 0, 0), 4)
                                image_counter += 1
                        temp += 1
                    approximations.append(approx)
                    lastDimensions.append((w, h))
                    centers.append(np.array((cx, cy)))
    print("LoopTime: " + str(time.time() - loopTime))
    cv2.imshow("Image", image)
    cv2.waitKey(1)

print("Found: " + str(image_counter) + " matches.")
print("Time: " + str(time.time() - start_time))
cap.release()
cv2.destroyAllWindows()


