#!/usr/bin/env python3
# -------------------------------------------------------------------------
# File: start_services.py
# Project: MRCA - Mining Regulatory Compliance Assistant
# Author: Alexander Ricciardi
# Date: 2025-01-25 (Creation Date)
# Last Modified: 2025-01-25 
# File Path: start_services.py
# ------------------------------------------------------------------------

# --- Module Objective ---
# Simple standalone launcher for MRCA services that starts both backend and 
# frontend as completely detached background processes. Services will continue
# running even after this script exits, preventing connection issues.
# -------------------------------------------------------------------------

"""
MRCA Simple Service Launcher

Starts the MRCA Advanced Parallel Hybrid backend and frontend services as
completely detached background processes that survive script termination.
"""

import os
import sys
import time
import subprocess
import requests

# Configuration
BACKEND_PORT = 8000
FRONTEND_PORT = 8501
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))

def cleanup_existing_processes():
    """Clean up any existing MRCA processes."""
    print("🧹 Cleaning up existing processes...")
    try:
        # Kill existing processes
        subprocess.run(["pkill", "-f", "streamlit"], capture_output=True)
        subprocess.run(["pkill", "-f", "uvicorn"], capture_output=True)
        time.sleep(2)
        print("✅ Cleanup complete")
    except Exception as e:
        print(f"⚠️  Cleanup warning: {e}")

def start_backend():
    """Start the FastAPI backend as a detached process."""
    print("🚀 Starting backend server...")
    
    backend_cmd = [
        sys.executable, "-m", "uvicorn", 
        "backend.main:app",
        "--host", "0.0.0.0",
        "--port", str(BACKEND_PORT),
        "--reload"
    ]
    
    # Start as completely detached background process
    subprocess.Popen(
        backend_cmd,
        cwd=PROJECT_ROOT,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        stdin=subprocess.DEVNULL,
        preexec_fn=os.setsid if hasattr(os, 'setsid') else None,
        creationflags=subprocess.CREATE_NEW_PROCESS_GROUP if os.name == 'nt' else 0
    )
    
    print(f"✅ Backend starting on http://localhost:{BACKEND_PORT}")

def start_frontend():
    """Start the Streamlit frontend as a detached process."""
    print("🎨 Starting frontend server...")
    
    frontend_cmd = [
        sys.executable, "-m", "streamlit", "run",
        "frontend/bot.py",
        "--server.address=0.0.0.0",
        f"--server.port={FRONTEND_PORT}",
        "--server.headless=true",
        "--browser.serverAddress=localhost",
        f"--browser.serverPort={FRONTEND_PORT}",
        "--server.enableXsrfProtection=false",
        "--server.enableCORS=false"
    ]
    
    # Start as completely detached background process
    subprocess.Popen(
        frontend_cmd,
        cwd=PROJECT_ROOT,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        stdin=subprocess.DEVNULL,
        preexec_fn=os.setsid if hasattr(os, 'setsid') else None,
        creationflags=subprocess.CREATE_NEW_PROCESS_GROUP if os.name == 'nt' else 0
    )
    
    print(f"✅ Frontend starting on http://localhost:{FRONTEND_PORT}")

def wait_for_services():
    """Wait for both services to become healthy."""
    print("⏳ Waiting for services to start...")
    
    max_attempts = 30
    for attempt in range(max_attempts):
        try:
            # Check backend
            backend_response = requests.get(f"http://localhost:{BACKEND_PORT}/health", timeout=2)
            frontend_response = requests.get(f"http://localhost:{FRONTEND_PORT}/_stcore/health", timeout=2)
            
            if backend_response.status_code == 200 and frontend_response.status_code == 200:
                print("✅ Both services are healthy!")
                return True
                
        except requests.RequestException:
            pass
        
        time.sleep(2)
        print(f"   Attempt {attempt + 1}/{max_attempts}...")
    
    print("⚠️  Services may still be starting...")
    return False

def print_access_info():
    """Print service access information."""
    print("\n" + "="*80)
    print("🎉 MRCA Advanced Parallel Hybrid Services Started!")
    print("="*80)
    print("Service URLs:")
    print(f"    Frontend: http://localhost:{FRONTEND_PORT}")
    print(f"    Backend:  http://localhost:{BACKEND_PORT}")
    print(f"    API Docs: http://localhost:{BACKEND_PORT}/docs")
    print("")
    print("VS Code Dev Container Access:")
    print("   1. Open the 'PORTS' tab in VS Code (bottom panel)")
    print(f"   2. Find ports {FRONTEND_PORT} and {BACKEND_PORT}")
    print(f"   3. Right-click port {FRONTEND_PORT} → 'Open in Browser'")
    print(f"   4. If ports not visible, click 'Add Port' and add {FRONTEND_PORT}")
    print("")
    print("Advanced Parallel Hybrid Technology Ready!")
    print("   - Dual AI processing modes")
    print("   - 4 fusion strategies available")
    print("   - Neo4j knowledge graph integration")
    print("")
    print("🔗 Services are running as detached background processes")
    print("   They will continue running even after closing this terminal")
    print("")
    print("To stop services later, run:")
    print("   pkill -f streamlit && pkill -f uvicorn")
    print("="*80)

def main():
    """Main launcher function."""
    print("MRCA Simple Service Launcher")
    print("="*50)
    
    try:
        cleanup_existing_processes()
        start_backend()
        time.sleep(3)  # Give backend time to start
        start_frontend()
        
        # Wait for services
        wait_for_services()
        print_access_info()
        
        print("\n✅ Launch complete! Services are running in the background.")
        print("   This script can now be safely closed.")
        
    except Exception as e:
        print(f"❌ Error starting services: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 