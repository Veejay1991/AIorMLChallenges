# Installation & Setup

## Prerequisites

- Python 3.9+
- Node.js 18+ & npm
- Angular CLI (`npm install -g @angular/cli`)

---

## 1. Python Backend

```bash
# Create and activate a virtual environment
python -m venv venv

# Windows
venv\Scripts\activate

# macOS / Linux
source venv/bin/activate

# Install Python dependencies
pip install -r requirements.txt
```

### Run as API Server (for Angular frontend)
```bash
# Starts on http://localhost:8000
python api.py
```

### Run as CLI (quick detection without the frontend)
```bash
python api.py assets/dog_test.jpg
python api.py assets/all_targets.jpg
python api.py path/to/any_image.jpg
```

Example CLI output:
```
--- Detection Results ---
Target: Person | Confidence: 0.92
Target: Dog    | Confidence: 0.87
Target: Cat    | Confidence: 0.76
```

The API exposes:
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/assets` | List example image filenames |
| POST | `/api/detect/upload` | Upload an image for detection |
| POST | `/api/detect/asset/{filename}` | Detect on an existing example image |
| GET | `/assets/{filename}` | Serve example images |

---

## 2. Angular Frontend

```bash
cd detection-app
npm install
ng serve
```

Open **http://localhost:4200** in your browser.

---

## Quick Start (two terminals)

**Terminal 1 — API server:**
```bash
# Activate venv first (Windows: venv\Scripts\activate | macOS/Linux: source venv/bin/activate)
python api.py
```

**Terminal 2 — Angular dev server:**
```bash
cd detection-app && ng serve
```
