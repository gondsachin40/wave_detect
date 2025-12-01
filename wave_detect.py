import cv2
import mediapipe as mp
import time

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=4,  
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7
)

HANDS_UP_THRESHOLD_RATIO = 0.5
DANGER_DURATION = 3  

hands_up_start_time = None

# --- Webcam setup ---
# videopath = "path in /"
# cap = cv2.VideoCapture(videopath)

cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("Error: Cannot access webcam")
    exit()

delay_ms = 33  

while True:
    success, frame = cap.read()
    if not success:
        print("Error: Failed to read frame from webcam")
        break

    h, w, _ = frame.shape
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(rgb_frame)

    left_up, right_up = False, False

    if results.multi_hand_landmarks and results.multi_handedness:
        for i, hand_landmarks in enumerate(results.multi_hand_landmarks):
            hand_label = results.multi_handedness[i].classification[0].label  
            wrist = hand_landmarks.landmark[mp_hands.HandLandmark.WRIST]

            if wrist.y < HANDS_UP_THRESHOLD_RATIO:
                cv2.circle(frame, (int(wrist.x * w), int(wrist.y * h)), 15, (0, 0, 255), cv2.FILLED)
                if hand_label == "Left":
                    left_up = True
                elif hand_label == "Right":
                    right_up = True

    if left_up and right_up:
        if hands_up_start_time is None:
            hands_up_start_time = time.time()
        elapsed = time.time() - hands_up_start_time
        cv2.putText(frame, f"BOTH HANDS UP: {elapsed:.1f}s", (20, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)
        if elapsed >= DANGER_DURATION:
            print("🚨 DANGER! Both hands held up for 3 seconds!")
            hands_up_start_time = None 
    else:
        hands_up_start_time = None
        cv2.putText(frame, f"BOTH HANDS UP: 0.0s", (20, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)

    cv2.imshow("Danger Signal Detection", frame)
    if cv2.waitKey(delay_ms) & 0xFF == 27: 
        break

cap.release()
cv2.destroyAllWindows()
hands.close()
