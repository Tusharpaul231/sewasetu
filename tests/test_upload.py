import io


def _upload(client, name, size):
    with client.session_transaction() as s:
        s["verified_mobile"] = "9876543210"
    return client.post("/upload", data={"document": (io.BytesIO(b"0" * size), name)},
                       content_type="multipart/form-data")


def test_jpg_is_accepted(client):
    assert _upload(client, "photo.jpg", 50_000).status_code == 302


def test_pdf_of_2mb_is_accepted(client):
    assert _upload(client, "certificate.pdf", 2 * 1024 * 1024).status_code == 302


def test_file_over_5mb_is_still_rejected(client):
    resp = _upload(client, "huge.pdf", 6 * 1024 * 1024)
    assert resp.status_code != 302


def test_other_types_are_still_rejected(client):
    assert _upload(client, "notes.txt", 100).status_code != 302