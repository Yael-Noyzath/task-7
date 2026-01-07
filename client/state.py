from pathlib import Path
from .hash_util import file_hash
import json

class State:
    def __init__(self):
        #יצירת תקיה
        self.state_dir = Path.home() / "AppData" / "Local" / "asset_client"
        self.state_dir.mkdir(parents=True, exist_ok=True)
        #יצירת קובץ uploaded.json
        self.state_file = self.state_dir / "uploaded.json"
        
        self.uploaded = set()
        self.load()

    #טעינת הקובץ
    def load(self):
        if self.state_file.exists():
            self.uploaded = set(json.loads(self.state_file.read_text()))
    
    def is_uploaded(self, file_path: Path) -> bool:
        return file_hash(file_path) in self.uploaded
    
    #הוספת HASH לקובץ
    def add(self, file_path):
        hash = file_hash(file_path)
        self.uploaded.add(hash)
        self.save()

    #שמירה של השינויים בקובץ (כתיבה לקובץ)
    def save(self):
        self.state_file.write_text(json.dumps(list(self.uploaded)))

