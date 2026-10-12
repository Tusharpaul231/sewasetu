import pytest


@pytest.mark.parametrize("bad", ["0000000000", "5123456789", "98765", "98765432101",
                                 "९८७६५४३२१०", "98765abcde"])
def test_apply_rejects_invalid_mobile(client, bad):
    resp = client.post("/apply", data={"mobile": bad})
    assert resp.status_code == 200          # stays on the page
    assert "10-digit" in resp.get_data(as_text=True)


def test_apply_accepts_valid_mobile(client):
    resp = client.post("/apply", data={"mobile": "9876543210"})
    assert resp.status_code == 302          # redirected to /verify


def test_mobile_field_is_numeric_in_browser(client):
    html = client.get("/apply").get_data(as_text=True)
    assert 'inputmode="numeric"' in html and "pattern=" in html