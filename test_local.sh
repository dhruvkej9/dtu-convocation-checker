#!/bin/bash
# Local Test Script for DTU Convocation Checker
# This allows you to test the script locally before deploying to GitHub Actions

echo "=================================="
echo "DTU Convocation Checker - Local Test"
echo "=================================="
echo ""

# Check if .env file exists
if [ ! -f .env ]; then
    echo "Creating .env file for local testing..."
    cat > .env << 'EOF'
# DTU Convocation Checker - Local Configuration
# Fill in your details below and save this file

# Your name in CAPITALS (as shown on DTU portal)
export STUDENT_NAME="DHRUV KEJRWAL"

# Comma-separated roll numbers to check
# Example: "2K21/MC/053, 2K21/MC/53"
export ROLL_NUMBERS="2K21/MC/053, 2K21/MC/53"

# Date of birth in dd-mm-yyyy format
export DATE_OF_BIRTH="09-02-2004"

# Telegram Bot Token (get from @BotFather)
export TELEGRAM_BOT_TOKEN="your_bot_token_here"

# Telegram Chat ID (get from @userinfobot)
export TELEGRAM_CHAT_ID="your_chat_id_here"
EOF
    echo "✓ Created .env file"
    echo ""
    echo "Please edit .env file with your credentials and run this script again."
    exit 1
fi

# Load environment variables
source .env

# Validate configuration
if [ "$TELEGRAM_BOT_TOKEN" = "your_bot_token_here" ]; then
    echo "❌ Error: Please configure your credentials in .env file"
    exit 1
fi

echo "Configuration:"
echo "  Name: $STUDENT_NAME"
echo "  Roll Numbers: $ROLL_NUMBERS"
echo "  DOB: $DATE_OF_BIRTH"
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.8 or higher."
    exit 1
fi


echo "Installing dependencies..."
pip install pytest-playwright playwright requests -U

echo "Installing Playwright browsers and dependencies..."
playwright install chromium
playwright install-deps chromium

echo ""
echo "Running the convocation checker..."
echo "=================================="
echo ""

python3 main.py

echo ""
echo "=================================="
echo "Test completed!"
echo "Check your Telegram for the notification."
echo "Screenshots are saved in the current directory."
