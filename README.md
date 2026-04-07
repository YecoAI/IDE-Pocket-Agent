# IDE Pocket Agent (Worker)

This repository contains the source code for the **IDE Pocket Agent**. The Agent is the local worker component that runs on your machine (server or workstation) to enable "Computer Use" capabilities and remote management via the IDE Pocket App.

For more information, visit the official website: [idepocket.com](https://idepocket.com)

## 🛡️ Trust & Privacy

We have chosen to make the **Agent** component **Open Source** to ensure total transparency and trust. As the bridge between your mobile device and your computer, the Agent has direct access to your desktop, captures your screen, and executes commands.

By keeping this component Open Source, we allow anyone to verify:
- **Data Privacy**: Exactly what data is captured and sent.
- **Secure Credentials**: How access tokens are encrypted locally using Windows DPAPI or macOS Keychain (via `keyring`).
- **Control**: The implementation of the safety **Kill Switch** to instantly stop all remote actions.

**Note:** While the Agent is Open Source for transparency, the **Backend Infrastructure** and the **Mobile App** are **Closed Source** (Proprietary to YecoAI).

## ✨ Key Features

- **Low-Latency Streaming**: Real-time visualization of your desktop or IDE with minimal lag (< 50ms response).
- **Secure Execution**: Commands are signed on your device and executed locally with zero-latency visual feedback.
- **Modern UI**: A sleek, professional interface built with the official IDE Pocket palette.
- **Cross-Platform Support**: Optimized for both Windows and macOS.
- **Background Mode**: Runs quietly in the System Tray, staying out of your way while keeping you connected.
- **Emergency Kill Switch**: Instantly stop all actions by moving the mouse and clicking 5 times in less than 3 seconds.
- **Smart Monitoring**: Automatic reconnection with exponential backoff to ensure stable long-term sessions.

## 🚀 Requirements & Installation

The Agent is written in Python and optimized for Windows and macOS.

1. **Clone the repository**:
   ```bash
   git clone https://github.com/yecoai/ide-pocket-agent.git
   cd ide-pocket-agent
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

### 🤖 Automatic Builds (CI/CD)
The project is configured with **GitHub Actions**. This means that you don't need to build the application manually on your machine.
- Every time you push a **Tag** (e.g., `v1.0.0`), GitHub will automatically build the versions for **Windows** and **macOS**.
- You can find the compiled binaries in the **Actions** tab of this repository or under **Releases**.

### 💻 Manual Build (Local)

#### Windows
To build the standalone executable (`.exe`) with all metadata and icons:

```bash
# Ensure PyInstaller is installed
pip install pyinstaller

# Generate the .ico icon from the official logo
python convert_icon.py

# Build the executable
pyinstaller --noconfirm --onefile --windowed --icon "IDE_Pocket.ico" --name "IDE-Pocket-Agent" --version-file "file_version_info.txt" --add-data "IDE_Pocket.png;." --add-data "src;src" --add-data "..\backend\operator_use;backend\operator_use" --hidden-import="customtkinter" --hidden-import="pystray" --hidden-import="PIL.Image" --hidden-import="pynput.mouse" --hidden-import="pynput.keyboard" --hidden-import="mss" --hidden-import="win32crypt" --hidden-import="win32gui" --hidden-import="win32api" --hidden-import="win32con" --hidden-import="comtypes" --hidden-import="comtypes.client" --hidden-import="comtypes.stream" main.py
```

#### macOS
To build the standalone application (`.app`) for macOS, you must run the build on a macOS machine. I have provided a helper script to automate this:

```bash
# 1. Give execution permissions
chmod +x build_macos.sh

# 2. Run the build script
./build_macos.sh
```

Alternatively, you can run the command manually:

```bash
# Ensure PyInstaller is installed
pip install pyinstaller

# Build the .app bundle
pyinstaller --noconfirm --onefile --windowed --icon "IDE_Pocket.png" --name "IDE-Pocket-Agent" --add-data "IDE_Pocket.png:." --add-data "src:src" --add-data "../backend/operator_use:backend/operator_use" --hidden-import="customtkinter" --hidden-import="pystray" --hidden-import="PIL.Image" --hidden-import="pynput.mouse" --hidden-import="pynput.keyboard" --hidden-import="mss" --hidden-import="keyring" main.py
```

Note: On macOS, the application will use the System Keychain to securely store your credentials.

## 👨‍💻 Author

Developed by **HighMark [ Marco N. ]** of **YecoAI**.

---
© 2026 [YecoAI](https://yecoai.com) - All Rights Reserved.
*Not affiliated with ByteDance Ltd.*
