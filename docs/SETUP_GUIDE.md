# 🚀 Complete Setup Guide - DTU Convocation Checker

## 📋 Quick Overview
This automation will check the DTU Convocation portal twice daily for your roll numbers and send you notifications via Telegram with screenshots.

---

## ✅ Step-by-Step Setup (10 minutes)

### **Step 1: Create Telegram Bot (2 minutes)**

1. Open Telegram and search for **@BotFather**
2. Send the command: `/newbot`
3. Follow the prompts:
   - Give your bot a name (e.g., "DTU Convocation Checker")
   - Choose a username (must end in 'bot', e.g., "dtu_conv_checker_bot")
4. **SAVE THE TOKEN** - It looks like: `1234567890:ABCdefGHIjklMNOpqrsTUVwxyz`

### **Step 2: Get Your Chat ID (1 minute)**

1. Search for **@userinfobot** on Telegram
2. Start a chat with it by clicking "START"
3. It will reply with your user information
4. **SAVE YOUR CHAT ID** - It's a number like: `123456789`

### **Step 3: Start Your Bot (Important!)**

1. Go back to Telegram and search for your bot username (from Step 1)
2. Click **START** or send `/start` to your bot
3. This is required for the bot to send you messages

### **Step 4: Fork This Repository (1 minute)**

1. Click the **"Fork"** button at the top right of this GitHub page
2. This creates your personal copy of the project

### **Step 5: Add GitHub Secrets (5 minutes)**

1. Go to your forked repository
2. Click **Settings** (top menu)
3. In the left sidebar: **Secrets and variables** → **Actions**
4. Click **"New repository secret"** button
5. Add these **5 secrets** one by one:

#### Secret 1: STUDENT_NAME
- **Name:** `STUDENT_NAME`
- **Value:** `DHRUV KEJRWAL` (your name in CAPITALS)

#### Secret 2: ROLL_NUMBERS
- **Name:** `ROLL_NUMBERS`
- **Value:** `2K21/MC/053, 2K21/MC/53`
- Note: Separate multiple roll numbers with commas and spaces

#### Secret 3: DATE_OF_BIRTH
- **Name:** `DATE_OF_BIRTH`
- **Value:** `09-02-2004`
- Format: dd-mm-yyyy (use leading zeros)

#### Secret 4: TELEGRAM_BOT_TOKEN
- **Name:** `TELEGRAM_BOT_TOKEN`
- **Value:** (paste the token from Step 1)

#### Secret 5: TELEGRAM_CHAT_ID
- **Name:** `TELEGRAM_CHAT_ID`
- **Value:** (paste the chat ID from Step 2)

### **Step 6: Enable GitHub Actions (1 minute)**

1. Go to the **Actions** tab in your repository
2. If you see a message about workflows, click **"I understand my workflows, go ahead and enable them"**
3. You should see the workflow: "DTU Convocation Checker"

### **Step 7: Test It! (2 minutes)**

1. In the **Actions** tab, click on **"DTU Convocation Checker"**
2. Click **"Run workflow"** (dropdown button on the right)
3. Click the green **"Run workflow"** button
4. Wait 2-3 minutes and check your Telegram!

---

## 📱 What You'll Receive

Every check, you'll get a message like this:

```
🎓 DTU Convocation Multi-Check Report

📅 Check Time: 07 October 2025, 09:00 AM IST
👤 Student: DHRUV KEJRWAL
🔢 Roll Numbers Checked: 2

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Check #1: 2K21/MC/053

❌ Roll No Not Found
Your roll number is not yet in the convocation system.

📄 Convocation: Convocation 2024

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Check #2: 2K21/MC/53

❌ Roll No Not Found
Your roll number is not yet in the convocation system.

📄 Convocation: Convocation 2024

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

💡 What This Means:
• If both show "Not Found": Normal before convocation announcement
• If one is "Found": Use that roll number format on the portal
• If results differ: The portal may prefer one format over the other

Automated check running twice daily at 9 AM and 6 PM IST
```

Plus **2 screenshots** (one for each roll number)!

---

## ⏰ Automatic Schedule

