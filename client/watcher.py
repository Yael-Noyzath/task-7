from pathlib import Path
import time

from .state import State

class FileWatcher:
    def __init__(self, watch_dir:Path,state, poll_interval: float = 5.0):
        #מקבל תקיה להשגיח עליה
        #DB וכל כמה שניות לסרוק את התקיה (ברירת מחדל-5 שניות)
        self.watch_dir = watch_dir
        self.state_set = state or State()
        self.poll_interval = poll_interval

    def scan_once(self):
        #מחזיר רשימה של קבצים שלא נמצאים בDB
        new_files = []
        for f in self.watch_dir.iterdir():
            if f.is_file() and not self.state_set.is_uploaded(f):
                new_files.append(f)
        return new_files
    
    def watch(self):
        #לולאה אינסופית שמחזירה קבצים חדשים כל כמה שניות
        print(f"Watching directory: {self.watch_dir}")
        while True:
            new_files = self.scan_once()
            if new_files:
                yield new_files
            time.sleep(self.poll_interval)







