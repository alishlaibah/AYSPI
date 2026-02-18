from typing import List

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from backend.predict import get_metadata, predict

app = FastAPI()

class LandmarksRequest(BaseModel):
    landmarks: List[float]


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/predict")
def get_prediction(request: LandmarksRequest):
    return predict(request.landmarks)


@app.get("/metadata")
def metadata():
    return get_metadata()
