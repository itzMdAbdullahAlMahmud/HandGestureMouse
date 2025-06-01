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



clicking = False
dragging = False
drag_start_time = None
right_clicking = False
double_clicking = False


while True:
    success, img = cap.read()
    img = cv2.flip(img, 1)
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    result = hands.process(img_rgb)


    if result.multi_hand_landmarks:
        for hand_landmarks in result.multi_hand_landmarks:
            lm_list = hand_landmarks.landmark
            h, w, _ = img.shape

            if len(lm_list) >= 13:
                # Index Finger Tip
                x = int(lm_list[8].x * w)
                y = int(lm_list[8].y * h)
                screen_x = screen_w * lm_list[8].x
                screen_y = screen_h * lm_list[8].y

                curr_x = prev_x + (screen_x - prev_x) / smoothening
                curr_y = prev_y + (screen_y - prev_y) / smoothening
                pyautogui.moveTo(curr_x, curr_y)
                prev_x, prev_y = curr_x, curr_y


                # Thumb Tip
                x_thumb = int(lm_list[4].x * w)
                y_thumb = int(lm_list[4].y * h)
                dist_thumb_index = math.hypot(x_thumb - x, y_thumb - y)

                # Middle Finger Tip
                x_middle = int(lm_list[12].x * w)
                y_middle = int(lm_list[12].y * h)
                dist_thumb_middle = math.hypot(x_thumb - x_middle, y_thumb - y_middle)

                # Pinky tip for selection mode
                x_pinky = int(lm_list[20].x * w)
                y_pinky = int(lm_list[20].y * h)

                # Ring Finger Tip
                x_ring = int(lm_list[16].x * w)
                y_ring = int(lm_list[16].y * h)
                dist_thumb_ring = math.hypot(x_thumb - x_ring, y_thumb - y_ring)





                # Draw
                cv2.circle(img, (x, y), 10, (255, 0, 0), cv2.FILLED)
                cv2.line(img, (x, y), (x_thumb, y_thumb), (0, 255, 0), 2)



                # Left Click
                if dist_thumb_index < 30 and not clicking and not dragging:
                    clicking = True
                    pyautogui.click()
                    time.sleep(0.3)
                elif dist_thumb_index >= 30:
                    clicking = False








                # Right Click
                if dist_thumb_middle < 30 and not right_clicking:
                    right_clicking = True
                    pyautogui.rightClick()
                    time.sleep(0.3)
                elif dist_thumb_middle >= 30:
                    right_clicking = False

                # --- Double Click ---
                if dist_thumb_ring < 30 and not double_clicking:
                    double_clicking = True
                    pyautogui.doubleClick()
                    time.sleep(0.3)
                elif dist_thumb_ring >= 30:
                    double_clicking = False


                # Click and Drag
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
