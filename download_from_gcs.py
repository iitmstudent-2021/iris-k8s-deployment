#!/usr/bin/env python3
"""
GCS Helper Script for GitHub Actions CI/CD
Downloads model and data from Google Cloud Storage
"""

from google.cloud import storage
import os
import sys

# Configuration
PROJECT_ID = "poised-defender-472812-e6"
BUCKET_NAME = "mlops-week6-artifacts-21f2001203"

def download_from_gcs(blob_name, destination_path):
    """Download file from GCS bucket"""
    try:
        storage_client = storage.Client(project=PROJECT_ID)
        bucket = storage_client.bucket(BUCKET_NAME)
        blob = bucket.blob(blob_name)
        
        # Create directory if it doesn't exist
        os.makedirs(os.path.dirname(destination_path), exist_ok=True)
        
        # Download file
        blob.download_to_filename(destination_path)
        print(f"✅ Downloaded: {blob_name} -> {destination_path}")
        return True
        
    except Exception as e:
        print(f"❌ Error downloading {blob_name}: {e}")
        return False

def main():
    """Download required files for deployment"""
    print("📦 Downloading artifacts from GCS...")
    print(f"   Bucket: {BUCKET_NAME}")
    
    files_to_download = [
        ("models/model.joblib", "model.joblib"),
        ("data/iris.csv", "iris.csv"),
    ]
    
    success = True
    for blob_name, local_path in files_to_download:
        if not download_from_gcs(blob_name, local_path):
            success = False
    
    if success:
        print("\n✅ All artifacts downloaded successfully!")
        sys.exit(0)
    else:
        print("\n❌ Some artifacts failed to download")
        sys.exit(1)

if __name__ == "__main__":
    main()
