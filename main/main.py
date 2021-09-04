from cv2 import cv2
import numpy as np
import mss
from pynput.mouse import Button, Controller


mouse = Controller()
stc = mss.mss()
stc2 = mss.mss()
acceleration_red_bar = 0
while True:
    scr = stc.grab({
        "left": 764,
        "top": 741,
        "width": 500,
        "height": 100,
    })

    frame = np.array(scr)
    hsvframe = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    red_lower = np.array([0, 50, 50], np.uint8)
    red_upper = np.array([10, 255, 255], np.uint8)
    red_mask = cv2.inRange(hsvframe, red_lower, red_upper)

    green_lower = np.array([40, 40, 40], np.uint8)
    green_upper = np.array([70, 255, 255], np.uint8)
    green_mask = cv2.inRange(hsvframe, green_lower, green_upper)

    kernal = np.ones((5, 5), "uint8")

    red_mask = cv2.dilate(red_mask, kernal)
    res_red = cv2.bitwise_and(frame, frame, mask=red_mask)

    green_mask = cv2.dilate(green_mask, kernal)
    res_green = cv2.bitwise_and(frame, frame, mask=green_mask)

    countours = cv2.findContours(red_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)[0]

    for pic, contour in enumerate(countours):
        area = cv2.contourArea(contour)
        if area > 900:
            x1, y1, w1, h1 = cv2.boundingRect(contour)
            frame_red_bar = cv2.rectangle(frame, (x1, y1), (x1 + w1, y1 + h1), (0, 0, 255), 2)
            print(len(frame_red_bar), "frame_red_bar")
            cv2.putText(frame, "red bar", (x1 + w1, y1 + h1), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255))
            print("red", x1)
            x_red1 = int(x1 + w1 / 2)
            y_red1 = int(y1 + h1 / 2)
            cv2.circle(frame, (x_red1, y_red1), 3, (0, 0, 255), -1)
            cv2.putText(frame, "red bar count: " + str(len(frame_red_bar) - 99), (10, 72), cv2.FONT_HERSHEY_SIMPLEX,
                        0.7, (0, 0, 255))

    for pic, contour in enumerate(countours):
        area2 = cv2.contourArea(contour)
        if 600 > area2 > 100:
            x1, y1, w1, h1 = cv2.boundingRect(contour)
            frame_red = cv2.rectangle(frame, (x1, y1), (x1 + w1, y1 + h1), (0, 0, 255), 2)
            x_red2 = int(x1 + w1 / 2)
            y_red2 = int(y1 + h1 / 2)
            acceleration_red_bar = x_red2 - acceleration_red_bar
            cv2.circle(frame, (x_red2, y_red2), 3, (0, 0, 255), -1)
            cv2.putText(frame, "hook", (x1 + w1, y1 + h1), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255))
            cv2.putText(frame, "hook count: " + str(len(frame_red) - 99), (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.7,
                        (0, 0, 255))

            try:
                cv2.line(frame, (x_red2, y_red2), (x_red1, y_red1), (0, 0, 255), 2)
                distance = int(np.sqrt((x_red2 - x_red1) ** 2 + (y_red2 - y_red1) ** 2))
                distance2 = int(np.sqrt((x_red2 - x_green) ** 2 + (y_red2 - y_green) ** 2))
                cv2.putText(frame, "distance: " + str(distance), (10, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255))
                cv2.putText(frame, "distance2: " + str(distance2), (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255))
                cv2.putText(frame, "green bar: " + str(x_green) + " " + str(y_green), (10, 20), cv2.FONT_HERSHEY_SIMPLEX,
                            0.7, (0, 0, 255))
                if not np.array_equal(frame_red, frame_green) and distance > 70:
                    if x_green > x_red2 and (x_red2 < x_red1):
                        print("red bar on the left1")
                        mouse.press(Button.left)
                    elif x_green < x_red2 and (x_red2 > x_red1)and distance > 70:
                        mouse.release(Button.left)
                        print("red bar on the left2")

                else:
                        if distance2 <= 10 or x_red2  > x_green and x1 > x2:
                            cv2.putText(frame, "red bar on the left", (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255))
                            print("red bar on the left3")
                            mouse.release(Button.left)
                        elif x_red2  < x_green and distance2 >10:
                            cv2.putText(frame, "red bar on the left", (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.7,
                                        (0, 0, 255))
                            print("red bar on the left4")
                            mouse.press(Button.left)



            except NameError:
                pass

    countours2 = cv2.findContours(green_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)[0]
    y_green_flag = 0
    for pic, contour in enumerate(countours2):

        area3 = cv2.contourArea(contour)
        if area3 > 500:
            x2, y2, w2, h2 = cv2.boundingRect(contour)
            frame_green = cv2.rectangle(frame, (x2, y2), (x2 + w2, y2 + h2), (0, 255, 0), 2)

            x_green = int(x2 + w2 / 2)
            y_green = int(y2 + h2 / 2)

            cv2.circle(frame, (x_green, y_green), 3, (0, 255, 0), -1)
            cv2.putText(frame, "green bar", (x2 + w2, y2 + h2), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0))
            cv2.putText(frame, str(x2), (80, 80), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0))
            cv2.putText(frame, "green bar count: " + str(len(countours2)), (10, 90), cv2.FONT_HERSHEY_SIMPLEX, 0.7,
                        (0, 255, 0))

            

            try:
                cv2.line(frame, (x_red2, y_red2), (x_green, y_green), (0, 255, 0), 2)

            except NameError:
                pass

    try:
        #The picture is divided into 10 equal parts with plenty of perpendicular lines.

        if np.array_equal(frame_red,frame_green):
            cv2.putText(frame, f"{np.intersect1d(frame_red, frame_green).size},1,hooked", (320, 90), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 255, 0))
        else:
            cv2.putText(frame, f"{np.intersect1d(frame_red, frame_green).size} ,2,not hooked", (320, 90), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 0, 255))
    except NameError:
        cv2.putText(frame, "not hooked", (320, 90), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 0, 255))

    cv2.imshow("frame", frame)
    cv2.imshow("red", res_red)
    cv2.imshow("green", res_green)
    cv2.setWindowProperty("frame", cv2.WND_PROP_TOPMOST, 1)
    cv2.setWindowProperty("red", cv2.WND_PROP_TOPMOST, 1)
    cv2.setWindowProperty("green", cv2.WND_PROP_TOPMOST, 1)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break
