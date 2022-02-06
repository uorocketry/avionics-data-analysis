import numpy as np
import cv2
import matplotlib.pyplot as plt
from scipy.fft import fft, fftfreq



print("ok")
cap = cv2.VideoCapture('./../data/attempt1/trial1_fullPres_100x_Trim.mp4')

roi_x = 490 #187
roi_y = 450
roi_w = 110
roi_h = 50

resultInTime = []

n = 0
while cap.isOpened():
    ret, frame = cap.read()
    n += 1
    # if frame is read correctly ret is True
    if not ret:
        print("Can't receive frame (stream end?). Exiting ...")
        break
    
    scale_percent = 60 # percent of original size
    width = int(frame.shape[1] * scale_percent / 100)
    height = int(frame.shape[0] * scale_percent / 100)
    dim = (width, height)
    
    # resize image
    resized = cv2.resize(frame, dim, interpolation = cv2.INTER_AREA)


    gray = cv2.cvtColor(resized, cv2.COLOR_BGR2GRAY)
    gray = cv2.rectangle(gray, (roi_x, roi_y), (roi_x+roi_w, roi_y+roi_h), (255, 0, 0), 1)


    roi = gray[roi_y:roi_y+roi_h, roi_x:roi_x+roi_w]
    roi_pixels = roi.flatten()

    roi_result = np.sum(roi_pixels)/roi_pixels.shape[0]

    resultInTime.append(roi_result)

    #print(roi_result)
    cv2.imshow('frame', gray)
    cv2.imshow('roi', roi)
    if cv2.waitKey(1) == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

plt.plot(resultInTime[100:1350])


yf = fft(resultInTime[100:1350])
xf = fftfreq((1350-100), 1 / 30)

#plt.plot(xf, np.abs(yf))

plt.show()