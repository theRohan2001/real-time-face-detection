import numpy as np
from PIL import Image, ImageDraw
import io
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision

# Initialize MediaPipe Face Detection
base_options = python.BaseOptions(model_asset_path='detector.tflite')
options = vision.FaceDetectorOptions(base_options=base_options)
face_detector = vision.FaceDetector.create_from_options(options)

def process_frame(frame_bytes: bytes):
    """
    Takes image bytes, uses mediapipe to detect face,
    draws bounding box with Pillow, returns annotated image bytes
    and ROI data dict.
    """
    image = Image.open(io.BytesIO(frame_bytes))
    image_rgb = image.convert('RGB')
    
    # Convert image to numpy array for MediaPipe
    image_np = np.array(image_rgb)
    mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=image_np)
    
    # Process with MediaPipe
    results = face_detector.detect(mp_image)
    
    roi_data = None
    if results.detections:
        # User specified "Assume only one face will be present in the video"
        detection = results.detections[0]
        bboxC = detection.bounding_box
        
        ih, iw = image_np.shape[:2]
        x_min = int(bboxC.origin_x)
        y_min = int(bboxC.origin_y)
        width = int(bboxC.width)
        height = int(bboxC.height)
        
        # Simple clamping
        x_min = max(0, x_min)
        y_min = max(0, y_min)
        width = min(iw - x_min, width)
        height = min(ih - y_min, height)
        
        roi_data = {
            "x_min": float(x_min),
            "y_min": float(y_min),
            "width": float(width),
            "height": float(height)
        }
        
        # Draw bounding box without OpenCV
        draw = ImageDraw.Draw(image)
        x_max = x_min + width
        y_max = y_min + height
        draw.rectangle([x_min, y_min, x_max, y_max], outline="red", width=3)
    
    # Encode modified image back to JPEG bytes
    buffer = io.BytesIO()
    image.save(buffer, format="JPEG")
    
    return buffer.getvalue(), roi_data
