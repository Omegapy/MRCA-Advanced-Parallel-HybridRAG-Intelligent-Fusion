#!/usr/bin/env python3
# -------------------------------------------------------------------------
# File: stop_services.py
# Project: MRCA - Mining Regulatory Compliance Assistant
#          Advanced Parallel HybridRAG - Intelligent Fusion System
# Author: Alexander Ricciardi
# Last Modified: 2025-07-25
# File Path: stop_services.py
# ------------------------------------------------------------------------

# --- Module Objective ---
# Simple script to stop all running MRCA services (backend and frontend).
# Provides a clean way to terminate detached processes.

# --- Apache-2.0 ---
# © 2025 Alexander Samuel Ricciardi - Mining Regulatory Compliance Assistant  
# License: Apache-2.0 | Technology: Advanced Parallel HybridRAG - Intelligent Fusion System
# -------------------------------------------------------------------------

"""
MRCA Service Stopper

Stops all running MRCA Advanced Parallel Hybrid services.
"""

import subprocess
import time
import requests

def stop_services():
    """Stop all MRCA services."""
    print("🛑 Stopping MRCA services...")
    
    try:
        # Kill all streamlit and uvicorn processes
        subprocess.run(["pkill", "-f", "streamlit"], capture_output=True, check=False)
        subprocess.run(["pkill", "-f", "uvicorn"], capture_output=True, check=False)
        
        print("Waiting for processes to terminate...")
        time.sleep(3)
        
        # Verify services are stopped
        try:
            backend_response = requests.get("http://localhost:8000/health", timeout=2)
            print("⚠️  Backend may still be running")
        except requests.RequestException:
            print("✅ Backend stopped")
            
        try:
            frontend_response = requests.get("http://localhost:8501/_stcore/health", timeout=2)
            print("⚠️  Frontend may still be running")
        except requests.RequestException:
            print("✅ Frontend stopped")
            
        print("\n✅ MRCA services have been stopped")
        
    except Exception as e:
        print(f"❌ Error stopping services: {e}")

def main():
    """Main function."""
    print("MRCA Service Stopper")
    print("="*30)
    stop_services()

if __name__ == "__main__":
    main() 