from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends
from sqlalchemy.orm import Session
from db.database import get_db
from db.models import FaceROI
import asyncio
from fastapi import BackgroundTasks
from fastapi.concurrency import run_in_threadpool
from services.face_detector import process_frame

router = APIRouter()

@router.websocket("/ws/feed")
async def websocket_feed(websocket: WebSocket, db: Session = Depends(get_db)):
    await websocket.accept()
    try:
        while True:
            # We accept bytes to minimize decoding overhead if client sends Blob,
            # or handle text if base64 logic is preferred. Let's do bytes.
            try:
                message = await websocket.receive()
                if "bytes" in message:
                    data = message["bytes"]
                elif "text" in message:
                    # if frontend sends DataURL, we process it as base64
                    import base64
                    text_data = message["text"]
                    if "," in text_data:
                        text_data = text_data.split(",")[1]
                    data = base64.b64decode(text_data)
                else:
                    continue
                    
                processed_bytes, roi_data = await run_in_threadpool(process_frame, data)
                
                if roi_data:
                    # Save to db
                    roi_entry = FaceROI(
                        x_min=roi_data['x_min'],
                        y_min=roi_data['y_min'],
                        width=roi_data['width'],
                        height=roi_data['height']
                    )
                    db.add(roi_entry)
                    db.commit()
                
                # Send the annotated frame back directly as bytes.
                await websocket.send_bytes(processed_bytes)

            except WebSocketDisconnect:
                print("WebSocket legitimately disconnected from frontend")
                break
            except RuntimeError as e:
                if "Cannot call" in str(e):
                    break
                print(f"Runtime error: {e}")
                break
            except Exception as e:
                print(f"Error processing frame: {e}")
                
    except WebSocketDisconnect:
        print("WebSocket disconnected entirely")
