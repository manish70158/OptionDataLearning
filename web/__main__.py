"""Startup script for the Options Backtester web app."""
import os
import sys
import webbrowser
import threading

import uvicorn


def open_browser():
    """Open the browser after a short delay."""
    import time
    time.sleep(1.5)
    webbrowser.open("http://localhost:8000")


def main():
    # Ensure the project root is on the Python path
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    if project_root not in sys.path:
        sys.path.insert(0, project_root)

    # Check if frontend is built
    frontend_dist = os.path.join(os.path.dirname(__file__), "frontend", "dist")
    if not os.path.isdir(frontend_dist):
        print("Frontend not built. Run: cd web/frontend && npm run build")
        print("Starting backend only...")
    else:
        print(f"Serving frontend from {frontend_dist}")

    # Open browser in background
    if "--no-browser" not in sys.argv:
        threading.Thread(target=open_browser, daemon=True).start()

    print("Starting Options Backtester at http://localhost:8000")
    print("API docs at http://localhost:8000/docs")
    print("Press Ctrl+C to stop.\n")

    # Render / Fly / other PaaS provide $PORT; fall back to 8000 for local dev.
    port = int(os.environ.get("PORT", "8000"))
    uvicorn.run(
        "web.backend.main:app",
        host="0.0.0.0",
        port=port,
        reload="--reload" in sys.argv,
    )


if __name__ == "__main__":
    main()
