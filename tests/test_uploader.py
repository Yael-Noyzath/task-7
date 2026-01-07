
from pathlib import Path
from client.uploader import Uploader
from client.state import State


class DummyResponse:
    status_code = 200
    text = "ok"


def fake_post(*args, **kwargs):
    return DummyResponse()

#העלאה מוצלחת
def test_uploader_success(tmp_path, monkeypatch):
    file = tmp_path / "a.txt"
    file.write_text("hello")

    monkeypatch.setattr("requests.post", fake_post)

    monkeypatch.setattr(Path, "home", lambda: tmp_path)

    state = State()
    uploader = Uploader("http://fake", state)

    status, _ = uploader.upload_file(file)

    assert status == 200
    assert len(state.uploaded) == 1

class FailResponse:
    status_code = 500
    text = "error"

#כשל בהעלאה – לא נשמר ב־State
def test_uploader_failure(tmp_path, monkeypatch):
    file = tmp_path / "a.txt"
    file.write_text("hello")

    monkeypatch.setattr("requests.post", lambda *a, **k: FailResponse())
    monkeypatch.setattr(Path, "home", lambda: tmp_path)

    state = State()
    uploader = Uploader("http://fake", state)

    status, _ = uploader.upload_file(file)

    assert status == 500
    assert len(state.uploaded) == 0
