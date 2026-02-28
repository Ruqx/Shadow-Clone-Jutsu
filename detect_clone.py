import cv2
import mediapipe as mp
import numpy as np
import time

mp_hands = mp.solutions.hands
mp_selfie = mp.solutions.selfie_segmentation
mp_draw = mp.solutions.drawing_utils

hands = mp_hands.Hands(
    max_num_hands=2,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7
)

segment = mp_selfie.SelfieSegmentation(model_selection=1)

cap = cv2.VideoCapture(0)

clones_active = False
last_trigger = 0
trigger_delay = 1.5


# ----------------------------
# Detect Index Finger Up
# ----------------------------
def is_index_extended(hand):
    tip = hand.landmark[8]
    pip = hand.landmark[6]
    mcp = hand.landmark[5]
    return tip.y < pip.y < mcp.y


print("Perform Shadow Clone hand sign!")
print("Press Q to quit.")

while True:
    ret, frame = cap.read()
    if not ret:
        break

    h, w, _ = frame.shape
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    results = hands.process(rgb)
    detected_shadow_sign = False

    # ----------------------------
    # Detect Naruto Cross Sign
    # ----------------------------
    if results.multi_hand_landmarks and len(results.multi_hand_landmarks) == 2:

        hand1 = results.multi_hand_landmarks[0]
        hand2 = results.multi_hand_landmarks[1]

        index1 = is_index_extended(hand1)
        index2 = is_index_extended(hand2)

        tip1 = hand1.landmark[8]
        tip2 = hand2.landmark[8]

        distance = abs(tip1.x - tip2.x) + abs(tip1.y - tip2.y)

        if index1 and index2 and distance < 0.15:
            detected_shadow_sign = True

        for handLms in results.multi_hand_landmarks:
            mp_draw.draw_landmarks(frame, handLms, mp_hands.HAND_CONNECTIONS)

    current_time = time.time()

    # Activate clones
    if detected_shadow_sign and (current_time - last_trigger) > trigger_delay:
        clones_active = not clones_active  # toggle on/off
        last_trigger = current_time
        print("CLONES ACTIVATED!" if clones_active else "CLONES DEACTIVATED!")

    # ----------------------------
    # Segment Person
    # ----------------------------
    seg_result = segment.process(rgb)
    mask = seg_result.segmentation_mask
    condition = mask > 0.5

    person = np.zeros_like(frame)
    person[condition] = frame[condition]

    background = frame.copy()
    background[condition] = 0  # remove person from background

    display = background.copy()

    # ----------------------------
    # Draw LIVE Clones Behind
    # ----------------------------
    if clones_active:

        for i in range(8):

            offset_x = (i - 4) * 60
            scale = 1 - (i * 0.05)

            resized = cv2.resize(person, None, fx=scale, fy=scale)
            ch, cw, _ = resized.shape

            x_start = max(0, w // 2 - cw // 2 + offset_x)
            y_start = h - ch

            if x_start + cw < w and y_start >= 0:
                roi = display[y_start:y_start + ch, x_start:x_start + cw]

                mask_clone = resized > 0
                roi[mask_clone] = resized[mask_clone]

                display[y_start:y_start + ch, x_start:x_start + cw] = roi

    # ----------------------------
    # Draw ORIGINAL USER LAST (ON TOP)
    # ----------------------------
    mask_original = person > 0
    display[mask_original] = person[mask_original]

    cv2.imshow("Naruto Shadow Clone Jutsu", display)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()