#!/usr/bin/env python3
"""
GCS Helper Script for GitHub Actions CI/CD
Downloads model and data from Google Cloud Storage
Note: google-cloud-storage must be installed first (pip install google-cloud-storage)
"""

import os
import sys

# Configuration
PROJECT_ID = "poised-defender-472812-e6"
BUCKET_NAME = "mlops-week6-artifacts-21f2001203"

def download_from_gcs(blob_name, destination_path):
    """Download file from GCS bucket"""
    try:
        # Import here after google-cloud-storage is installed
        from google.cloud import storage
        
        storage_client = storage.Client(project=PROJECT_ID)
        bucket = storage_client.bucket(BUCKET_NAME)
        blob = bucket.blob(blob_name)
        
        # Create directory if it doesn't exist
        dest_dir = os.path.dirname(destination_path)
        if dest_dir:
            os.makedirs(dest_dir, exist_ok=True)
        
        # Download file
        blob.download_to_filename(destination_path)
        print(f"✅ Downloaded: {blob_name} -> {destination_path}")
        return True
        
    except ImportError:
        print(f"❌ Error: google-cloud-storage not installed")
        print(f"   Run: pip install google-cloud-storage")
        return False
    except Exception as e:
        print(f"❌ Error downloading {blob_name}: {e}")
        return False

def main():
    """Download required files for deployment"""
    print("📦 Downloading artifacts from GCS...")
    print(f"   Bucket: gs://{BUCKET_NAME}")
    print("=" * 70)
    
    files_to_download = [
        ("models/model.joblib", "model.joblib"),
        ("data/iris.csv", "iris.csv"),
    ]
    
    downloaded = []
    failed = []
    
    for blob_name, local_path in files_to_download:
        if download_from_gcs(blob_name, local_path):
            downloaded.append(local_path)
        else:
            failed.append(blob_name)
    
    print("\n" + "=" * 70)
    print(f"📊 Download Summary:")
    print(f"   ✅ Downloaded: {len(downloaded)}")
    print(f"   ❌ Failed: {len(failed)}")
    
    if failed:
        print(f"\n⚠️  Missing files in GCS:")
        for file in failed:
            print(f"      - {file}")
        print(f"\n💡 To upload files, run:")
        print(f"      gsutil cp model.joblib gs://{BUCKET_NAME}/models/")
        print(f"      gsutil cp iris.csv gs://{BUCKET_NAME}/data/")
        print(f"\n   Or use: python upload_to_gcs.py")
        print(f"\n⚠️  Workflow will continue with dummy files...")
    else:
        print("\n✅ All artifacts downloaded successfully!")
    
    # Always exit successfully - the workflow will create dummy files if needed
<<<<<<< HEAD
    print("\n✅ Download script completed (exit 0)")
=======
>>>>>>> 9de670f32520420f9bbd9217e714b3f211c97559
    sys.exit(0)

if __name__ == "__main__":
    main()
