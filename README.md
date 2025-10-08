# 🎓 DTU Convocation Checker - Automated Multi-Roll Number Monitor

An automated system that checks the DTU Convocation portal twice daily for multiple roll number variations and sends notifications via Telegram with screenshots.

## ✅ Status: TESTED AND WORKING!

The script has been tested successfully and is ready to deploy to GitHub Actions.

## 📋 What This Does

- Automatically logs into the DTU Convocation portal
- Checks **multiple roll number variations** (e.g., with/without leading zeros)
- Runs **twice daily** at 2 PM and 10 PM IST
- Sends **Telegram notifications** with screenshots
- **Completely FREE** - uses GitHub Actions (no credit card required)

## 🚀 Complete Setup Guide

### Step 1: Fork This Repository

1. Click the **"Fork"** button at the top right of this page
2. This creates your own copy of the repository

### Step 2: Set Up Telegram Bot (Your Notification Channel)

First, we need to create a way for the automation to reach you. Telegram is perfect because it's free, reliable, and easy to set up.

**Creating your Telegram bot:**
1. Open Telegram and search for "BotFather" (the official bot creation tool)
2. Start a chat and send the command `/newbot`
3. Give your bot a name (like "DTU Convocation Monitor")
4. Give it a username (must end in 'bot', like "dtu_convocation_check_bot")
5. BotFather will give you a **token** that looks like `1234567890:ABCdefGHIjklMNOpqrsTUVwxyz`. Save this carefully.

**Getting your Chat ID:**
1. Search for your new bot in Telegram and start a conversation
2. Send any message to it (like "Hello")
3. Open this URL in your browser: `https://api.telegram.org/bot<YOUR_BOT_TOKEN>/getUpdates`
   (Replace `<YOUR_BOT_TOKEN>` with your actual token)
4. Look for `"chat":{"id":` followed by a number. That's your **chat ID**. Save it.

### Step 3: Add GitHub Secrets

This is where you'll securely store your sensitive information. GitHub Secrets are encrypted and never exposed in logs or screenshots, which keeps your credentials completely safe.

1. In your repository, click on "Settings" (top menu)
2. In the left sidebar, click "Secrets and variables" → "Actions"
3. Click "New repository secret" for each of the following:

**Create these 5 secrets:**

| Secret Name | Value | Example |
|------------|-------|---------|
| `STUDENT_NAME` | Your name in CAPITALS | `DHRUV KEJRWAL` |
| `ROLL_NUMBERS` | Comma-separated roll numbers | `2K21/MC/053, 2K21/MC/53` |
| `DATE_OF_BIRTH` | Date in dd-mm-yyyy format | `19-07-2000` |
| `TELEGRAM_BOT_TOKEN` | Your bot token from [Step 2](#step-2-set-up-telegram-bot-your-notification-channel) | `123456789:ABC...` |
| `TELEGRAM_CHAT_ID` | Your chat ID from [Step 2](#step-2-set-up-telegram-bot-your-notification-channel) | `123456789` |


**How to add each secret:**
- Click "New repository secret"
- Enter the name exactly as shown above (case-sensitive!)
- Paste the value
- Click "Add secret"
- Repeat for all 5 secrets

**Important Notes:**
- For `ROLL_NUMBERS`: Separate multiple roll numbers with commas
- Example: `2K21/MC/053, 2K21/MC/53` (this checks both variations)
- Name must be in CAPITALS exactly as shown on portal
- Date format must be dd-mm-yyyy (e.g., 19-07-2000)

### Step 4: Enable GitHub Actions

1. Go to the **Actions** tab in your repository
2. Click **"I understand my workflows, go ahead and enable them"**
3. The automation is now active!

### Step 5: Test Your Automation

Before waiting for the scheduled runs, let's test it immediately to make sure everything works:

1. Go to the "Actions" tab in your repository
2. Click on "DTU Convocation Checker" in the left sidebar
3. Click the "Run workflow" button on the right
4. Click the green "Run workflow" button in the dropdown
5. Wait about 1-2 minutes, then refresh the page
6. You should see a new workflow run appear
7. Click on it to see the progress
8. Check your Telegram - you should receive a message with a screenshot!

## 📱 What You'll Receive

You'll get a Telegram message like this:

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

Automated check running twice daily at 9 AM and 6 PM IST
```

Plus screenshots of each check!

## ⏰ Schedule

The workflow runs automatically **twice daily**:

- **2:00 PM IST** (8:30 AM UTC) – Afternoon check  
- **10:00 PM IST** (4:30 PM UTC) – Evening check

You can also trigger it **manually anytime** from the GitHub Actions tab.

💡 **Tip:** Learn more about cron syntax and customize schedules at [Crontab Guru](https://crontab.guru/#30_*_*_*).

## 🔧 Troubleshooting

### Not receiving notifications?

1. **Check your bot**: Send a message to your bot on Telegram first
2. **Verify secrets**: Make sure all 5 secrets are added correctly
3. **Check Actions tab**: Look for any error messages in the workflow runs
4. **Date format**: Ensure it's dd-mm-yyyy (e.g., 09-02-2004, not 9-2-2004)

### Want to check more roll numbers?

Just add them to the `ROLL_NUMBERS` secret, separated by commas:
```
2K21/MC/053, 2K21/MC/53, 2K21/MC/0053
```

### Want to change the schedule?

Edit `.github/workflows/check_convocation.yml`:
```yaml
schedule:
  - cron: '30 8 * * *'   # 2:00 PM IST
  - cron: '30 16 * * *'  # 10:00 PM IST
```

Use [Crontab Guru](https://crontab.guru/) to create custom schedules.

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

---

**Made with ❤️ for DTU students waiting for their convocation**
dtu-convocation-checker
