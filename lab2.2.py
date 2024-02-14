import cv2
import time
import math

cap = cv2.VideoCapture('sample.mp4')

countR=0
countL=0
mx=0
my=0

Pi=3.1415;
while True:
    ret, frame =cap.read()
    if not ret:
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
    gray = cv2.GaussianBlur(gray, (21, 21),0)

    ret, thresh = cv2.threshold(gray, 105, 255, cv2.THRESH_BINARY_INV)

    contours, hierarchy = cv2.findContours(thresh,
                                           cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    if len(contours) > 0:
        c = max(contours, key=cv2.contourArea)
        x, y, w, h = cv2.boundingRect(c)
        mx=mx+x+w/2
        my=my+y+h/2
        if 320 <= x + w / 2:
            color = (255, 0, 0)
            countL = countL+1
        else:
            color = (0, 0, 255)
            countR = countR+1
        cv2.circle(frame, (int(x+w/2), int(y+h/2) ), int(max(w/2, h/2)), color, 2)
        cv2.line(frame, (int(x+w/2),0),(int(x+w/2),480),color, 2)
        cv2.line(frame, (0, int(y+h/2)), (640, int(y+h/2)), color, 2)

        cv2.putText(frame, "({},{}), {}, {}%".format(x+w/2,y+h/2,
                                                     round(math.dist((x+w/2, y+h/2), (320, 240)), 2),
                                                     round(max(w/2, h/2)**2*Pi/480/640*100, 2)),
                    (0, 470), cv2.FONT_HERSHEY_SIMPLEX
                    , 1, (255, 255, 255), 2, cv2.LINE_AA)
        print("({},{})".format(x + w / 2, y + h / 2))
        if 220 <= x + w / 2 <= 420 and 140 <= y + h / 2 <= 340:
            color = (0, 0, 255)
        else:
            color = (0, 0, 0)
        cv2.rectangle(frame, (220, 140), (420, 340), color, 2)
        cv2.putText(frame, "{}".format(countR), (10, 30), cv2.FONT_HERSHEY_SIMPLEX
                    , 1, (255, 255, 255), 2, cv2.LINE_AA)
        cv2.putText(frame, "{}".format(countL), (550, 30), cv2.FONT_HERSHEY_SIMPLEX
                , 1, (255, 255, 255), 2, cv2.LINE_AA)

    cv2.imshow('frame',frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    time.sleep(0.1)

cap.release()
cv2.destroyAllWindows()

print("mean coord:({},{})".format(round(mx/(countR+countL),2),
                                  round(my/(countR+countL),2)))