#!/bin/bash

# IDE Pocket Agent - macOS Build Script
# This script bundles the Python application into a standalone .app for macOS.

echo "🚀 Starting IDE Pocket Agent build for macOS..."

# 1. Check for Python
if ! command -v python3 &> /dev/null
then
    echo "❌ Error: python3 is not installed."
    exit 1
fi

# 2. Create Virtual Environment
echo "📦 Setting up virtual environment..."
python3 -m venv venv_build
source venv_build/bin/activate

# 3. Install Dependencies
echo "📥 Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt
pip install pyinstaller

# 4. Clean previous builds
echo "🧹 Cleaning old build artifacts..."
rm -rf build dist IDE-Pocket-Agent.spec

# 5. Build with PyInstaller
echo "🛠️ Building .app bundle..."
pyinstaller --noconfirm --onefile --windowed \
    --icon "IDE_Pocket.png" \
    --name "IDE-Pocket-Agent" \
    --add-data "IDE_Pocket.png:." \
    --add-data "src:src" \
    --add-data "../backend/operator_use:backend/operator_use" \
    --hidden-import="customtkinter" \
    --hidden-import="pystray" \
    --hidden-import="PIL.Image" \
    --hidden-import="pynput.mouse" \
    --hidden-import="pynput.keyboard" \
    --hidden-import="mss" \
    --hidden-import="keyring" \
    main.py

# 6. Check result
if [ -d "dist/IDE-Pocket-Agent.app" ] || [ -f "dist/IDE-Pocket-Agent" ]; then
    echo "✅ Build successful! You can find the application in the 'dist' folder."
else
    echo "❌ Build failed. Please check the logs above."
    exit 1
fi

deactivate
echo "Done."
