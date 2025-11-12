# main.py
from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import numpy as np
import pandas as pd
import logging
import sys
import os

# OpenTelemetry imports for Google Cloud Trace
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.cloud_trace import CloudTraceSpanExporter
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.sdk.resources import Resource

# Configure logging to stdout (required for GKE logs)
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger(__name__)

# Setup Google Cloud Trace
try:
    # Get project ID from environment or metadata
    project_id = os.getenv("GCP_PROJECT", "poised-defender-472812-e6")
    
    # Create a resource with service name
    resource = Resource.create({"service.name": "iris-classifier-api"})
    
    # Set up the tracer provider
    tracer_provider = TracerProvider(resource=resource)
    trace.set_tracer_provider(tracer_provider)
    
    # Configure Cloud Trace exporter
    cloud_trace_exporter = CloudTraceSpanExporter(project_id=project_id)
    tracer_provider.add_span_processor(BatchSpanProcessor(cloud_trace_exporter))
    
    logger.info(f"✅ Cloud Trace configured for project: {project_id}")
except Exception as e:
    logger.warning(f"⚠️ Cloud Trace setup failed (will continue without tracing): {e}")

# Get tracer for manual tracing
tracer = trace.get_tracer(__name__)

app = FastAPI(title="🌸 Iris Classifier API")

# Instrument FastAPI with OpenTelemetry (auto-traces all endpoints)
FastAPIInstrumentor.instrument_app(app)

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
    with tracer.start_as_current_span("health-check") as span:
        span.set_attribute("endpoint", "root")
        return {"message": "Welcome to the Iris Classifier API!"}

@app.post("/predict/")
def predict_species(data: IrisInput):
    logger.info(f"Prediction request received: {data.dict()}")
    
    with tracer.start_as_current_span("predict-species") as span:
        # Add input attributes to trace
        span.set_attribute("input.sepal_length", data.sepal_length)
        span.set_attribute("input.sepal_width", data.sepal_width)
        span.set_attribute("input.petal_length", data.petal_length)
        span.set_attribute("input.petal_width", data.petal_width)
        
        # Prepare input
        with tracer.start_as_current_span("prepare-input"):
            X = np.array([[data.sepal_length, data.sepal_width, data.petal_length, data.petal_width]])
        
        # Make prediction
        with tracer.start_as_current_span("model-predict"):
            prediction = model.predict(X)[0]
            span.set_attribute("prediction.result", prediction)
        
        logger.info(f"Prediction result: {prediction}")
        
        return {
            "predicted_class": prediction
        }
