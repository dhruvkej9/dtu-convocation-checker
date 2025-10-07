# 🎓 DTU Convocation Checker - Automated Multi-Roll Number Monitor

An automated system that checks the DTU Convocation portal twice daily for multiple roll number variations and sends notifications via Telegram with screenshots.

## ✅ Status: TESTED AND WORKING!

The script has been tested successfully and is ready to deploy to GitHub Actions.

## 📋 What This Does

- Automatically logs into the DTU Convocation portal
- Checks **multiple roll number variations** (e.g., with/without leading zeros)
- Runs **twice daily** at 9 AM and 6 PM IST
- Sends **Telegram notifications** with screenshots
- **Completely FREE** - uses GitHub Actions (no credit card required)

## 🚀 Complete Setup Guide

### Step 1: Fork This Repository

1. Click the **"Fork"** button at the top right of this page
2. This creates your own copy of the repository

### Step 2: Create a Telegram Bot

1. Open Telegram and search for **@BotFather**
2. Send `/newbot` command
3. Follow the prompts to create your bot
4. **Save the Bot Token** (looks like: `123456789:ABCdefGHIjklMNOpqrsTUVwxyz`)

### Step 3: Get Your Telegram Chat ID

1. Search for **@userinfobot** on Telegram
2. Start a chat with it
3. It will send you your **Chat ID** (looks like: `123456789`)
4. **Save this number**

### Step 4: Add GitHub Secrets

1. Go to your forked repository on GitHub
2. Click **Settings** → **Secrets and variables** → **Actions**
3. Click **"New repository secret"** and add these 5 secrets:

| Secret Name | Value | Example |
|------------|-------|---------|
| `STUDENT_NAME` | Your name in CAPITALS | `DHRUV KEJRWAL` |
| `ROLL_NUMBERS` | Comma-separated roll numbers | `2K21/MC/053, 2K21/MC/53` |
| `DATE_OF_BIRTH` | Date in dd-mm-yyyy format | `09-02-2004` |
| `TELEGRAM_BOT_TOKEN` | Your bot token from Step 2 | `123456789:ABC...` |
| `TELEGRAM_CHAT_ID` | Your chat ID from Step 3 | `123456789` |

**Important Notes:**
- For `ROLL_NUMBERS`: Separate multiple roll numbers with commas
- Example: `2K21/MC/053, 2K21/MC/53` (this checks both variations)
- Name must be in CAPITALS exactly as shown on portal
- Date format must be dd-mm-yyyy (e.g., 09-02-2004)

### Step 5: Enable GitHub Actions

1. Go to the **Actions** tab in your repository
2. Click **"I understand my workflows, go ahead and enable them"**
3. The automation is now active!

### Step 6: Test It (Optional)

1. Go to **Actions** tab
2. Click on **"DTU Convocation Checker"** workflow
3. Click **"Run workflow"** dropdown
4. Click the green **"Run workflow"** button
5. Wait a few minutes and check your Telegram for the notification

## 📱 What You'll Receive

You'll get a Telegram message like this:

```
🎓 DTU Convocation Multi-Check Report

📅 Check Time: 07 October 2025, 09:00 AM IST
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

The checker runs automatically:
- **9:00 AM IST** (3:30 AM UTC) - Morning check
- **6:00 PM IST** (12:30 PM UTC) - Evening check

You can also run it manually anytime from the Actions tab.

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
  - cron: '30 3 * * *'   # 9:00 AM IST
  - cron: '30 12 * * *'  # 6:00 PM IST
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
