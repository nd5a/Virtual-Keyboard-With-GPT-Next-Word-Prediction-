import subprocess
import cv2 as cv
from cvzone.HandTrackingModule import HandDetector
from pynput.keyboard import Controller
import webbrowser
import time
from gpt_predictor import GPTNextWordPredictor

# Webcam setup
cap = cv.VideoCapture(2)
cap.set(3, 640)  # Width
cap.set(4, 480)  # Height

detector = HandDetector(detectionCon=0.6)
keyboard = Controller()
predictor = GPTNextWordPredictor()

msg = ""
next_word = ""

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
    ["YouTube", 890, 400, 160, 80], ["Instagram", 1060, 400, 180, 80],
    ["Predict", 40, 400, 140, 80]
]

# Draw key function with transparency
def drawbtn(img, x, y, w, h, text, color=(200, 200, 200), hover="none"):
    overlay = img.copy()
    alpha = 0.2
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
debounce_delay = 0.15
hover_start_time = {}  # New: Track when each key is hovered

while True:
    success, f = cap.read()
    f = cv.flip(f, 1)
    
    hands, f = detector.findHands(f)

    if hands:
        lmList = hands[0]["lmList"]
        index_finger = lmList[8][:2]  # (x, y) of index fingertip

        for key, x, y, w, h in btnlist:
            f = drawbtn(f, x, y, w, h, key)

            if x < index_finger[0] < x + w and y < index_finger[1] < y + h:
                f = drawbtn(f, x, y, w, h, key, hover="slide")
                if key not in hover_start_time:
                    hover_start_time[key] = time.time()
                else:
                    if time.time() - hover_start_time[key] >= 1:  # 1 seconds hold
                        f = drawbtn(f, x, y, w, h, key, hover="click")

                        if key == "Backspace":
                            msg = msg[:-1]
                            keyboard.press("\b")
                        elif key == "Enter":
                            keyboard.press("\n")
                            if msg.strip():
                                webbrowser.open(f"https://www.google.com/search?q={msg.strip()}")
                            msg = ""
                        elif key == "Predict":
                            if next_word:
                                msg += " " + next_word
                                keyboard.press(" ")
                                for ch in next_word:
                                    keyboard.press(ch)
                                next_word = ""
                        # elif key == "Google":
                        #     webbrowser.open(f"https://www.google.com/search?q={msg.strip()}")
                        elif key == "Google":
                            if msg.strip():
                                query = msg.strip()
                                url = f"https://www.google.com/search?tbm=isch&q={query}"
                                subprocess.Popen(['C:\\Program Files\\Mozilla Firefox\\firefox.exe', url])

                        elif key == "YouTube":
                            webbrowser.open(f"https://www.youtube.com/results?search_query={msg.strip()}")
                        elif key == "Instagram":
                            webbrowser.open(f"https://www.instagram.com/explore/tags/{msg.strip()}/")
                        else:
                            keyboard.press(key)
                            msg += key
                            last_word = msg.strip().split()[-1] if msg.strip().split() else ""
                            if len(last_word) >= 3:
                                next_word = predictor.predict_next(msg.strip())
                            

                        hover_start_time.clear()  # Reset all timers after press
            else:
                if key in hover_start_time:
                    del hover_start_time[key]  # Remove if not hovered

    else:
        hover_start_time.clear()

    # Display text and prediction
    cv.putText(f, f"Typed: {msg}", (50, 650), cv.FONT_HERSHEY_SIMPLEX, 1.5, (0, 255, 255), 3)
    cv.putText(f, f"Prediction: {next_word}", (800, 650), cv.FONT_HERSHEY_SIMPLEX, 1.2, (255, 100, 100), 2)

    cv.imshow("Virtual Keyboard", f)
    if cv.waitKey(10) == 27:
        break

cap.release()
cv.destroyAllWindows()
