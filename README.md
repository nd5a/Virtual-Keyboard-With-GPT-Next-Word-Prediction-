# Virtual-Keyboard-With-GPT-Next-Word-Prediction-

---

````markdown
## 🖐️ Virtual Keyboard with Hand Gesture & GPT Word Prediction

This Python project is an AI-powered Virtual Keyboard using OpenCV and hand tracking. It allows you to type by hovering your index finger over keys on the screen and includes:

- ✍️ Real-time hand gesture control
- 🔤 GPT-style next word prediction
- 🌐 Instant search buttons: Google Images, YouTube, Instagram
- 📹 HD screen recording
- ⌨️ On-screen virtual keyboard (QWERTY)

---

## 📸 Demo

![Screenshot 2025-05-23 174559](https://github.com/user-attachments/assets/8b177fa2-dc59-4daa-8dba-45ddf1ac1b00)


> You can type using your index finger. Hold for 1 second to press a key. Use the "Predict" button to complete words based on GPT prediction.

---

## 🚀 Features

- ✅ Hand tracking with `cvzone.HandTrackingModule`
- ✅ QWERTY semi-transparent on-screen keyboard
- ✅ Finger hover detection (press after 1 second hold)
- ✅ Predict next word using Hugging Face GPT API
- ✅ Search via Google (Image tab), YouTube, Instagram
- ✅ HD screen recording (1280×720 AVI output)
- ✅ Python OpenCV-based GUI

---

## 🛠️ Requirements

Install the dependencies using pip:

```bash
pip install opencv-python cvzone pynput requests
````

> Make sure you have Python 3.7+ installed and a webcam connected.

---

## 📂 File Structure

```
virtual-keyboard/
├── main.py                      # Main app file
├── gpt_predictor.py            # GPT next word predictor logic
├── output_HD.avi               # (Will be created after run)
├── screenshot.png              # Demo image (add yours)
├── requirements.txt
└── README.md
```

---

## 🔑 Hugging Face API Key Setup

In `gpt_predictor.py`, replace:

```python
self.headers = {
    "Authorization": "Bearer YOUR_HUGGINGFACE_TOKEN",
    "Content-Type": "application/json"
}
```

> Get a free API token from: [https://huggingface.co/settings/tokens](https://huggingface.co/settings/tokens)

---

## ▶️ How to Run

```bash
python main.py
```

> Press ESC key to exit.

---

## 🎥 Screen Recording

The app automatically records HD screen output (`output_HD.avi`) in the same folder.

You can convert it to `.mp4` using FFmpeg:

```bash
ffmpeg -i output_HD.avi output_HD.mp4
```

---

## 🌐 Special Keys

| Button    | Action                                   |
| --------- | ---------------------------------------- |
| Predict   | Suggests next word using GPT API         |
| Google    | Opens search result in Google Images tab |
| YouTube   | Opens YouTube search for typed content   |
| Instagram | Opens Instagram tag search               |
| Enter     | Executes search for typed query          |
| Backspace | Deletes last character                   |

---

## 🧠 How It Works

* **Hand Detection**: OpenCV captures frame → `cvzone.HandTrackingModule` detects index finger.
* **Key Selection**: If index finger hovers over a key for >1 second → key is pressed.
* **Prediction**: After typing 3+ characters, GPT predicts next word using Hugging Face.
* **Screen Recording**: Every frame is saved via `cv2.VideoWriter`.

---

## 📄 License

This project is licensed under the MIT License.

---

## 🤝 Contributions

Feel free to fork, enhance features, or submit pull requests.

---

## 💡 Credits

* [OpenCV](https://opencv.org/)
* [cvzone](https://github.com/cvzone)
* [Hugging Face Transformers](https://huggingface.co/)
* [Pynput](https://pypi.org/project/pynput/)

---
