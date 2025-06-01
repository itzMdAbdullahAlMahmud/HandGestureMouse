
# 🖐️ Hand Gesture Mouse

**Hand Gesture Mouse** is a Python-based virtual mouse
that lets you control your computer using hand gestures 
captured through your webcam. No touchpad or mouse 
required — just wave your hand in the air!

---

## 📌 Features

- 🖱️ Mouse movement using index finger
- 👆 Left click by touching thumb and index finger
- 👉 Right click by touching thumb and middle finger
- 👇 Double click by touching thumb and ring finger
- ✊ Click and drag using thumb and index finger hold
- 🎥 Real-time hand tracking with MediaPipe
- ⚡ Smooth cursor motion

---

## 🔧 Requirements

- Python 3.7+
- Webcam

### 📦 Python Libraries

Install the required libraries using pip:

```bash
pip install opencv-python mediapipe pyautogui
````

Or install from the provided `requirements.txt`:

```bash
pip install -r requirements.txt
```

---

## 🚀 How to Run

1. Clone or download this repository.
2. Ensure your webcam is connected and functioning.
3. Run the script:

```bash
python hand_gesture_mouse.py
```

4. A window will open showing your webcam feed. Use hand gestures to control the mouse.
5. Press `q` to quit the application.

---

## 🖐️ Gesture Controls

| Gesture                             | Action         |
| ----------------------------------- | -------------- |
| Index finger pointing               | Move cursor    |
| Thumb + Index finger close          | Left click     |
| Thumb + Middle finger close         | Right click    |
| Thumb + Ring finger close           | Double click   |
| Thumb + Index held together (0.5s+) | Click and drag |

> *Cursor follows your index finger tip across the screen.*

---

## 🧠 Technologies Used

* **OpenCV** – Real-time computer vision
* **MediaPipe** – Hand landmark detection
* **PyAutoGUI** – Simulating mouse actions

---

## 🛡️ Disclaimer

This project is a proof of concept and may not be suitable for high-precision tasks.
Accuracy may vary based on lighting conditions and webcam quality.

---

## 📃 License

This project is open-source and available under the [MIT License](LICENSE).

---

## 🙌 Acknowledgments

* [Google MediaPipe](https://mediapipe.dev/)
* [OpenCV](https://opencv.org/)
* [PyAutoGUI](https://pyautogui.readthedocs.io/)

