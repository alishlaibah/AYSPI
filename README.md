# AYSPI

Real-time ASL letter recognition from a webcam using MediaPipe hand tracking and a custom-trained sequence classifier.

- **Live site:** [ayspi.com](https://ayspi.com)
- **Source:** [github.com/alishlaibah/AYSPI](https://github.com/alishlaibah/AYSPI)

> The backend runs on Render's free tier. The first request may take ~30-120s while the backend wakes up from a cold start.

## Demo

<p align="center">
  <img src="images/demo.GIF" alt="Sign Language AI Demo" width="400"/>
  <img src="images/A_reference.png" alt="ASL Letter A Reference" width="200"/>
</p>

## How It Works

```
Browser (React + MediaPipe Hands)
  |
  |  21 landmarks x 3 coords = 63 values per frame
  v
Sliding window buffer (30 frames)
  |
  |  POST /predict  { landmarks: float[1890] }
  v
FastAPI backend (Render)
  |
  |  Wrist-relative normalization -> StandardScaler -> Keras model
  v
Response  { letter, confidence, index }
```

1. **Track hand** -- MediaPipe Hands extracts 21 3D landmarks from each webcam frame.
2. **Normalize in-browser** -- Landmarks are structured client-side. No raw video leaves the browser.
3. **Buffer sequence** -- A sliding 30-frame window captures motion over time, enabling recognition of motion-dependent letters like J and Z.
4. **Classify** -- The sequence is sent to the backend, wrist-normalized, scaled, and passed through a Conv1D + Bidirectional GRU classifier.

![Hand Landmarks](images/hand_landmarks.png)

## How It Was Built

### Data Collection

I wrote webcam-based scripts to record and label my own training set. Collected ~200-300 samples per letter. For letters that depend on motion (J, Z), I captured 60-frame sequences instead of single snapshots.

- Static signs: `dataset/data_collection.py`
- Motion letters: `dataset/motion_data_collection.py`
- Normalization + loading: `dataset/data_loader.py`

### Training

Trained a sequence classifier in TensorFlow/Keras on the landmark data. Used NumPy and scikit-learn for preprocessing (StandardScaler, train/test split, stratified sampling). The architecture (Conv1D → Bidirectional GRU → Dense) is defined in `models/asl_sequence_classifier.py`.

- Training script: `training/train_asl_classifier.py`
- Local live testing: `training/predict_live.py`
- `best_asl_sequence_classifier.keras` is a checkpoint saved during training based on best validation accuracy. I went with the final epoch model (`asl_sequence_classifier.keras`) instead since it generalized better on live webcam input.

### Deployment

Backend is a FastAPI app deployed on [Render](https://render.com). Frontend is React + Vite hosted on [Cloudflare Pages](https://pages.cloudflare.com).

## Run Locally

**Prerequisites:** Python 3.10.x, Node.js + npm, a webcam.

### Backend

```bash
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python -m uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000
```

API runs at `http://localhost:8000`.

### Frontend

```bash
cd frontend
npm install
npm run dev
```

Dev server runs at `http://localhost:3000`.

Set `VITE_API_URL` in `frontend/.env` if the backend is not on `http://localhost:8000`. Restart the dev server after changing it.

## Credits

- [MediaPipe Hands](https://developers.google.com/mediapipe/solutions/vision/hand_landmarker) -- hand landmark detection
- [TensorFlow / Keras](https://www.tensorflow.org/) -- model training and inference
- [FastAPI](https://fastapi.tiangolo.com/) + [Uvicorn](https://www.uvicorn.org/) + [Pydantic](https://docs.pydantic.dev/) -- API server
- [OpenCV](https://opencv.org/) -- webcam capture for data collection and local prediction
- [scikit-learn](https://scikit-learn.org/) -- preprocessing (StandardScaler, train/test split)
- [React](https://react.dev/) + [Vite](https://vite.dev/) -- frontend

## License

MIT -- see [LICENSE](LICENSE).
