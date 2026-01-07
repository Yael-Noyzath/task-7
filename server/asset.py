import datetime
import json
import uuid
import os
from server.hasher import Hasher


class Asset:
    ##constractor
    def __init__(self, file_content: bytes, filename: str):
        self.id = str(uuid.uuid4())           # מזהה ייחודי
        self.file_content = file_content
        self.filename = filename
        self.hash = Hasher.compute_hash(file_content)  # hash ייחודי
        self.upload_time = datetime.datetime.now().isoformat()

        # metadata dict
        self.metadata = {
            "id": self.id,
            "filename": self.filename,
            "hash": self.hash,
            "upload_time": self.upload_time
        }

    ##שמירת קובץ
    def save_file(self, storage_dir: str):
        try:
            os.makedirs(storage_dir, exist_ok=True)
            name, ext = os.path.splitext(self.filename)
            if not ext:
                ext = ".bin"
            print(ext)
            file_path = os.path.join(storage_dir, f"{self.id}_{self.filename}{ext}")
            with open(file_path, "wb") as f:
                f.write(self.file_content)
        except Exception as e:
            print(f"Error saving asset {self.id}: {e}")

    #שמירת metadata
    def save_metadata(self, storage_dir: str):

        os.makedirs(storage_dir, exist_ok=True)
        metadata_file = os.path.join(storage_dir, "metadata.json")

        # טען metadata קיים
        if os.path.exists(metadata_file):
            with open(metadata_file, "r") as f:
                all_metadata = json.load(f)
        else:
            all_metadata = {}

        # הוסף/עדכן מטא-דאטה של הקובץ הזה
        all_metadata[self.id] = self.metadata

        # שמור חזרה
        with open(metadata_file, "w") as f:
            json.dump(all_metadata, f, indent=4)
