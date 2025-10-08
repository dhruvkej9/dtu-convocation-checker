"""
FastAPI server to trigger the DTU Convocation Checker
Updated for Render deployment
"""

from fastapi import FastAPI, BackgroundTasks
from fastapi.responses import JSONResponse
import subprocess
import sys
import os
from datetime import datetime
from zoneinfo import ZoneInfo

app = FastAPI(
    title="DTU Convocation Checker API",
    description="API to trigger convocation portal checks",
    version="1.0.0"
)

@app.get("/")
async def root():
    """Root endpoint with API information"""
    return {
        "message": "DTU Convocation Checker API",
        "endpoints": {
            "/check": "Trigger convocation check",
            "/health": "Health check endpoint"
        }
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.now(ZoneInfo("Asia/Kolkata")).isoformat()
    }

def run_check_script():
    """Run the main.py script as a subprocess"""
    try:
        # Run main.py using the current Python interpreter
        result = subprocess.run(
            [sys.executable, "main.py"],
            capture_output=True,
            text=True,
            timeout=300  # 5 minute timeout
        )
        
        print("Script Output:")
        print(result.stdout)
        if result.stderr:
            print("Script Errors:")
            print(result.stderr)
            
        return {
            "success": result.returncode == 0,
            "stdout": result.stdout,
            "stderr": result.stderr,
            "return_code": result.returncode
        }
    except subprocess.TimeoutExpired:
        print("Script execution timed out")
        return {
            "success": False,
            "error": "Script execution timed out after 5 minutes"
        }
    except Exception as e:
        print(f"Error running script: {e}")
        return {
            "success": False,
            "error": str(e)
        }

@app.get("/check")
async def trigger_check(background_tasks: BackgroundTasks):
    """
    Trigger the convocation portal check
    
    This endpoint runs the main.py script in the background
    and returns immediately with a confirmation message.
    """
    timestamp = datetime.now(ZoneInfo("Asia/Kolkata"))
    
    # Add the check to background tasks so it runs async
    background_tasks.add_task(run_check_script)
    
    return JSONResponse(
        status_code=202,
        content={
            "status": "accepted",
            "message": "Convocation check started",
            "timestamp": timestamp.isoformat(),
            "note": "The check is running in the background. Results will be sent via Telegram."
        }
    )

@app.get("/check-sync")
async def trigger_check_sync():
    """
    Trigger the convocation portal check synchronously
    
    This endpoint runs the main.py script and waits for completion
    before returning the results.
    """
    timestamp = datetime.now(ZoneInfo("Asia/Kolkata"))
    
    # Run the check synchronously
    result = run_check_script()
    
    if result.get("success"):
        return {
            "status": "completed",
            "message": "Convocation check completed successfully",
            "timestamp": timestamp.isoformat(),
            "output": result.get("stdout", ""),
            "note": "Results have been sent via Telegram."
        }
    else:
        return JSONResponse(
            status_code=500,
            content={
                "status": "failed",
                "message": "Convocation check failed",
                "timestamp": timestamp.isoformat(),
                "error": result.get("error") or result.get("stderr", "Unknown error")
            }
        )

if __name__ == "__main__":
    import uvicorn
    # Get port from environment variable (Render provides this)
    # Default to 8000 for local development
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)