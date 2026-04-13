#!/bin/zsh

# Get the directory where this script is located
# Use a more robust way for zsh/bash compatibility
cd "$(dirname "$0")"

echo "--------------------------------------"
echo "🚀 GSC Citation Audit Tool"
echo "--------------------------------------"

# Ensure requirements.txt exists where we are
if [ ! -f "requirements.txt" ]; then
    echo "❌ Error: Could not find requirements.txt in the project folder."
    exit 1
fi

# Check if streamlit is already installed
python3 -m streamlit --version &> /dev/null
if [ $? -ne 0 ]; then
    echo "📦 Dependencies not found. Installing..."
    python3 -m pip install -r requirements.txt
    if [ $? -ne 0 ]; then
        echo "❌ Installation failed. Please check your internet connection."
        exit 1
    fi
fi

echo "✨ Launching the app... Keep this window open."
python3 -m streamlit run app.py
