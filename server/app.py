import json
from fastapi import FastAPI, File, UploadFile, Form
from fastapi.responses import JSONResponse
import os
import uuid
import pdb

from server.asset import Asset


app = FastAPI(title="Asset Catalog Server")

STORAGE_DIR = "storage_files"
os.makedirs(STORAGE_DIR, exist_ok=True)
METADATA_FILE = os.path.join(STORAGE_DIR, "uploaded_hashes.json")

# טען metadata קיים
if os.path.exists(METADATA_FILE):
    with open(METADATA_FILE, "r") as f:
        all_metadata = json.load(f)
else:
    all_metadata = {}

@app.get("/health")
def health():
    return{"status": "ok" }

@app.post("/upload")
async def upload(file: UploadFile = File(...)):
    try:
        content = await file.read()
        asset = Asset(content, filename=file.filename)
        if any(asset.hash == data.get("hash") for data in all_metadata.values()):
            return {"status": "skipped", "reason": "file already uploaded"}

        asset.save_file(STORAGE_DIR)
        asset.save_metadata(STORAGE_DIR)
        all_metadata[asset.id] = asset.metadata

        return {"status": "success", "file_id": asset.id, "message":"File saved successfully."}
    except Exception as e:
        return {"status": "error", "message": "File saving failed." + str(e)}