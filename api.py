# ---------------------------------------------------------------------------
# Standard library imports — built into Python, no installation needed
# ---------------------------------------------------------------------------
import os       # File system helpers (e.g. deleting a temporary file)
import shutil   # High-level file operations (e.g. copying file streams)
import tempfile # Create temporary files that are auto-cleaned up
from pathlib import Path    # Cross-platform file path handling
from typing import List     # Type hint: tells Python a value is a list

# ---------------------------------------------------------------------------
# Third-party imports — installed via 'pip install -r requirements.txt'
# ---------------------------------------------------------------------------
# FastAPI is the web framework that handles HTTP requests and routing
from fastapi import FastAPI, File, UploadFile, HTTPException
# CORS middleware lets the Angular frontend (port 4200) talk to this API
from fastapi.middleware.cors import CORSMiddleware
# StaticFiles serves files in /assets/ directly from disk (no Python code needed)
from fastapi.staticfiles import StaticFiles
# Pydantic models define the shape of request/response data and validate it
from pydantic import BaseModel
# Ultralytics provides the YOLOv11 object-detection model
from ultralytics import YOLO

# ---------------------------------------------------------------------------
# App setup
# ---------------------------------------------------------------------------
# Create the FastAPI application — this is the central object for the whole API
app = FastAPI(title="Target Detection API")

# Allow the Angular dev server (localhost:4200) to call this API.
# Without this browsers block cross-origin requests for security reasons.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4200"],  # Only allow our Angular app
    allow_credentials=True,
    allow_methods=["*"],   # GET, POST, etc.
    allow_headers=["*"],
)

# ---------------------------------------------------------------------------
# Static assets — example images the user can run detection on
# ---------------------------------------------------------------------------
# Path(__file__) is the path to this very file; .parent goes up one folder
ASSETS_DIR = Path(__file__).parent / "assets"
# Mount the /assets route so images can be fetched directly via URL,
# e.g. http://localhost:8000/assets/dog_test.jpg
app.mount("/assets", StaticFiles(directory=str(ASSETS_DIR)), name="assets")

# ---------------------------------------------------------------------------
# Load the YOLOv11 model (runs once at startup, reused for every request)
# ---------------------------------------------------------------------------
# yolo11l.pt is the 'large' size — high accuracy, good for reliable detection.
# NOTE: YOLOv11 uses 'yolo11' NOT 'yolov11' — there is no 'v' in the filename.
# On first run it auto-downloads weights (~87 MB) from Ultralytics servers.
model = YOLO("yolo11l.pt")

# COCO dataset class IDs we care about:
#   0 = person, 15 = cat, 16 = dog
TARGET_CLASSES = [0, 15, 16]


# ---------------------------------------------------------------------------
# Data models (Pydantic) — define what the API sends back as JSON
# ---------------------------------------------------------------------------

class Detection(BaseModel):
    """A single detected object with its label and confidence score."""
    label: str          # e.g. "Person", "Dog"
    confidence: float   # 0.0 – 1.0, higher = more confident


class DetectionResult(BaseModel):
    """The full response returned by every detection endpoint."""
    detections: List[Detection]  # All objects found in the image
    message: str                 # Human-readable summary


# ---------------------------------------------------------------------------
# Core detection logic — shared by both API routes and the CLI
# ---------------------------------------------------------------------------

def run_detection_on_file(image_path: str) -> DetectionResult:
    """Run YOLOv11 Large on the given image file and return structured results."""

    # model.predict() returns a list of Result objects (one per image).
    # conf=0.4 means ignore anything the model is less than 40% sure about.
    # iou=0.5 reduces duplicate boxes that overlap more than 50%.
    results = model.predict(source=image_path, classes=TARGET_CLASSES, conf=0.4, iou=0.5, verbose=False)

    detections = []

    # Loop over results (will be just one since we pass a single image)
    for r in results:
        # r.boxes contains one entry per detected object bounding box
        for box in r.boxes:
            class_id = int(box.cls[0])                    # Numeric class index
            label = model.names[class_id].capitalize()    # Convert to readable name
            confidence = round(float(box.conf[0]), 2)     # Round to 2 decimal places
            detections.append(Detection(label=label, confidence=confidence))

    # Build a simple summary message
    if detections:
        message = f"Found {len(detections)} target(s)"
    else:
        message = "No target detected"

    return DetectionResult(detections=detections, message=message)


