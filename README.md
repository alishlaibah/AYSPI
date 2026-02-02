A project to translate sign language gestures into real-time subtitles using AI and computer vision.

🌐 Live site: [ayspi.com](https://ayspi.com)

Quick demo of detecting the letter A.

## Demo

<p align="center">
  <img src="images/demo.GIF" alt="Sign Language AI Demo" width="400"/>
  <img src="images/A_reference.png" alt="ASL Letter A Reference" width="200"/>
</p>

## Hand Landmarks Reference

This project uses MediaPipe hand landmark coordinates as shown below:

![Hand Landmarks](images/hand_landmarks.png)

---

# Run Locally

## Prerequisites

- Python 3.10.x
- Node.js + npm (for the frontend)
- A webcam for live demo/testing

## Backend (FastAPI)

From the project root:

```bash
source venv_asl/bin/activate
python -m pip install -r requirements.txt
python -m uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000
```

## Frontend (Vite / React)

```bash
cd frontend
npm install
npm run dev -- --host
```
