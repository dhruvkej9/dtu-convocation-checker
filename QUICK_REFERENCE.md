# ⚡ Quick Reference - DTU Convocation Checker

## 🎯 What You Need

| Item | Value | Where to Get |
|------|-------|--------------|
| **STUDENT_NAME** | `DHRUV KEJRWAL` | Your name in CAPITALS |
| **ROLL_NUMBERS** | `2K21/MC/053, 2K21/MC/53` | Your roll number variations |
| **DATE_OF_BIRTH** | `09-02-2004` | dd-mm-yyyy format |
| **TELEGRAM_BOT_TOKEN** | `123456:ABC...` | @BotFather on Telegram |
| **TELEGRAM_CHAT_ID** | `123456789` | @userinfobot on Telegram |

## 🚀 5-Minute Setup

1. Create Telegram bot → @BotFather → `/newbot` → Save token
2. Get Chat ID → @userinfobot → Save number
3. **START your bot** → Search your bot → Click START
4. Fork repository → Click Fork button
5. Add 5 secrets → Settings → Secrets → Actions → New secret
6. Enable Actions → Actions tab → Enable
7. Test → Actions → Run workflow

## 📱 Telegram Bot Setup (IMPORTANT!)

```
Step 1: @BotFather
        ↓
Step 2: /newbot → Follow prompts
        ↓
Step 3: Copy TOKEN
        ↓
Step 4: @userinfobot
        ↓
Step 5: Copy CHAT_ID
        ↓
Step 6: Find YOUR bot → Click START ⚠️ MUST DO THIS!
```

## 🔐 GitHub Secrets to Add

```
Repository → Settings → Secrets and variables → Actions → New repository secret
```

Add 5 secrets (click New repository secret for each):

1. Name: `STUDENT_NAME` → Value: `DHRUV KEJRWAL`
2. Name: `ROLL_NUMBERS` → Value: `2K21/MC/053, 2K21/MC/53`
3. Name: `DATE_OF_BIRTH` → Value: `09-02-2004`
4. Name: `TELEGRAM_BOT_TOKEN` → Value: `<your token>`
5. Name: `TELEGRAM_CHAT_ID` → Value: `<your chat id>`

## ⏰ When It Runs

- 🌅 9:00 AM IST daily
- 🌆 6:00 PM IST daily
- 🔧 Manual: Actions tab → Run workflow

## 📊 Status Messages

| Message | Meaning |
|---------|---------|
| ❌ Roll No Not Found | Normal - keep waiting |
| ✅ ROLL NUMBER FOUND | 🎉 Check portal NOW! |
| ⚠️ Invalid Credentials | Fix your secrets |
| ❌ Error | Check Actions logs |

## 🐛 Quick Fixes

### No notifications?
→ Did you START your bot? (Search your bot → Click START)

### SSL Error?
→ Already fixed in code with browser args!

### Wrong date format?
→ Must be `09-02-2004` (with leading zeros)

### Name format?
→ Must be CAPITALS: `DHRUV KEJRWAL`

## 📂 Project Structure

```
dtu-convocation-checker/
├── check_convocation.py          # Main script
├── .github/workflows/
│   └── check_convocation.yml     # GitHub Actions workflow
├── requirements.txt               # Python dependencies
├── README.md                      # Full documentation
├── SETUP_GUIDE.md                # Detailed setup guide
├── CHANGES.md                    # What was fixed
└── QUICK_REFERENCE.md            # This file!
```

## 💻 Commands

### Test Locally:
```bash
./test_local.sh
```

### Install Dependencies:
```bash
pip install -r requirements.txt
playwright install chromium
```

### Run Manually:
```bash
export STUDENT_NAME="DHRUV KEJRWAL"
export ROLL_NUMBERS="2K21/MC/053, 2K21/MC/53"
export DATE_OF_BIRTH="09-02-2004"
export TELEGRAM_BOT_TOKEN="your_token"
export TELEGRAM_CHAT_ID="your_chat_id"
python3 check_convocation.py
```

## 🎓 Multiple Students

Each student needs:
1. Fork the repo
2. Add THEIR secrets
3. Enable Actions

## 💰 Cost

- GitHub Actions: FREE (2000 min/month)
- Telegram: FREE forever
- Total: **$0.00** 🎉

## ⚙️ Customization

### Check more often:
Edit `.github/workflows/check_convocation.yml`:
```yaml
schedule:
  - cron: '0 */4 * * *'  # Every 4 hours
```

### Check more roll numbers:
Update `ROLL_NUMBERS` secret:
```
2K21/MC/053, 2K21/MC/53, 2K21/MC/0053
```

## 🆘 Help

1. Check Actions tab for logs
2. Verify all 5 secrets exist
3. Confirm you started your bot
4. Try manual run first

## ✅ Final Checklist

- [ ] Created Telegram bot (@BotFather)
- [ ] Got Chat ID (@userinfobot)
- [ ] **Started the bot** (sent /start)
- [ ] Forked repository
- [ ] Added 5 secrets
- [ ] Enabled Actions
- [ ] Tested with "Run workflow"
- [ ] Received Telegram message

---

**All set? You'll get notifications twice daily! 🎓**
