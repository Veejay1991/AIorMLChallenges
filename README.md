# AI / ML Challenges — Target Detection App

## Starting Point

Before starting this challenge, my experience was:

- **Python** — Could write basic Python code (variables, loops, functions) but had no experience with libraries, frameworks, or building applications
- **Computer Vision** — No prior knowledge of computer vision, object detection, or how vision models work
- **YOLO / AI Models** — Had never heard of YOLO or any object detection model before this challenge
- **COCO Dataset** — No knowledge of what COCO is or how models are trained on datasets

Before the challenge, I had explored a little out of personal curiosity:

- **PyTorch** — Went through the basics of how PyTorch works as the underlying deep learning framework behind YOLO. Understood that models are built as layers of mathematical operations applied to numbers (tensors)
- **How Models Are Trained** — Learned the basic idea: the model makes a prediction, compares it to the correct answer using a loss function (a simple math calculation measuring how wrong it was), then adjusts its internal weights slightly to do better next time — this cycle repeats thousands of times (training)
- **Inference vs Training** — Understood the difference: training is the learning phase (slow, done once), inference is using the trained model to make predictions (fast, what this app does)

Everything in this project — especially understanding how YOLO works, object detection, and the COCO dataset — was learned during this challenge.

---

## Research Path

I did not follow any specific documentation, videos, or courses for this challenge.

My entire research was done through **conversations with GitHub Copilot and Google Gemini**. I asked questions, got explanations, asked follow-up questions, and kept going until I fully understood each concept — then moved on to the next one.

The learning flow was roughly:

1. **What is object detection?** — Asked Copilot to explain it from scratch in simple terms
2. **What models exist?** — Asked for a comparison, understood why YOLO stood out
3. **How does YOLO work internally?** — Asked about grids, bounding boxes, confidence scores, NMS
4. **What is the COCO dataset?** — Asked how models are pre-trained and what class IDs mean
5. **How does PyTorch fit in?** — Asked about tensors, layers, loss functions, and the training loop
6. **What is inference?** — Clarified the difference between training a model and using one
7. **Implementation** — Once I understood the concepts, started writing the code with guidance

No courses, no documentation pages, no YouTube videos — just conversations until things made sense, then built it.

---

## Pivot Moments

### 1. Getting Detection Working
The core integration turned out to be simpler than expected — pass the image path to the YOLO model, specify which target classes to look for (class IDs: 0 = person, 15 = cat, 16 = dog), and the model handles everything internally and returns structured results. No complex setup needed on my side. That was a confidence boost early on.

### 2. YOLOv8 Nano → Medium (Accuracy Problem)
The first model I tried was **YOLOv8 nano** (`yolov8n.pt`) — the smallest and fastest variant. On several test images it returned wrong or missing detections. I researched using Copilot and Gemini and learned that YOLO comes in five sizes (nano → small → medium → large → xlarge), each progressively more accurate at the cost of speed and file size. Switched to **medium** (`yolov8m.pt`) and the results noticeably improved.

### 3. YOLOv8 → YOLOv11 (Newer Generation)
While researching further, I discovered Ultralytics had released **YOLOv11** — a newer generation model with higher accuracy than v8 at the same model size and faster inference speed. The code change was a single filename swap (`yolov8m.pt` → `yolo11m.pt`), so switching was straightforward.

### 4. YOLOv11 Medium → Large (Misclassification Fix)
After switching to YOLOv11 medium, a new problem appeared — on the `all_targets.jpg` test image (which has 1 person, 1 dog, 1 cat) the model was returning **2 dogs and 1 person**. The cat was being misclassified as a dog at low confidence (0.44) while the actual cat was only detected at 0.26 — below the 0.4 threshold, so it was filtered out entirely.

Tested the **large** model (`yolo11l.pt`) on the same image:

| Target | Confidence |
|---|---|
| Dog | 0.92 |
| Person | 0.86 |
| Cat | 0.76 |

All three targets detected correctly with high confidence. The large model has enough learned detail to distinguish between a cat and a dog where the medium model could not. Switched to `yolo11l.pt` as the final model.

---

## Model Choice

YOLO (**You Only Look Once**) processes the entire image in a **single neural network pass**, making it significantly faster than two-stage detectors like Faster R-CNN that scan the image twice.

### Key Reasons for Choosing YOLOv11

| Reason | Detail |
|---|---|
| **Speed** | Real-time detection — one pass through the network, no region scanning |
| **Accuracy** | Higher accuracy than v8 at the same model size |
| **Pre-trained** | Trained on 80 COCO classes — works out of the box, no custom training needed |
| **Scalable sizes** | nano → xlarge — tune speed vs accuracy for your hardware |
| **Easy to use** | One `ultralytics` package handles inference, training, and export |
| **Custom training** | Can be fine-tuned on your own images with a few lines of code |

### Model Size Used

This project uses `yolo11m.pt` (medium) — the best balance of speed and accuracy for a development machine.

| Model | Speed | Accuracy |
|---|---|---|
| `yolo11n.pt` | Fastest | Basic |
| `yolo11s.pt` | Fast | Good |
| `yolo11m.pt` | Balanced | Very good |
| **`yolo11l.pt`** ← *this project* | Fast-Balanced | High |
| `yolo11x.pt` | Slowest | Best |

### Why Not Other Models?

| Model | Reason Not Chosen |
|---|---|
| Faster R-CNN | Two-stage — slower, overkill for this use case |
| SSD | Less accurate than YOLO at similar speeds |
| EfficientDet | More complex setup, less community support |
| RT-DETR | Heavier compute requirements |
| SAM | Segmentation-only, no class labels |

---

## If I Had More Time

This was a **48-hour challenge**. The major goal — detecting objects in images using a YOLO model — is complete and working.

With more time, the next thing I would have done is **custom training**. Rather than using the pre-trained YOLO model as-is (which detects 80 general COCO classes), I would:

- Collect or find a dataset of specific target images relevant to the challenge
- Label the images with bounding boxes for the objects to detect
- Fine-tune the YOLO model on that custom dataset so it learns to detect those specific targets with higher precision
- Compare results between the pre-trained model and the custom-trained model

Right now the app uses the existing pre-trained `yolo11m.pt` model directly and it produces good results for the three target classes (person, cat, dog). Custom training would take that further — making the model specialised rather than general purpose. That is something I would definitely explore given more time.

---

## Quick Start

See [INSTALL.md](INSTALL.md) for full setup instructions.

---

## Demo

[Watch the app demo on Google Drive](https://drive.google.com/file/d/1Yqi5JEYBH7Vn0VNUhRDvkb9U7lgIczJX/view?usp=sharing)