The checker runs automatically:
- **9:00 AM IST** every day
- **6:00 PM IST** every day

You can also run it manually anytime from the Actions tab.

---

## 🔧 Troubleshooting

### ❌ Not receiving messages?

**Problem:** Bot doesn't send messages  
**Solution:** 
1. Make sure you clicked "START" on your bot (Step 3)
2. Double-check your `TELEGRAM_BOT_TOKEN` and `TELEGRAM_CHAT_ID` in GitHub Secrets
3. Send any message to your bot first

### ❌ Workflow fails with SSL error?

**Problem:** `ERR_CERT_COMMON_NAME_INVALID`  
**Solution:** The code now handles this automatically with browser args. If it still fails, check the Actions logs.

### ❌ Invalid credentials error?

**Problem:** Shows "Invalid Credentials"  
**Solution:**
1. Check your name is in CAPITALS: `DHRUV KEJRWAL`
2. Check date format is dd-mm-yyyy: `09-02-2004` (with leading zeros)
3. Check roll numbers match the portal format

### ❌ Workflow doesn't run automatically?

**Problem:** No automatic checks  
**Solution:**
1. Make sure you enabled GitHub Actions (Step 6)
2. Check the workflow file exists: `.github/workflows/check_convocation.yml`
3. The first automatic run happens at the next scheduled time (9 AM or 6 PM IST)

---

## 🎯 Adding More Roll Numbers

To check more variations of your roll number:

1. Go to **Settings** → **Secrets and variables** → **Actions**
2. Click on `ROLL_NUMBERS`
3. Click **"Update"**
4. Add more roll numbers separated by commas:
   ```
   2K21/MC/053, 2K21/MC/53, 2K21/MC/0053
   ```

---

## 🔒 Security & Privacy

✅ All credentials are encrypted in GitHub Secrets  
✅ Bot token and chat ID are never exposed in code  
✅ Screenshots are deleted after 7 days  
✅ Only you can see your notifications  
✅ No data is stored anywhere  

---

## 💰 Cost

**100% FREE!**
- GitHub Actions: 2000 free minutes/month (you'll use ~20 minutes/month)
- Telegram: Free forever
- No credit card needed anywhere

---

## 📊 Understanding the Results

| Status | Meaning | Action Needed |
|--------|---------|---------------|
| ❌ Roll No Not Found | Normal before announcement | Keep waiting |
| ✅ ROLL NUMBER FOUND | Your data is available! | Login to portal immediately |
| ⚠️ Invalid Credentials | Wrong name/DOB/format | Check your secrets |
| ❌ Error | Technical issue | Check Actions logs |

---

## 🔄 Changing the Schedule

To run at different times, edit `.github/workflows/check_convocation.yml`:

```yaml
schedule:
  - cron: '30 3 * * *'   # 9:00 AM IST (3:30 AM UTC)
  - cron: '30 12 * * *'  # 6:00 PM IST (12:30 PM UTC)
```

Use [Crontab Guru](https://crontab.guru/) to create custom schedules.

**Examples:**
- Every 6 hours: `0 */6 * * *`
- 3 times daily (8 AM, 2 PM, 8 PM IST): `30 2,8,14 * * *`
- Every hour: `0 * * * *`

---

## 📝 Important Notes

✅ **Name Format:** Must be CAPITALS exactly as on portal  
✅ **Date Format:** Must be dd-mm-yyyy (e.g., 09-02-2004, not 9-2-2004)  
✅ **Roll Numbers:** Can check unlimited variations  
✅ **First Message:** Start your bot first!  

---

## 🆘 Still Need Help?

1. Check the **Actions** tab for error logs
2. Make sure all 5 secrets are added correctly
3. Verify you started your Telegram bot
4. Try running manually first (Run workflow button)

---

## 🎓 For Other DTU Students

Want to use this for your roll number?

1. Fork this repository
2. Follow Steps 1-7 above
3. Use **YOUR** name, roll numbers, and DOB

That's it! The system is ready to notify you the moment your convocation details are available.

---

**Good luck with your convocation! 🎓**
