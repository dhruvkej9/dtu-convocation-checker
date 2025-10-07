import os
import sys
from datetime import datetime
from playwright.sync_api import sync_playwright
import requests

# Get Telegram credentials
bot_token = os.getenv('TELEGRAM_BOT_TOKEN')
chat_id = os.getenv('TELEGRAM_CHAT_ID')

print(bot_token, chat_id)
    