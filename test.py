import cv2 as cv
from cvzone.HandTrackingModule import HandDetector
from pynput.keyboard import Controller
import webbrowser
import time

# Webcam setup
cap = cv.VideoCapture(2)
cap.set(3, 1400)
cap.set(4, 700)

detector = HandDetector(detectionCon=0.8)
keyboard = Controller()
msg = ""

# QWERTY Keyboard Layout
btnlist = [
    ["Q", 40, 100, 80, 80], ["W", 130, 100, 80, 80], ["E", 220, 100, 80, 80], ["R", 310, 100, 80, 80],
    ["T", 400, 100, 80, 80], ["Y", 490, 100, 80, 80], ["U", 580, 100, 80, 80], ["I", 670, 100, 80, 80],
    ["O", 760, 100, 80, 80], ["P", 850, 100, 80, 80], ["Backspace", 940, 100, 180, 80],

    ["A", 70, 200, 80, 80], ["S", 160, 200, 80, 80], ["D", 250, 200, 80, 80], ["F", 340, 200, 80, 80],
    ["G", 430, 200, 80, 80], ["H", 520, 200, 80, 80], ["J", 610, 200, 80, 80], ["K", 700, 200, 80, 80],
    ["L", 790, 200, 80, 80],

    ["Z", 130, 300, 80, 80], ["X", 220, 300, 80, 80], ["C", 310, 300, 80, 80], ["V", 400, 300, 80, 80],
    ["B", 490, 300, 80, 80], ["N", 580, 300, 80, 80], ["M", 670, 300, 80, 80], ["Enter", 880, 200, 240, 80],

    [" ", 200, 400, 500, 80], ["Google", 720, 400, 160, 80],
    ["YouTube", 890, 400, 160, 80], ["Instagram", 1060, 400, 180, 80]
]

# Draw key function with transparency
def drawbtn(img, x, y, w, h, text, color=(200, 200, 200), hover="none"):
    overlay = img.copy()
    alpha = 0.3
    rect_color = color

    if hover == "slide":
        rect_color = (255, 200, 200)
        alpha = 0.4
    elif hover == "click":
        rect_color = (0, 255, 0)
        alpha = 0.6

    cv.rectangle(overlay, (x, y), (x + w, y + h), rect_color, cv.FILLED)
    cv.addWeighted(overlay, alpha, img, 1 - alpha, 0, img)
    cv.rectangle(img, (x, y), (x + w, y + h), (50, 50, 50), 3)

    font_scale = 1.5 if len(text) == 1 else 1
    text_size = cv.getTextSize(text, cv.FONT_HERSHEY_SIMPLEX, font_scale, 2)[0]
    text_x = x + (w - text_size[0]) // 2
    text_y = y + (h + text_size[1]) // 2
    cv.putText(img, text, (text_x, text_y), cv.FONT_HERSHEY_SIMPLEX, font_scale, (0, 0, 0), 2)

    return img

last_pressed_time = 0
debounce_delay = 0.15  # reduced delay

while True:
    success, f = cap.read()
    f = cv.flip(f, 1)
    hands, f = detector.findHands(f)

    if hands:
        lmList = hands[0]["lmList"]

        for key, x, y, w, h in btnlist:
            f = drawbtn(f, x, y, w, h, key)

            if x < lmList[8][0] < x + w and y < lmList[8][1] < y + h:
                f = drawbtn(f, x, y, w, h, key, hover="slide")

                # Distance between index and thumb
                result = detector.findDistance((lmList[8][1], lmList[8][2]), (lmList[4][1], lmList[4][2]), f)

                l = result[0]

                if l < 40:
                    current_time = time.time()
                    if current_time - last_pressed_time > debounce_delay:
                        f = drawbtn(f, x, y, w, h, key, hover="click")

                        if key == "Backspace":
                            msg = msg[:-1]
                            keyboard.press('\b')
                        elif key == "Enter":
                            keyboard.press("\n")
                            if msg.strip():
                                webbrowser.open(f"https://www.google.com/search?q={msg.strip()}")
                            msg = ""
                        elif key == "Google":
                            webbrowser.open(f"https://www.google.com/search?q={msg.strip()}")
                        elif key == "YouTube":
                            webbrowser.open(f"https://www.youtube.com/results?search_query={msg.strip()}")
                        elif key == "Instagram":
                            webbrowser.open(f"https://www.instagram.com/explore/tags/{msg.strip()}/")
                        else:
                            keyboard.press(key)
                            msg += key

                        last_pressed_time = current_time

    # Display typed text
    cv.putText(f, f"Typed: {msg}", (50, 650), cv.FONT_HERSHEY_SIMPLEX, 1.5, (0, 255, 255), 3)
    cv.imshow("Virtual Keyboard", f)
    if cv.waitKey(1) == 27:  # ESC
        break

cap.release()
cv.destroyAllWindows()
