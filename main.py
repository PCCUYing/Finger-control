import cv2
import mediapipe as mp
import math
import time
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
from comtypes import CLSCTX_ALL


def detect_hand_keypoints():
    # 初始化 MediaPipe Hands
    mp_hands = mp.solutions.hands
    hands = mp_hands.Hands(static_image_mode=False,
                           max_num_hands=1,
                           min_detection_confidence=0.7,
                           min_tracking_confidence=0.7)
    mp_drawing = mp.solutions.drawing_utils

    # 初始化 Pycaw 控制音量
    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(
        IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    volume = interface.QueryInterface(IAudioEndpointVolume)

    # 獲取音量範圍
    vol_range = volume.GetVolumeRange()
    min_vol = vol_range[0]
    max_vol = vol_range[1]

    # 開啟攝像頭
    cap = cv2.VideoCapture(0)

    prev_time = 0  # FPS 計算
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            print("攝像頭讀取失敗")
            break

        # 將影像轉為 RGB
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # 偵測手部關鍵點
        results = hands.process(frame_rgb)

        # 畫出手部關鍵點並控制音量
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                # 繪製手部關鍵點和連線
                mp_drawing.draw_landmarks(
                    frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

                # 提取手指關鍵點座標
                h, w, _ = frame.shape
                thumb_tip = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP]
                index_tip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]

                thumb_x, thumb_y = int(thumb_tip.x * w), int(thumb_tip.y * h)
                index_x, index_y = int(index_tip.x * w), int(index_tip.y * h)

                # 繪製大拇指與食指之間的線
                cv2.circle(frame, (thumb_x, thumb_y), 10, (255, 0, 0), -1)
                cv2.circle(frame, (index_x, index_y), 10, (0, 255, 0), -1)
                cv2.line(frame, (thumb_x, thumb_y), (index_x, index_y), (255, 0, 255), 3)

                # 計算大拇指與食指間的距離
                distance = math.hypot(index_x - thumb_x, index_y - thumb_y)

                # 距離對應到音量範圍
                vol = min_vol + ((distance - 20) / (300 - 20)) * (max_vol - min_vol)
                vol = max(min(vol, max_vol), min_vol)  # 限制音量範圍
                volume.SetMasterVolumeLevel(vol, None)

                # 顯示音量百分比
                vol_bar = int((vol - min_vol) / (max_vol - min_vol) * 100)
                cv2.rectangle(frame, (50, 100), (100, 400), (255, 255, 255), 2)
                cv2.rectangle(frame, (50, int(400 - vol_bar * 3)), (100, 400), (0, 255, 0), -1)
                cv2.putText(frame, f"Volume: {vol_bar}%", (50, 450),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

        # 計算並顯示 FPS
        curr_time = time.time()
        fps = 1 / (curr_time - prev_time)
        prev_time = curr_time
        cv2.putText(frame, f"FPS: {int(fps)}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

        # 顯示畫面
        cv2.imshow('Hand Volume Control', frame)

        # 按下 ESC 鍵退出
        if cv2.waitKey(1) & 0xFF == 27:
            break

    # 釋放資源
    cap.release()
    cv2.destroyAllWindows()
    hands.close()


if __name__ == "__main__":
    detect_hand_keypoints()
