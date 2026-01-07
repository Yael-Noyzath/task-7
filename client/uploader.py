import json
from pathlib import Path
import requests
from .config import Config
from .state import State

class Uploader:
    def __init__(self, server_url,state:State):
        self.server_url = server_url
        self.state = state

    def upload_file(self, file_path: Path):
        metadata = {
            "filename": file_path.name,
            "size": file_path.stat().st_size
        }

        with open(file_path, "rb") as f:
            files = {
                "file": (file_path.name, f)
            }
            data = {
                "metadata": json.dumps(metadata)
            }

            response = requests.post(
                self.server_url,
                files=files,
                data=data
            )
            if(response.status_code == 200):
                self.state.add(file_path)

        return response.status_code, response.text
