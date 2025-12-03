# 🎓 DTU Convocation Checker

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![Playwright](https://img.shields.io/badge/Playwright-enabled-brightgreen.svg)](https://playwright.dev/)

An automated system that checks the DTU Convocation portal twice daily for multiple roll number variations and sends notifications via Telegram with screenshots.

## ✨ Features

- 🔄 **Automated Monitoring** - Checks the DTU convocation portal twice daily
- 🔢 **Multi-Roll Number Support** - Check multiple roll number variations simultaneously
- 📱 **Telegram Notifications** - Instant alerts with screenshots
- 🖼️ **Screenshot Capture** - Visual proof of portal status
- ⏰ **Scheduled Runs** - Runs at 2:00 PM and 10:00 PM IST
- 🆓 **100% Free** - Uses GitHub Actions (no credit card required)
- 🐳 **Docker Ready** - Can be deployed to Render or any container platform

## 📋 Table of Contents

- [Quick Start](#-quick-start)
- [Prerequisites](#-prerequisites)
- [Setup Guide](#-setup-guide)
- [Configuration](#-configuration)
- [Schedule](#-schedule)
- [Sample Notification](#-sample-notification)
- [Deployment Options](#-deployment-options)
- [Troubleshooting](#-troubleshooting)
- [Project Structure](#-project-structure)
- [Contributing](#-contributing)
- [License](#-license)

## 🚀 Quick Start

1. **Fork** this repository
2. **Create** a Telegram bot via [@BotFather](https://t.me/botfather)
3. **Add** your credentials as GitHub Secrets
4. **Enable** GitHub Actions
5. **Done!** You'll receive notifications twice daily

## 📦 Prerequisites

- GitHub account (free)
- Telegram account (free)
- 10 minutes of setup time

## 🔧 Setup Guide

### Step 1: Fork This Repository

1. Click the **"Fork"** button at the top right of this page
2. This creates your own copy of the repository

### Step 2: Set Up Telegram Bot

First, create a Telegram bot to receive notifications:

**Creating your Telegram bot:**

1. Open Telegram and search for [@BotFather](https://t.me/botfather)
2. Start a chat and send `/newbot`
3. Give your bot a name (e.g., "DTU Convocation Monitor")
4. Give it a username (must end in 'bot', e.g., `dtu_convocation_check_bot`)
5. Save the **token** (looks like `1234567890:ABCdefGHIjklMNOpqrsTUVwxyz`)

**Getting your Chat ID:**

1. Search for your new bot in Telegram and start a conversation
2. Send any message to it (e.g., "Hello")
3. Open this URL in your browser (replace `<YOUR_BOT_TOKEN>` with your token):
   ```
   https://api.telegram.org/bot<YOUR_BOT_TOKEN>/getUpdates
   ```
4. Look for `"chat":{"id":` followed by a number — that's your **Chat ID**

### Step 3: Add GitHub Secrets

Store your credentials securely in GitHub Secrets:

1. Go to your forked repository → **Settings** → **Secrets and variables** → **Actions**
2. Click **"New repository secret"** for each of the following:

| Secret Name | Description | Example |
|------------|-------------|---------|
| `STUDENT_NAME` | Your name in CAPITALS | `DHRUV KEJRWAL` |
| `ROLL_NUMBERS` | Comma-separated roll numbers | `2K21/MC/053, 2K21/MC/53` |
| `DATE_OF_BIRTH` | Date in dd-mm-yyyy format | `19-07-2000` |
| `TELEGRAM_BOT_TOKEN` | Bot token from Step 2 | `123456789:ABC...` |
| `TELEGRAM_CHAT_ID` | Chat ID from Step 2 | `123456789` |

> **Note:** For `ROLL_NUMBERS`, separate multiple variations with commas to check different formats.

### Step 4: Enable GitHub Actions

1. Go to the **Actions** tab in your repository
2. Click **"I understand my workflows, go ahead and enable them"**

### Step 5: Test Your Setup

Test your setup immediately:

1. Go to **Actions** → **DTU Convocation Checker**
2. Click **"Run workflow"** → **"Run workflow"**
3. Wait 1-2 minutes
4. Check your Telegram for the notification!

## ⚙️ Configuration

### Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `STUDENT_NAME` | Yes | Student name in CAPITALS |
| `ROLL_NUMBERS` | Yes | Comma-separated roll numbers |
| `DATE_OF_BIRTH` | Yes | Date in dd-mm-yyyy format |
| `TELEGRAM_BOT_TOKEN` | Yes | Telegram bot API token |
| `TELEGRAM_CHAT_ID` | Yes | Telegram chat ID for notifications |

## ⏰ Schedule

The workflow runs automatically **twice daily**:

| Time (IST) | Time (UTC) | Description |
|------------|------------|-------------|
| 2:00 PM | 8:30 AM | Afternoon check |
| 10:00 PM | 4:30 PM | Evening check |

You can also trigger it **manually anytime** from the GitHub Actions tab.

### Customizing the Schedule

Edit `.github/workflows/check_convocation.yml`:

```yaml
schedule:
  - cron: '30 8 * * *'   # 2:00 PM IST
  - cron: '30 16 * * *'  # 10:00 PM IST
```

Use [Crontab Guru](https://crontab.guru/) to create custom schedules.

## 📱 Sample Notification

```
🎓 DTU Convocation Multi-Check Report

📅 Check Time: 07 October 2025, 2:00 PM IST
👤 Student: DHRUV KEJRWAL
🔢 Roll Numbers Checked: 2

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Check #1: 2K21/MC/053

❌ Roll No Not Found
Your roll number is not yet in the convocation system.

📄 Page Title: DTU Convocation 2024

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Check #2: 2K21/MC/53

❌ Roll No Not Found
Your roll number is not yet in the convocation system.

📄 Page Title: DTU Convocation 2024

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

💡 What This Means:
• If both show "Not Found": Normal before convocation announcement
• If one is "Found": Use that roll number format on the portal
• If results differ: The portal may prefer one format over the other

Automated check running twice daily at 2 PM and 10 PM IST
```

Plus screenshots of each check!

## 🐳 Deployment Options

### Option 1: GitHub Actions (Recommended)

The default deployment method. Simply fork and configure as described above.

### Option 2: Render Deployment

Deploy as a web service on Render for API-based triggering:

1. Create a new Web Service on [Render](https://render.com)
2. Connect your forked repository
3. Set the following:
   - **Environment:** Docker
   - **Build Command:** (auto-detected from Dockerfile)
   - **Start Command:** (auto-detected from Dockerfile)
4. Add environment variables in Render dashboard

#### API Endpoints (Render Deployment)

| Endpoint | Description |
|----------|-------------|
| `/` | API info and available endpoints |
| `/health` | Health check (use for cron jobs) |
| `/wakeup` | Wake-up status info |
| `/check` | Trigger convocation check (async) |
| `/check-sync` | Trigger convocation check (sync) |

#### Wake-Up Script

For Render's free tier, use the wake-up utility to prevent cold starts:

```bash
# Wake up the app (default 60s timeout)
python wakeup.py

# With custom timeout and retries
python wakeup.py --timeout 90 --retries 3
```

## 🔧 Troubleshooting

### Not receiving notifications?

1. **Start your bot**: Make sure you've sent a message to your bot first
2. **Verify secrets**: Ensure all 5 secrets are added correctly
3. **Check Actions tab**: Look for error messages in workflow runs
4. **Date format**: Use dd-mm-yyyy (e.g., `09-02-2004`, not `9-2-2004`)

### Want to check more roll numbers?

Add them to the `ROLL_NUMBERS` secret, separated by commas:

```
2K21/MC/053, 2K21/MC/53, 2K21/MC/0053
```

## 📊 How It Works

1. **GitHub Actions** triggers the workflow twice daily
2. **Python script** launches a headless browser using Playwright
3. Script navigates to DTU convocation portal
4. Logs in with each roll number variation
5. Captures the response and takes screenshot
6. Sends everything to your Telegram

## 💰 Cost

**100% FREE!**
- GitHub Actions: Free for public repositories (2000 minutes/month)
- Telegram Bot: Free forever
- No credit card required anywhere

## 🔒 Security

- All credentials stored as encrypted GitHub Secrets
- Bot token and chat ID never exposed in code
- Screenshots automatically deleted after 7 days

## 📝 Notes

- The script is respectful to the DTU servers with appropriate delays
- Screenshots are uploaded as GitHub artifacts (backup)
- Each roll number is checked sequentially
- Portal text is analyzed to determine status

## 🤝 Support

If you encounter issues:
1. Check the Actions tab for error logs
2. Verify all secrets are correctly configured
3. Ensure date format is exactly dd-mm-yyyy
4. Make sure you've started a chat with your Telegram bot

## ⚠️ Disclaimer

This is an educational project for automating legitimate access to your own convocation portal. Use responsibly and in accordance with DTU's terms of service.

## 📂 Project Structure

```
dtu-convocation-checker/
├── main.py                    # Main automation script
├── server.py                  # FastAPI server for API deployment
├── wakeup.py                  # Render wake-up utility
├── requirements.txt           # Python dependencies
├── Dockerfile                 # Docker configuration
├── render.yaml                # Render deployment config
├── .github/
│   └── workflows/
│       ├── check_convocation.yml  # Main checker workflow
│       └── keep_alive.yml         # Keep Render app alive
└── docs/
    ├── SETUP_GUIDE.md         # Detailed setup guide
    ├── QUICK_REFERENCE.md     # Quick reference card
    └── DEPLOYMENT.md          # Deployment documentation
```

## 📚 Documentation

- [Setup Guide](docs/SETUP_GUIDE.md) - Detailed step-by-step instructions
- [Quick Reference](docs/QUICK_REFERENCE.md) - Quick lookup card
- [Deployment Guide](docs/DEPLOYMENT.md) - Deployment options and details

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

---

**Made with ❤️ for DTU students waiting for their convocation**
