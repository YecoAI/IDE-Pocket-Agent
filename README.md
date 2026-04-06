# TRAE Mobile Agent (Worker)

This repository contains the source code for the **TRAE Mobile Agent**. The Agent is the local worker component that runs on your machine (server or workstation) to enable "Computer Use" capabilities and remote management via the TRAE Mobile App.

For more information, visit the official website: [trae-mobile.yecoai.com](https://trae-mobile.yecoai.com)

## 🛡️ Trust & Privacy

We have chosen to make the **Agent** component **Open Source** to ensure total transparency and trust. As the bridge between your mobile device and your computer, the Agent has direct access to your desktop, captures your screen, and executes commands.

By keeping this component Open Source, we allow anyone to verify:
- **Data Privacy**: Exactly what data is captured and sent.
- **Secure Credentials**: How access tokens are encrypted locally using Windows DPAPI.
- **Control**: The implementation of the safety **Kill Switch** to instantly stop all remote actions.

**Note:** While the Agent is Open Source for transparency, the **Backend Infrastructure** and the **Mobile App** are **Closed Source** (Proprietary to YecoAI).

## ✨ Key Features

- **Low-Latency Streaming**: Real-time visualization of your desktop or IDE with minimal lag (< 50ms response).
- **Secure Execution**: Commands are signed on your device and executed locally with zero-latency visual feedback.
- **Modern UI**: A sleek, professional interface built with the official TRAE.ai palette.
- **Background Mode**: Runs quietly in the System Tray, staying out of your way while keeping you connected.
- **Emergency Kill Switch**: Instantly stop all actions by moving the mouse and clicking 5 times in less than 3 seconds.
- **Smart Monitoring**: Automatic reconnection with exponential backoff to ensure stable long-term sessions.

## 🚀 Requirements & Installation

The Agent is written in Python and optimized for Windows systems.

1. **Clone the repository**:
   ```bash
   git clone https://github.com/YecoAI/TRAE-Mobile-Agent.git
   cd trae-mobile-agent
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the Agent**:
   ```bash
   python main.py
   ```

## 🛠️ Development & Build

To build the standalone executable (`.exe`) with all metadata and icons:

```bash
# Ensure PyInstaller is installed
pip install pyinstaller

# Generate the .ico icon from the official logo
python convert_icon.py

# Build the executable
pyinstaller --noconfirm --onefile --windowed --icon "TRAE_Mobile.ico" --name "TRAE-Mobile-Agent" --version-file "file_version_info.txt" --add-data "TRAE_Mobile.png;." --add-data "src;src" --add-data "..\backend\operator_use;backend\operator_use" --hidden-import="customtkinter" --hidden-import="pystray" --hidden-import="PIL.Image" --hidden-import="pynput.mouse" --hidden-import="pynput.keyboard" --hidden-import="mss" --hidden-import="win32crypt" --hidden-import="win32gui" --hidden-import="win32api" --hidden-import="win32con" --hidden-import="comtypes" --hidden-import="comtypes.client" --hidden-import="comtypes.stream" main.py
```

## 👨‍💻 Author

Developed by **HighMark [ Marco N. ]** of **YecoAI**.

---
© 2026 [YecoAI](https://yecoai.com) - All Rights Reserved.
*Not affiliated with TRAE or ByteDance Ltd.*
