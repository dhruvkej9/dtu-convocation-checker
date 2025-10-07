"""
DTU Convocation Portal Checker - Multi Roll Number Version
This script automates login to DTU convocation portal and checks multiple roll numbers
"""

import os
import sys
from datetime import datetime
from playwright.sync_api import sync_playwright
import requests

def send_telegram_message(bot_token, chat_id, message, screenshot_paths=None):
    """
    Sends a message to Telegram, optionally with multiple screenshots
    
    Args:
        bot_token: Your Telegram bot token
        chat_id: Your Telegram chat ID
        message: The text message to send
        screenshot_paths: List of screenshot file paths (optional)
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
        
        # If we have screenshots, send them as a media group
        if screenshot_paths:
            for i, screenshot_path in enumerate(screenshot_paths):
                if os.path.exists(screenshot_path):
                    url = f"https://api.telegram.org/bot{bot_token}/sendPhoto"
                    with open(screenshot_path, 'rb') as photo:
                        files = {'photo': photo}
                        caption = f"Screenshot {i+1} of {len(screenshot_paths)}"
                        data = {'chat_id': chat_id, 'caption': caption}
                        requests.post(url, data=data, files=files)
        
        return response.json()
    except Exception as e:
        print(f"Error sending Telegram message: {e}")
        return None

def check_single_roll_number(page, name, roll_number, dob):
    """
    Checks a single roll number on the portal
    
    Args:
        page: Playwright page object
        name: Student name
        roll_number: Roll number to check
        dob: Date of birth
        
    Returns:
        Dictionary with status information
    """
    result = {
        'roll_number': roll_number,
        'status': '',
        'page_title': '',
        'screenshot_path': None,
        'success': False
    }
    
    try:
        print(f"\n{'='*50}")
        print(f"Checking Roll Number: {roll_number}")
        print(f"{'='*50}")
        
        # Navigate to the portal fresh for each check
        print("Navigating to portal...")
        page.goto('https://www.convocation.dtu.ac.in/index.php', 
                 wait_until='domcontentloaded', timeout=30000)
        
        # Wait for page to be ready
        page.wait_for_timeout(2000)
        
        # Fill in the login form
        print("Filling credentials...")
        page.fill('input[placeholder="Enter Name"]', name)
        page.wait_for_timeout(500)
        page.fill('input[placeholder="Enter Roll No"]', roll_number)
        page.wait_for_timeout(500)
        page.fill('input[placeholder="Date of Birth"]', dob)
        
        # Wait a moment for form to be ready
        page.wait_for_timeout(1000)
        
        # Click login and wait for response
        print("Logging in...")
        # Note: The page doesn't navigate, it updates content in place
        # Try multiple selectors for the login button
        try:
            # Use click with no_wait_after to handle pages that may or may not navigate
            page.locator('input[type="submit"][value="Log In"]').click(timeout=5000)
        except:
            try:
                page.locator('button:has-text("Log In")').click(timeout=5000)
            except:
                page.locator('#signin').click(timeout=5000)
        # Wait for the response to appear (page updates without full reload)
        page.wait_for_timeout(4000)
        
        # Get page information
        # Extract the convocation title from the h2 heading (e.g., "Convocation 2024")
        try:
            convocation_title = page.locator('h2').first.inner_text()
            result['page_title'] = convocation_title
        except:
            result['page_title'] = page.title()  # Fallback to browser title
        
        page_content = page.content()
        
        # Analyze the response to determine status
        # The portal returns different messages based on whether your roll number is found
        if "Roll No Not Found" in page_content:
            result['status'] = "❌ Roll No Not Found"
            result['status_detail'] = "Your roll number is not yet in the convocation system."
        elif "Roll No Found" in page_content or "successfully" in page_content.lower():
            result['status'] = "✅ ROLL NUMBER FOUND!"
            result['status_detail'] = "Your convocation details are available! Check the portal immediately."
        elif "Invalid" in page_content or "incorrect" in page_content.lower():
            result['status'] = "⚠️ Invalid Credentials"
            result['status_detail'] = "The credentials might be incorrect or there's an issue with this roll number format."
        else:
            result['status'] = "❔ Status Unknown"
            result['status_detail'] = "The portal responded but the status is unclear."
        
        # Take a screenshot with a unique name for this roll number
        # We sanitize the roll number to create a valid filename by replacing slashes
        safe_roll_number = roll_number.replace('/', '_')
        screenshot_path = f"screenshot_{safe_roll_number}.png"
        page.screenshot(path=screenshot_path, full_page=True)
        result['screenshot_path'] = screenshot_path
        
        result['success'] = True
        print(f"✓ Check completed: {result['status']}")
        
    except Exception as e:
        result['status'] = "❌ Error"
        result['status_detail'] = f"An error occurred while checking: {str(e)}"
        print(f"✗ Error checking {roll_number}: {e}")
    
    return result

def check_convocation_portal():
    """
    Main function that checks the DTU convocation portal for multiple roll numbers
    Returns: List of results for each roll number checked
    """
    # Get credentials from environment variables
    name = os.getenv('STUDENT_NAME')
    roll_numbers_str = os.getenv('ROLL_NUMBERS')  # Now expects comma-separated values
    dob = os.getenv('DATE_OF_BIRTH')
    
    # Validate credentials
    if not all([name, roll_numbers_str, dob]):
        return [{
            'roll_number': 'N/A',
            'status': '❌ Configuration Error',
            'status_detail': 'Missing credentials in GitHub Secrets. Check STUDENT_NAME, ROLL_NUMBERS, and DATE_OF_BIRTH.',
            'page_title': 'Error',
            'screenshot_path': None,
            'success': False
        }]
    
    # Parse the comma-separated roll numbers into a list
    # This allows you to check as many roll number variations as you need
    roll_numbers = [rn.strip() for rn in roll_numbers_str.split(',')]
    
    print(f"Starting checks at {datetime.now()}")
    print(f"Student: {name}")
    print(f"Roll numbers to check: {len(roll_numbers)}")
    for rn in roll_numbers:
        print(f"  - {rn}")
    
    results = []
    
    try:
        # Start Playwright and create a browser instance
        # We'll reuse the same browser for all checks to be more efficient
        with sync_playwright() as p:
            # Launch browser with args to handle SSL issues
            browser = p.chromium.launch(
                headless=True,
                args=['--ignore-certificate-errors', '--ignore-certificate-errors-spki-list']
            )
            context = browser.new_context(
                viewport={'width': 1280, 'height': 720},
                user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
                ignore_https_errors=True  # Handle SSL certificate issues
            )
            page = context.new_page()
            
            # Check each roll number sequentially
            # We do this one at a time to avoid overwhelming the portal
            for roll_number in roll_numbers:
                result = check_single_roll_number(page, name, roll_number, dob)
                results.append(result)
                
                # Small delay between checks to be respectful to the server
                if roll_number != roll_numbers[-1]:  # Not the last one
                    page.wait_for_timeout(2000)
            
            browser.close()
            
    except Exception as e:
        print(f"Critical error: {e}")
        results.append({
            'roll_number': 'All',
            'status': '❌ Critical Error',
            'status_detail': f"Failed to run checks: {str(e)}",
            'page_title': 'Error',
            'screenshot_path': None,
            'success': False
        })
    
    return results

def format_notification_message(results):
    """
    Creates a formatted message combining all check results
    
    Args:
        results: List of result dictionaries from checking each roll number
        
    Returns:
        Formatted HTML message string
    """
    current_time = datetime.now().strftime("%d %B %Y, %I:%M %p IST")
    
    # Start building the message with header
    message = f"""🎓 <b>DTU Convocation Multi-Check Report</b>

