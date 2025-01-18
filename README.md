# Finger-control
# 手勢音量控制系統

本專案使用 **MediaPipe** 和 **OpenCV** 建立即時手勢追蹤系統，並結合 **PyCAW** 實現電腦音量控制。系統透過檢測拇指與食指之間的距離調整音量，並在畫面上顯示當前音量百分比與 FPS（每秒幀數）。

## 功能介紹
- **即時手勢追蹤**：基於 MediaPipe 的手部追蹤功能。
- **音量控制**：依據拇指與食指的距離動態調整音量。
- **平滑化處理**：避免音量因微小抖動快速變化。
- 視覺化顯示：
  - 當前音量百分比。
  - 畫面 FPS（每秒幀數）。
- 用戶友好的操作介面，提供即時影像回饋。

## 環境需求
執行專案前，請確保安裝以下依賴套件：

```bash
conda create "project name" pythen=3.10.16
conda activate "project name"
pip install opencv-python mediapipe pycaw comtypes
```

## 執行步驟
1. 將此專案克隆至本地：
   ```bash
   git clone https://github.com/PCCUYing/Finger-control.git
   cd Finger-control
   ```
2. 執行主程式：
   ```bash
   python main.py
   ```
3. 操作方式：
   - 調整拇指與食指的距離來控制音量大小。
   - 按下 `ESC` 鍵結束程式。

## 專案檔案概述
- **`main.py`**：主程式，包含手勢追蹤與音量控制邏輯。
- **`test.py`**：測試套件是否安裝成功。

## 技術細節
- **手勢追蹤**：使用 MediaPipe Hands 模組檢測手部節點與連線。
- **音量控制**：透過 PyCAW 與 Windows 音量系統介接。
- **FPS 計算**：動態計算每秒幀數以監測系統效能。

## 示範
- 系統執行示例：

![示範截圖]
![image](https://github.com/user-attachments/assets/5a04cd44-b48d-4e5c-b369-a5d854ae7b9a)


## 未來改進方向
- 支援更多手勢操作功能。
- 提供跨平台音量控制支援。
- 優化效能以支援低階硬體。

## 授權條款
本專案採用 MIT 授權，歡迎自由使用與修改。

## 致謝
- [MediaPipe](https://google.github.io/mediapipe/) 提供手勢追蹤功能。
- [PyCAW](https://github.com/AndreMiras/pycaw) 提供音量控制介接。

---

如果您在使用過程中遇到問題或有改進建議，請隨時提交 Issue 或發送 Pull Request！

