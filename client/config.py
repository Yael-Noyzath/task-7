from pathlib import Path
import json

class Config:
    def __init__(self):
        # תיקיית config ב-Windows: C:\Users\<user>\AppData\Roaming\asset_client
        self.config_dir = Path.home() / "AppData" / "Roaming" / "asset_client"
        self.config_dir.mkdir(parents=True, exist_ok=True)
        self.config_file = self.config_dir / "config.json"

        # הגדרות ברירת מחדל
        self.data = {
            "server_url": "http://127.0.0.1:8009/upload"#,
        }
        self.save()

    #def load(self):
    #    if self.config_file.exists():
    #        print(f"Config saved to {self.config_file}")
    #        self.data.update(json.loads(self.config_file.read_text()))
    #    else:
    #        self.save()

    def save(self):
        self.config_file.write_text(json.dumps(self.data, indent=2))
