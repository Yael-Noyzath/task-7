from client.watcher import FileWatcher
from client.state import State
from pathlib import Path

def test_watcher_detects_new_files(tmp_path):
    db = State()
    watch_dir = tmp_path / "watch"  # תיקייה נפרדת לצפייה
    watch_dir.mkdir()

    f1 = watch_dir / "a.txt"
    f2 = watch_dir / "b.txt"

    f1.write_text("a")
    f2.write_text("b")
    
    state = State()
    watcher = FileWatcher(watch_dir, state)
    new_files = watcher.scan_once()

    assert len(new_files) == 2

#קובץ חדש לא מסומן כ־uploaded
def test_state_new_file_not_uploaded(tmp_path, monkeypatch):
    monkeypatch.setattr(Path, "home", lambda: tmp_path)

    state = State()
    test_file = tmp_path / "file.txt"
    test_file.write_text("hello")

    assert state.is_uploaded(test_file) is False

#הוספת קובץ ושמירה
def test_state_add_and_persist(tmp_path, monkeypatch):
    monkeypatch.setattr(Path, "home", lambda: tmp_path)

    state = State()
    test_file = tmp_path / "file.txt"
    test_file.write_text("hello")

    state.add(test_file)

    # טען מחדש מהדיסק
    state2 = State()
    assert len(state2.uploaded) == 1

#קובץ שכבר הועלה – לא יזוהה שוב
def test_watcher_ignores_uploaded_files(tmp_path, monkeypatch):
    monkeypatch.setattr(Path, "home", lambda: tmp_path)

    watch_dir = tmp_path / "watch"
    watch_dir.mkdir()

    f = watch_dir / "a.txt"
    f.write_text("data")

    state = State()
    watcher = FileWatcher(watch_dir, state)
    watcher.state_set.add(f)

    new_files = watcher.scan_once()
    assert new_files == []

#קבצים בלבד (לא תיקיות)
def test_watcher_ignores_directories(tmp_path, monkeypatch):
    monkeypatch.setattr(Path, "home", lambda: tmp_path)

    watch_dir = tmp_path / "watch"
    watch_dir.mkdir()

    (watch_dir / "subdir").mkdir()
    (watch_dir / "file.txt").write_text("x")

    state = State()
    watcher = FileWatcher(watch_dir, state)
    files = watcher.scan_once()

    assert len(files) == 1
    assert files[0].name == "file.txt"

