"""
Render App Wake-Up Script using Playwright
This script wakes up the Render app by hitting the health endpoint
and waiting for the app to respond (up to 60 seconds).
"""

import asyncio
import sys
from playwright.async_api import async_playwright, TimeoutError as PlaywrightTimeoutError

# Default URL to wake up
DEFAULT_URL = "https://dtu-convocation-checker.onrender.com/health"

async def wakeup_render_app(url: str = DEFAULT_URL, timeout_seconds: int = 60) -> dict:
    """
    Wake up the Render app by navigating to the health endpoint
    and waiting for a JSON response.
    
    Args:
        url: The health endpoint URL to hit
        timeout_seconds: Maximum time to wait for the app to wake up (default: 60s)
    
    Returns:
        dict with status, message, and response data
    """
    result = {
        "success": False,
        "message": "",
        "response": None,
        "time_taken": 0
    }
    
    print(f"🚀 Starting wake-up process for: {url}")
    print(f"⏱️  Timeout set to: {timeout_seconds} seconds")
    print("-" * 50)
    
    async with async_playwright() as p:
        browser = await p.chromium.launch(
            headless=True,
            args=[
                '--no-sandbox',
                '--disable-setuid-sandbox',
                '--disable-dev-shm-usage',
                '--disable-gpu'
            ]
        )
        
        context = await browser.new_context(
            ignore_https_errors=True
        )
        
        page = await context.new_page()
        
        try:
            import time
            start_time = time.time()
            
            print("📡 Navigating to health endpoint...")
            
            # Navigate with extended timeout for cold starts
            response = await page.goto(
                url,
                wait_until='domcontentloaded',
                timeout=timeout_seconds * 1000  # Convert to milliseconds
            )
            
            # Wait for content to be fully loaded
            await page.wait_for_load_state('networkidle', timeout=timeout_seconds * 1000)
            
            end_time = time.time()
            time_taken = round(end_time - start_time, 2)
            result["time_taken"] = time_taken
            
            # Get the page content
            content = await page.content()
            
            # Check if we got a valid response
            if response and response.status == 200:
                # Try to extract JSON from the page
                try:
                    # The JSON is typically wrapped in a <pre> tag or directly in body
                    json_text = await page.locator('body').inner_text()
                    import json
                    result["response"] = json.loads(json_text)
                    result["success"] = True
                    result["message"] = f"✅ App woke up successfully in {time_taken}s!"
                    print(result["message"])
                    print(f"📄 Response: {result['response']}")
                except json.JSONDecodeError:
                    # Even if JSON parsing fails, the app is awake
                    result["success"] = True
                    result["message"] = f"✅ App responded in {time_taken}s (non-JSON response)"
                    result["response"] = content[:500]  # First 500 chars
                    print(result["message"])
            else:
                status_code = response.status if response else "No response"
                result["message"] = f"⚠️ App responded with status: {status_code}"
                print(result["message"])
                
        except PlaywrightTimeoutError:
            result["message"] = f"❌ Timeout after {timeout_seconds}s - App may need manual intervention"
            print(result["message"])
        except Exception as e:
            result["message"] = f"❌ Error: {str(e)}"
            print(result["message"])
        finally:
            await browser.close()
    
    return result


async def wakeup_with_retry(url: str = DEFAULT_URL, max_retries: int = 3, timeout_seconds: int = 60) -> dict:
    """
    Wake up the Render app with retry logic.
    
    Args:
        url: The health endpoint URL
        max_retries: Maximum number of retry attempts
        timeout_seconds: Timeout for each attempt
    
    Returns:
        dict with final status
    """
    for attempt in range(1, max_retries + 1):
        print(f"\n🔄 Attempt {attempt}/{max_retries}")
        result = await wakeup_render_app(url, timeout_seconds)
        
        if result["success"]:
            return result
        
        if attempt < max_retries:
            print(f"⏳ Waiting 5 seconds before retry...")
            await asyncio.sleep(5)
    
    return result


def main():
    """
    Main entry point for the wake-up script.
    Can be run directly or imported as a module.
    """
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Wake up Render app by hitting the health endpoint"
    )
    parser.add_argument(
        "--url",
        default=DEFAULT_URL,
        help=f"Health endpoint URL (default: {DEFAULT_URL})"
    )
    parser.add_argument(
        "--timeout",
        type=int,
        default=60,
        help="Timeout in seconds (default: 60)"
    )
    parser.add_argument(
        "--retries",
        type=int,
        default=1,
        help="Number of retry attempts (default: 1)"
    )
    
    args = parser.parse_args()
    
    print("=" * 50)
    print("🌐 RENDER APP WAKE-UP UTILITY")
    print("=" * 50)
    
    if args.retries > 1:
        result = asyncio.run(wakeup_with_retry(args.url, args.retries, args.timeout))
    else:
        result = asyncio.run(wakeup_render_app(args.url, args.timeout))
    
    print("\n" + "=" * 50)
    print("📊 FINAL RESULT")
    print("=" * 50)
    print(f"Success: {result['success']}")
    print(f"Message: {result['message']}")
    print(f"Time taken: {result['time_taken']}s")
    print("=" * 50)
    
    # Exit with appropriate code
    sys.exit(0 if result["success"] else 1)


if __name__ == "__main__":
    main()
