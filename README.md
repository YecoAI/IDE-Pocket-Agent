# 🚀 IDEPocket - Your PC in Your Pocket

**Official Website: [idepocket.com](https://idepocket.com)**

> [!WARNING]
> **BETA / DEVELOPMENT ONLY**: This project is NOT a stable release. It is currently in active development, experimental, and may contain critical bugs or security flaws. Use at your own risk.

**Contribute to IDEPocket!** 🚀
We are open to and hope to receive Pull Requests from anyone who wants to continue or complete this project. Your contribution is valuable!

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![React Native](https://img.shields.io/badge/React%20Native-Expo-61DAFB.svg)](https://reactnative.dev/)

**IDEPocket** is a revolutionary open-source AI assistant that allows you to control your PC directly from your smartphone. It's not just a remote control: it's an autonomous agent capable of executing complex tasks, writing code, managing the terminal, and automating your workflow wherever you are.

> [!IMPORTANT]
> **Demo coming soon!** We are preparing a video demo to showcase the power of IDEPocket.

---

## ✨ Key Features

- **🤖 Multi-LLM Support**: Choose your favorite brain. Native support for OpenAI (GPT-5.5), Anthropic (Claude 4.7), Groq, Qwen, and Llama.
- **🛡️ Privacy First**: Want total control? Use **Ollama** to run local models. Your data never leaves your home network.
- **🖥️ Native Computer Use**: The agent interacts with the desktop like a human would: clicks, types, scrolls, and manages windows.
- **🛡️ Deterministic Security Layer**: Powered by **YecoAI Security Layer**. Heuristic filtering for prompt injections, PII/DLP protection, and execution sandbox guards with < 1.5ms latency.
- **📱 Mobile Experience**: Smooth app developed in React Native for immediate and intuitive control.
- **🛠️ Extensible**: Modular architecture designed for developers. Add your tools and customize the agent's behavior.

---

## 🏗️ Project Structure

| Module | Description |
| :--- | :--- |
| [Backend](./Backend) | FastAPI API, session management, database, and agent orchestration. |
| [Terminal_Agent](./Terminal_Agent) | The operational "arm" to run on the target PC. |
| [client_gui](./client_gui) | The mobile user interface (Android & PWA). |
| [shared](./shared) | Core logic, communication protocols, and tool definitions. |

---

## 🚀 Quick Start (One-Click)

The fastest way to start IDEPocket (Backend and Agent together) is using our quick start scripts.

1. **Clone the repository**:
   ```bash
   git clone https://github.com/YecoAI/IDE-Pocket.git
   cd IDE-Pocket
   ```

2. **Start the environment**:

   **Windows (PowerShell):**
   ```powershell
   .\start_local.ps1
   ```

   **Linux / macOS:**
   ```bash
   chmod +x start_local.sh
   ./start_local.sh
   ```

> **Note:** On the first run, the script will generate the `Backend/.env` file. Configure your API Keys inside and run the script again!

---

## 🛡️ Security & Architecture (IMPORTANT)

Since IDEPocket provides command execution and desktop control capabilities, security is our absolute priority. We implement a **Defense-in-Depth** strategy:

- **[YecoAI Security Layer](https://github.com/YecoAI/YecoAI-Security-Layer) (Heuristic Filter)**: Every input and output is processed by a deterministic security engine:
    - **Asimov Rules Injection**: Injects foundational safety guidelines into the LLM system prompt.
    - **SafetyModel Validation**: Scans LLM outputs for dangerous commands, SQLi, and sensitive data (API keys, etc.) before they reach the user.
    - **Execution Sandbox Guard**: Intercepts tool calls at runtime to prevent destructive operations (e.g., `rm -rf /`) and SSRF attacks.
- **Localhost Execution**: By default, the Backend and Terminal Agent communicate locally. No port is exposed to the public internet.
- **Total Privacy with Ollama**: You can run LLM models locally using Ollama. No data, screenshots, or code snippets will ever leave your home network.
- **JWT Authentication**: Remote access via the mobile app is protected by secure JWT tokens.
- **Principle of Least Privilege**: The Terminal Agent inherits only the permissions of the current user. It is highly recommended **not** to run the agent as `root` or Administrator.

---

## 🛠️ Manual Installation (Docker & More)

### Start Backend via Docker
You can easily start the Backend using Docker Compose. Make sure you have configured the `Backend/.env` file before starting.

```bash
docker-compose up -d
```

### 1. Backend (Server) - Manual Start
```bash
pip install -e ./shared
cd Backend
pip install -r requirements.txt
python main.py
```

### 2. Terminal Agent (Target PC)
```bash
pip install -e ./shared
cd Terminal_Agent
pip install -r requirements.txt
python main.py
```

### 3. Mobile App (Smartphone)
```bash
cd client_gui/android
npm install
npx expo start
```

---

## 🤝 Contributing

Contributions are what make the open source community such an amazing place. Any help is welcome! 

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📜 License

Distributed under the MIT License. See `LICENSE` for more information.

---

Developed with ❤️ by **[HighMark](https://highmark.it/) [ Marco N. ] @ YecoAI**
