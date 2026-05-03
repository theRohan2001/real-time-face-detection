# Real-time Face Detection

A highly responsive live-stream tracking API that detects faces over WebSockets, caches region-of-interest coordinates in a tiny SQLite datastore, and powers an ultra-fast HTML5 Canvas feed—built entirely with standard Python libraries and MediaPipe without using OpenCV!

## Quick Start (Docker)
We use `docker compose` to effortlessly package the environment. Since setting up dependencies for computer vision pipelines (like MediaPipe) locally can be overwhelming, running it via containerization isolates the setup and saves hours of potential troubleshooting.

**To run the application:**
1. Clone or navigate to the directory.
2. Run this simple command:
   ```bash
   docker compose up --build -d
   ```
3. Open your browser and test it!
   [http://localhost:8000](http://localhost:8000)

Your Regions of Interest metadata logs will be persisted to a local `face_roi.db` file so restarts won't destroy history!

## Endpoints
- **WebSocket Feed**: `ws://localhost:8000/ws/feed` (Accepts frame chunks)
- **Extracted ROI**: `http://localhost:8000/api/roi` 
