"""
DTU Convocation Portal Checker
This script automates login to DTU convocation portal and checks status
"""

import os
import sys
from datetime import datetime
from playwright.sync_api import sync_playwright
import requests
import base64

def send_telegram_message(bot_token, chat_id, message, screenshot_path=None):
    """
    Sends a message to Telegram, optionally with a screenshot
    
    Args:
        bot_token: Your Telegram bot token
        chat_id: Your Telegram chat ID
        message: The text message to send
        screenshot_path: Path to screenshot file (optional)
    """
    try:
        # First send the text message
        url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
        data = {
            "chat_id": chat_id,
            "text": message,
            "parse_mode": "HTML"
        }
        response = requests.post(url, data=data)
        
        # If we have a screenshot, send it as a photo
        if screenshot_path and os.path.exists(screenshot_path):
            url = f"https://api.telegram.org/bot{bot_token}/sendPhoto"
            with open(screenshot_path, 'rb') as photo:
                files = {'photo': photo}
                data = {'chat_id': chat_id}
                requests.post(url, data=data, files=files)
        
        return response.json()
    except Exception as e:
        print(f"Error sending Telegram message: {e}")
        return None

def check_convocation_portal():
    """
    Main function that checks the DTU convocation portal
    Returns: tuple of (status_message, screenshot_path)
    """
    # Get credentials from environment variables (kept secure in GitHub Secrets)
    name = os.getenv('STUDENT_NAME')
    roll_number = os.getenv('ROLL_NUMBER')
    dob = os.getenv('DATE_OF_BIRTH')
    
    # Validate that we have all required credentials
    if not all([name, roll_number, dob]):
        return "❌ ERROR: Missing credentials in GitHub Secrets", None
    
    print(f"Starting check at {datetime.now()}")
    print(f"Checking for Roll Number: {roll_number}")
    
    screenshot_path = "screenshot.png"
    status_message = ""
    page_title = ""
    
    try:
        # Start Playwright - this launches a real browser in the background
        with sync_playwright() as p:
            # Launch browser in headless mode (no visible window)
            # We use chromium because it's lightweight and reliable
            browser = p.chromium.launch(headless=True)
            
            # Create a new browser context (like an incognito window)
            context = browser.new_context(
                viewport={'width': 1280, 'height': 720},
                user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            )
            
            # Open a new page
            page = context.new_page()
            
            print("Navigating to DTU convocation portal...")
            # Go to the login page
            page.goto('https://www.convocation.dtu.ac.in/index.php', 
                     wait_until='networkidle', timeout=30000)
            
            # Get the page title
            page_title = page.title()
            print(f"Page title: {page_title}")
            
            # Fill in the login form
            # We use fill() which is more reliable than type()
            print("Filling in credentials...")
            
            # Fill Name field (looking for input with placeholder "Enter Name")
            page.fill('input[placeholder="Enter Name"]', name)
            
            # Fill Roll Number field
            page.fill('input[placeholder="Enter Roll No"]', roll_number)
            
            # Fill Date of Birth field
            page.fill('input[placeholder="Date of Birth"]', dob)
            
            # Wait a moment for the form to be ready
            page.wait_for_timeout(1000)
            
            print("Clicking login button...")
            # Click the Log In button and wait for navigation
            page.click('button:has-text("Log In")')
            
            # Wait for the page to load after login
            # This is crucial - we wait for network to be idle
            page.wait_for_load_state('networkidle', timeout=15000)
            
            # Additional wait to ensure dynamic content loads
            page.wait_for_timeout(2000)
            
            # Get the updated page title after login
            page_title = page.title()
            
            # Check what message is displayed on the page
            page_content = page.content()
            
            # Look for common status messages
            if "Roll No Not Found" in page_content:
                status_message = "⏳ <b>Roll No Not Found</b>\n\nYour roll number is not yet in the system. This is normal before convocation details are released."
            elif "Roll No Found" in page_content or "Convocation" in page_content:
                status_message = "🎉 <b>ROLL NUMBER FOUND!</b>\n\nYour convocation details are now available! Check the portal."
            elif "Invalid" in page_content or "Error" in page_content:
                status_message = "⚠️ <b>Error or Invalid Credentials</b>\n\nThere might be an issue with the credentials or the portal."
            else:
                # If we can't determine the status, just report what we see
                status_message = "ℹ️ <b>Status Unknown</b>\n\nThe portal responded but the status is unclear. Check the screenshot."
            
            print(f"Status detected: {status_message}")
            
            # Take a screenshot of the entire page
            print("Capturing screenshot...")
            page.screenshot(path=screenshot_path, full_page=True)
            
            # Close browser
            browser.close()
            
            return status_message, screenshot_path, page_title
            
    except Exception as e:
        error_msg = f"❌ <b>Error occurred:</b>\n\n{str(e)}"
        print(f"Error: {e}")
        return error_msg, None, "Error"

def main():
    """
    Main execution function
    """
    print("=" * 50)
    print("DTU CONVOCATION CHECKER STARTED")
    print("=" * 50)
    
    # Get Telegram credentials
    bot_token = os.getenv('TELEGRAM_BOT_TOKEN')
    chat_id = os.getenv('TELEGRAM_CHAT_ID')
    
    if not bot_token or not chat_id:
        print("ERROR: Telegram credentials not found in secrets")
        sys.exit(1)
    
    # Run the check
    status_message, screenshot_path, page_title = check_convocation_portal()
    
    # Prepare the full message
    current_time = datetime.now().strftime("%d %B %Y, %I:%M %p IST")
    
    full_message = f"""
🎓 <b>DTU Convocation Portal Check</b>

📅 <b>Check Time:</b> {current_time}
📄 <b>Page Title:</b> {page_title}

{status_message}

<i>This is an automated check. The portal is checked twice daily.</i>
"""
    
    # Send notification
    print("Sending Telegram notification...")
    result = send_telegram_message(bot_token, chat_id, full_message, screenshot_path)
    
    if result:
        print("✓ Notification sent successfully!")
    else:
        print("✗ Failed to send notification")
    
    print("=" * 50)
    print("CHECK COMPLETED")
    print("=" * 50)

if __name__ == "__main__":
    main()
