# main.py
from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import numpy as np
import pandas as pd

app = FastAPI(title="🌸 Iris Classifier API")

# Load model
model = joblib.load("model.joblib")

# Input schema
class IrisInput(BaseModel):
    sepal_length: float
    sepal_width: float
    petal_length: float
    petal_width: float

@app.get("/")
def read_root():
    return {"message": "Welcome to the Iris Classifier API!"}

@app.post("/predict/")
def predict_species(data: IrisInput):
    X = np.array([[data.sepal_length, data.sepal_width, data.petal_length, data.petal_width]])
    prediction = model.predict(X)[0]
    return {
        "predicted_class": prediction
    }
