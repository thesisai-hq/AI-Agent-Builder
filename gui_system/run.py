#!/usr/bin/env python3
"""
Launcher script for AI Agent Builder GUI System.

This script starts both the FastAPI backend and opens the browser to the frontend.

Usage:
    python run.py              # Development mode (backend only)
    python run.py --frontend   # Development mode (backend + frontend)
    python run.py --prod       # Production mode (build frontend first)
"""

import sys
import subprocess
import webbrowser
import time
from pathlib import Path

# Add parent directory to Python path so gui_system module can be imported
sys.path.insert(0, str(Path(__file__).parent.parent))


def main():
    """Main launcher function."""
    args = sys.argv[1:]
    mode = "dev"
    
    if "--prod" in args:
        mode = "prod"
    elif "--frontend" in args:
        mode = "dev-full"
    
    print("=" * 60)
    print("AI Agent Builder - GUI System")
    print("=" * 60)
    
    if mode == "prod":
        print("\n🚀 Production Mode")
        print("\nBuilding frontend...")
        
        # Check if frontend is built
        frontend_dist = Path("frontend/dist")
        if not frontend_dist.exists():
            print("\n❌ Frontend not built!")
            print("Run these commands first:")
            print("  cd frontend")
            print("  npm install")
            print("  npm run build")
            return
        
        print("✓ Frontend built")
        print("\n📡 Starting backend server...")
        print("Backend: http://localhost:8000")
        print("Docs: http://localhost:8000/docs\n")
        
        # Start backend
        subprocess.run([
            sys.executable, "-m", "uvicorn",
            "backend.main:app",
            "--host", "127.0.0.1",
            "--port", "8000"
        ])
    
    elif mode == "dev-full":
        print("\n🔧 Development Mode (Full)")
        print("\n📡 Starting backend...")
        
        # Start backend in background
        backend_process = subprocess.Popen([
            sys.executable, "-m", "uvicorn",
            "backend.main:app",
            "--host", "127.0.0.1",
            "--port", "8000",
            "--reload"
        ])
        
        # Wait for backend to start
        print("Waiting for backend to start...")
        time.sleep(3)
        
        print("\n🎨 Starting frontend...")
        print("Frontend: http://localhost:5173")
        print("Backend: http://localhost:8000")
        print("Docs: http://localhost:8000/docs\n")
        
        # Check if node_modules exists
        frontend_dir = Path("frontend")
        if not (frontend_dir / "node_modules").exists():
            print("\n⚠️  Frontend dependencies not installed!")
            print("Run: cd frontend && npm install\n")
            backend_process.terminate()
            return
        
        # Open browser
        time.sleep(1)
        webbrowser.open("http://localhost:5173")
        
        # Start frontend
        try:
            subprocess.run(
                ["npm", "run", "dev"],
                cwd=str(frontend_dir)
            )
        except KeyboardInterrupt:
            print("\n\n👋 Shutting down...")
            backend_process.terminate()
    
    else:  # dev mode - backend only
        print("\n🔧 Development Mode (Backend Only)")
        print("\n📡 Starting backend...")
        print("Backend: http://localhost:8000")
        print("Docs: http://localhost:8000/docs")
        print("\nTo start frontend separately:")
        print("  cd frontend")
        print("  npm run dev\n")
        
        # Start backend with correct module path
        subprocess.run([
            sys.executable, "-m", "uvicorn",
            "backend.main:app",
            "--host", "127.0.0.1",
            "--port", "8000",
            "--reload"
        ])


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Shutting down...")
        sys.exit(0)
