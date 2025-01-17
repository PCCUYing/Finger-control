import cv2
import mediapipe as mp
import pycaw
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
from comtypes import CLSCTX_ALL
import math
import time

def detect_hand_keypoints():
    # Initialize MediaPipe Hands
    mp_hands = mp.solutions.hands
    hands = mp_hands.Hands(static_image_mode=False,
                           max_num_hands=1,
                           min_detection_confidence=0.5,
                           min_tracking_confidence=0.5)
    mp_drawing = mp.solutions.drawing_utils

    # Initialize pycaw for volume control
    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(
        IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    volume = interface.QueryInterface(IAudioEndpointVolume)

    # Get volume range
    vol_range = volume.GetVolumeRange()
    min_vol = vol_range[0]
    max_vol = vol_range[1]

    # Start webcam
    cap = cv2.VideoCapture(0)

    prev_distance = None  # For smoothing
    prev_time = 0  # For FPS calculation

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            print("Failed to grab frame")
            break

        # Convert BGR to RGB
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        # Process the frame to detect hand landmarks
        results = hands.process(frame_rgb)

        # Draw hand landmarks and control volume if detected
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                mp_drawing.draw_landmarks(
                    frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

                # Extract coordinates for thumb and index finger tips
                h, w, _ = frame.shape
                thumb_tip = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP]
                index_tip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]

                thumb_x, thumb_y = int(thumb_tip.x * w), int(thumb_tip.y * h)
                index_x, index_y = int(index_tip.x * w), int(index_tip.y * h)

                # Draw circles on thumb and index finger tips
                cv2.circle(frame, (thumb_x, thumb_y), 10, (255, 0, 0), -1)
                cv2.circle(frame, (index_x, index_y), 10, (0, 255, 0), -1)

                # Calculate distance between thumb and index finger
                distance = math.hypot(index_x - thumb_x, index_y - thumb_y)

                # Smooth the distance using moving average
                if prev_distance is None:
                    prev_distance = distance
                smoothed_distance = prev_distance * 0.8 + distance * 0.2
                prev_distance = smoothed_distance

                # Map distance to volume range
                scaled_distance = smoothed_distance * 1.5  # Adjust scaling factor
                vol = min_vol + (scaled_distance / w) * (max_vol - min_vol)
                vol = max(min(vol, max_vol), min_vol)  # Clamp to volume range
                volume.SetMasterVolumeLevel(vol, None)

                # Display volume level on the frame
                vol_bar = int((vol - min_vol) / (max_vol - min_vol) * 100)
                cv2.rectangle(frame, (50, 100), (100, 400), (255, 255, 255), 2)
                cv2.rectangle(frame, (50, int(400 - vol_bar * 3)), (100, 400), (0, 255, 0), -1)
                cv2.putText(frame, f"Volume: {vol_bar}%, Distance: {scaled_distance:.2f}", (50, 450),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

        # Calculate and display FPS
        curr_time = time.time()
        fps = 1 / (curr_time - prev_time)
        prev_time = curr_time
        cv2.putText(frame, f"FPS: {int(fps)}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

        # Display the frame
        cv2.imshow('Hand Volume Control', frame)

        # Break loop on 'ESC' key press
        if cv2.waitKey(1) & 0xFF == 27:
            break

    # Release resources
    cap.release()
    cv2.destroyAllWindows()
    hands.close()

if __name__ == "__main__":
    detect_hand_keypoints()
