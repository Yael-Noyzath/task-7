from client.hash_util import file_hash

#אותו תוכן → אותו hash
def test_file_hash_same_content(tmp_path):
    f1 = tmp_path / "a.txt"
    f2 = tmp_path / "b.txt"

    f1.write_text("hello")
    f2.write_text("hello")

    assert file_hash(f1) == file_hash(f2)

#תוכן שונה → hash שונה
def test_file_hash_different_content(tmp_path):
    f1 = tmp_path / "a.txt"
    f2 = tmp_path / "b.txt"

    f1.write_text("hello")
    f2.write_text("world")

    assert file_hash(f1) != file_hash(f2)