📅 <b>Check Time:</b> {current_time}
👤 <b>Student:</b> {os.getenv('STUDENT_NAME')}
🔢 <b>Roll Numbers Checked:</b> {len(results)}

"""
    
    # Add details for each roll number checked
    # This creates a clear, organized report showing the status of each variation
    for i, result in enumerate(results, 1):
        message += f"""━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
<b>Check #{i}: {result['roll_number']}</b>

{result['status']}
{result['status_detail']}

📄 <b>Convocation:</b> {result['page_title']}
"""
        
        # Add extra spacing between results for readability
        if i < len(results):
            message += "\n"
    
    # Add footer with helpful information
    message += f"""
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

💡 <b>What This Means:</b>
• If both show "Not Found": Normal before convocation announcement
• If one is "Found": Use that roll number format on the portal
• If results differ: The portal may prefer one format over the other

<i>Automated check running twice daily at 9 AM and 6 PM IST</i>
"""
    
    return message

def main():
    """
    Main execution function
    """
    print("=" * 60)
    print("DTU CONVOCATION MULTI-ROLL NUMBER CHECKER STARTED")
    print("=" * 60)
    
    # Get Telegram credentials
    bot_token = os.getenv('TELEGRAM_BOT_TOKEN')
    chat_id = os.getenv('TELEGRAM_CHAT_ID')
    
    if not bot_token or not chat_id:
        print("ERROR: Telegram credentials not found in secrets")
        sys.exit(1)
    
    # Run all checks
    results = check_convocation_portal()
    
    # Format the notification message
    message = format_notification_message(results)
    
    # Collect all screenshot paths that were successfully created
    screenshot_paths = [r['screenshot_path'] for r in results if r['screenshot_path']]
    
    # Send the notification with all screenshots
    print("\nSending Telegram notification...")
    send_result = send_telegram_message(bot_token, chat_id, message, screenshot_paths)
    
    if send_result:
        print("✓ Notification sent successfully!")
    else:
        print("✗ Failed to send notification")
    
    # Print summary to logs
    print("\n" + "=" * 60)
    print("CHECK SUMMARY")
    print("=" * 60)
    for result in results:
        print(f"{result['roll_number']}: {result['status']}")
    print("=" * 60)
    print("ALL CHECKS COMPLETED")
    print("=" * 60)

if __name__ == "__main__":
    main()
