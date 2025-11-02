#!/usr/bin/env python3
"""
Upload ML artifacts to Google Cloud Storage
Run this locally to make files available for CI/CD workflows
"""

from google.cloud import storage
import os
import sys

# Configuration
PROJECT_ID = "poised-defender-472812-e6"
BUCKET_NAME = "mlops-week6-artifacts-21f2001203"

def upload_to_gcs(local_path, blob_name):
    """Upload file to GCS bucket"""
    try:
        if not os.path.exists(local_path):
            print(f"❌ File not found: {local_path}")
            return False
            
        storage_client = storage.Client(project=PROJECT_ID)
        bucket = storage_client.bucket(BUCKET_NAME)
        blob = bucket.blob(blob_name)
        
        # Upload file
        blob.upload_from_filename(local_path)
        file_size = os.path.getsize(local_path)
        print(f"✅ Uploaded: {local_path} -> gs://{BUCKET_NAME}/{blob_name} ({file_size:,} bytes)")
        return True
        
    except Exception as e:
        print(f"❌ Error uploading {local_path}: {e}")
        return False

def main():
    """Upload required files to GCS"""
    print("🚀 Uploading artifacts to GCS...")
    print(f"   Bucket: gs://{BUCKET_NAME}")
    print("=" * 70)
    
    # Files to upload
    files_to_upload = [
        ("model.joblib", "models/model.joblib"),
        ("iris.csv", "data/iris.csv"),
    ]
    
    uploaded = []
    failed = []
    
    for local_path, blob_name in files_to_upload:
        if upload_to_gcs(local_path, blob_name):
            uploaded.append(local_path)
        else:
            failed.append(local_path)
    
    print("\n" + "=" * 70)
    print(f"📊 Upload Summary:")
    print(f"   ✅ Uploaded: {len(uploaded)}")
    print(f"   ❌ Failed: {len(failed)}")
    
    if uploaded:
        print(f"\n✅ Files uploaded to gs://{BUCKET_NAME}/")
        print(f"\n🔗 View at: https://console.cloud.google.com/storage/browser/{BUCKET_NAME}")
        print(f"\n🚀 You can now deploy: git push origin main")
    
    if failed:
        print(f"\n❌ Failed to upload:")
        for file in failed:
            print(f"      - {file}")
        print(f"\n💡 Make sure files exist in current directory")
        sys.exit(1)
    else:
        sys.exit(0)

if __name__ == "__main__":
    main()
