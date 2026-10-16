import re


def _sum(client):
    html = client.get("/apply").get_data(as_text=True)
    a, b = re.search(r"What is (\d) \+ (\d)\?", html).groups()
    return int(a) + int(b)


def test_wrong_answer_is_rejected(client, monkeypatch):
    import app as app_module
    monkeypatch.setattr(app_module, "CAPTCHA_ENABLED", True)
    answer = _sum(client)
    resp = client.post("/apply", data={"mobile": "9876543210", "captcha": str(answer + 1)})
    assert resp.status_code == 200 and "security check" in resp.get_data(as_text=True)


def test_empty_answer_is_rejected(client, monkeypatch):
    import app as app_module
    monkeypatch.setattr(app_module, "CAPTCHA_ENABLED", True)
    _sum(client)
    assert client.post("/apply", data={"mobile": "9876543210", "captcha": ""}).status_code == 200


def test_correct_answer_passes(client, monkeypatch):
    import app as app_module
    monkeypatch.setattr(app_module, "CAPTCHA_ENABLED", True)
    answer = _sum(client)
    resp = client.post("/apply", data={"mobile": "9876543210", "captcha": str(answer)})
    assert resp.status_code == 302


def test_field_is_required_in_the_browser(client, monkeypatch):
    import app as app_module
    monkeypatch.setattr(app_module, "CAPTCHA_ENABLED", True)
    assert 'name="captcha" required' in client.get("/apply").get_data(as_text=True)