A project to translate sign language gestures into real-time subtitles using AI and computer vision.

Quick demo of my Sign Language  Subtitle AI detecting the letter A.
(And yes, that is a sword in the background, doesn’t everyone keep one in their room in case the crusaders come back?)

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