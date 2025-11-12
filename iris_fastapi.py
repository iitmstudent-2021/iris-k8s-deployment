# main.py
from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import numpy as np
import pandas as pd
import logging
import sys

# Configure logging to stdout (required for GKE logs)
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger(__name__)

app = FastAPI(title="🌸 Iris Classifier API")

# Load model
logger.info("Loading model from model.joblib...")
model = joblib.load("model.joblib")
logger.info("Model loaded successfully!")

# Input schema
class IrisInput(BaseModel):
    sepal_length: float
    sepal_width: float
    petal_length: float
    petal_width: float

@app.get("/")
def read_root():
    logger.info("Health check endpoint accessed")
    return {"message": "Welcome to the Iris Classifier API!"}

@app.post("/predict/")
def predict_species(data: IrisInput):
    logger.info(f"Prediction request received: {data.dict()}")
    X = np.array([[data.sepal_length, data.sepal_width, data.petal_length, data.petal_width]])
    prediction = model.predict(X)[0]
    logger.info(f"Prediction result: {prediction}")
    return {
        "predicted_class": prediction
    }