# ---------------------------------------------------------------------------
# API Route 1: GET /api/assets — list the example images available
# ---------------------------------------------------------------------------

@app.get("/api/assets", response_model=List[str])
def list_assets():
    """Return list of example asset image filenames."""
    supported = {".jpg", ".jpeg", ".png", ".bmp", ".webp"}
    # Iterate over files in the assets folder and keep only image files
    files = [
        f.name for f in ASSETS_DIR.iterdir()
        if f.is_file() and f.suffix.lower() in supported
    ]
    return sorted(files)  # Alphabetical order for a consistent UI list


# ---------------------------------------------------------------------------
# API Route 2: POST /api/detect/upload — detect objects in a user-uploaded image
# ---------------------------------------------------------------------------

@app.post("/api/detect/upload", response_model=DetectionResult)
async def detect_uploaded_image(file: UploadFile = File(...)):
    """Accept an uploaded image and return detection results."""

    # Basic validation: reject anything that isn't an image
    if not file.content_type or not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="File must be an image")

    # Save the uploaded bytes to a temporary file on disk so YOLO can read it.
    # NamedTemporaryFile with delete=False keeps the file after closing it.
    suffix = Path(file.filename).suffix or ".jpg"
    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
        shutil.copyfileobj(file.file, tmp)  # Stream bytes from upload into file
        tmp_path = tmp.name

    try:
        result = run_detection_on_file(tmp_path)
    finally:
        # Always delete the temp file, even if detection raised an error
        os.unlink(tmp_path)

    return result


# ---------------------------------------------------------------------------
# API Route 3: POST /api/detect/asset/{filename} — detect on a built-in example
# ---------------------------------------------------------------------------

@app.post("/api/detect/asset/{filename}", response_model=DetectionResult)
def detect_asset_image(filename: str):
    """Run detection on one of the pre-existing example asset images."""

    # Security: strip any directory parts from the filename so a malicious
    # request like '../../secret.txt' can't escape the assets folder.
    safe_filename = Path(filename).name
    image_path = ASSETS_DIR / safe_filename

    if not image_path.exists() or not image_path.is_file():
        raise HTTPException(status_code=404, detail="Asset not found")

    return run_detection_on_file(str(image_path))


# ---------------------------------------------------------------------------
# Entry point — how the script is run directly (python api.py ...)
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    import sys
    import uvicorn  # ASGI server that runs the FastAPI app

    if len(sys.argv) > 1:
        # CLI mode: an image path was passed as a command-line argument
        # Example: python api.py assets/dog_test.jpg
        image_path = sys.argv[1]

        # Check the file exists before passing it to the model —
        # gives a clear human-readable message instead of a raw Python error
        if not Path(image_path).is_file():
            print(f"\nError: Image file not found — '{image_path}'")
            print("Please check the path and try again.")
            print("Example: python api.py assets/dog_test.jpg")
            sys.exit(1)

        result = run_detection_on_file(image_path)
        print("\n--- Detection Results ---")
        if result.detections:
            for d in result.detections:
                # :.2f formats the float to 2 decimal places, e.g. 0.92
                print(f"Target: {d.label} | Confidence: {d.confidence:.2f}")
        else:
            print(result.message)
    else:
        # Server mode: start the API so the Angular frontend can connect
        # reload=True automatically restarts when you save changes to this file
        uvicorn.run("api:app", host="0.0.0.0", port=8000, reload=True)
