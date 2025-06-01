import cv2
import mediapipe as mp
import pyautogui
import time
import math

cap = cv2.VideoCapture(0)
screen_w, screen_h = pyautogui.size()

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.7)
mp_draw = mp.solutions.drawing_utils

prev_x, prev_y = 0, 0
smoothening = 3

prev_hand_y = None
scroll_sensitivity = 50
scroll_threshold = 20

clicking = False
dragging = False
drag_start_time = None
right_clicking = False
double_clicking = False

# NEW: For scroll stability
scroll_mode_start = None
scroll_mode_delay = 0.2  # seconds

while True:
    success, img = cap.read()
    img = cv2.flip(img, 1)
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    result = hands.process(img_rgb)

    if result.multi_hand_landmarks:
        for hand_landmarks in result.multi_hand_landmarks:
            lm_list = hand_landmarks.landmark
            h, w, _ = img.shape

            if len(lm_list) >= 21:
                # Index finger tip
                x = int(lm_list[8].x * w)
                y = int(lm_list[8].y * h)
                screen_x = screen_w * lm_list[8].x
                screen_y = screen_h * lm_list[8].y

                curr_x = prev_x + (screen_x - prev_x) / smoothening
                curr_y = prev_y + (screen_y - prev_y) / smoothening
                pyautogui.moveTo(curr_x, curr_y)
                prev_x, prev_y = curr_x, curr_y

                # Thumb tip
                x_thumb = int(lm_list[4].x * w)
                y_thumb = int(lm_list[4].y * h)
                dist_thumb_index = math.hypot(x_thumb - x, y_thumb - y)

                # Middle finger tip
                x_middle = int(lm_list[12].x * w)
                y_middle = int(lm_list[12].y * h)
                dist_thumb_middle = math.hypot(x_thumb - x_middle, y_thumb - y_middle)

                # Ring finger tip
                x_ring = int(lm_list[16].x * w)
                y_ring = int(lm_list[16].y * h)
                dist_thumb_ring = math.hypot(x_thumb - x_ring, y_thumb - y_ring)

                # Drawing pointer
                cv2.circle(img, (x, y), 10, (255, 0, 0), cv2.FILLED)
                cv2.line(img, (x, y), (x_thumb, y_thumb), (0, 255, 0), 2)

                # === Finger Extension Check ===
                finger_tips = [8, 12, 16, 20]
                finger_pips = [6, 10, 14, 18]
                extended_fingers = 0
                for tip_id, pip_id in zip(finger_tips, finger_pips):
                    if lm_list[tip_id].y < lm_list[pip_id].y:
                        extended_fingers += 1

                # Reliable thumb extension detection
                thumb_tip = lm_list[4]
                index_mcp = lm_list[5]
                thumb_dist = math.hypot(thumb_tip.x - index_mcp.x, thumb_tip.y - index_mcp.y)
                thumb_extended = thumb_dist > 0.1

                # === Scroll Logic ===
                if extended_fingers == 4 and not thumb_extended:
                    if scroll_mode_start is None:
                        scroll_mode_start = time.time()
                    elif time.time() - scroll_mode_start > scroll_mode_delay:
                        hand_y = lm_list[0].y * screen_h

                        if prev_hand_y is not None:
                            dy = hand_y - prev_hand_y
                            if abs(dy) > scroll_threshold:
                                if dy < 0:
                                    pyautogui.scroll(scroll_sensitivity)
                                    cv2.putText(img, "Scroll Up", (10, 110), cv2.FONT_HERSHEY_SIMPLEX, 1,
                                                (0, 255, 255), 2)
                                else:
                                    pyautogui.scroll(-scroll_sensitivity)
                                    cv2.putText(img, "Scroll Down", (10, 110), cv2.FONT_HERSHEY_SIMPLEX, 1,
                                                (0, 255, 255), 2)

                        prev_hand_y = hand_y
                else:
                    scroll_mode_start = None
                    prev_hand_y = None

                # === Left Click ===
                if dist_thumb_index < 30 and not clicking and not dragging:
                    clicking = True
                    pyautogui.click()
                    time.sleep(0.3)
                elif dist_thumb_index >= 30:
                    clicking = False

                # === Right Click ===
                if dist_thumb_middle < 30 and not right_clicking:
                    right_clicking = True
                    pyautogui.rightClick()
                    time.sleep(0.3)
                elif dist_thumb_middle >= 30:
                    right_clicking = False

                # === Double Click ===
                if dist_thumb_ring < 30 and not double_clicking:
                    double_clicking = True
                    pyautogui.doubleClick()
                    time.sleep(0.3)
                elif dist_thumb_ring >= 30:
                    double_clicking = False

                # === Click and Drag ===
                if dist_thumb_index < 30:
                    if not dragging:
                        if drag_start_time is None:
                            drag_start_time = time.time()
                        elif time.time() - drag_start_time > 0.5:
                            dragging = True
                            pyautogui.mouseDown()
                    else:
                        curr_x = prev_x + (screen_x - prev_x) / smoothening
                        curr_y = prev_y + (screen_y - prev_y) / smoothening
                        pyautogui.moveTo(curr_x, curr_y)
                        prev_x, prev_y = curr_x, curr_y
                else:
                    drag_start_time = None
                    if dragging:
                        dragging = False
                        pyautogui.mouseUp()

            mp_draw.draw_landmarks(img, hand_landmarks, mp_hands.HAND_CONNECTIONS)

    cv2.imshow("Hand Gesture Mouse", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
