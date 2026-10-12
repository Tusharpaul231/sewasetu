M = "9876543210"


def _latest_code(db):
    cur = db.cursor()
    cur.execute("SELECT code FROM otps WHERE mobile=%s ORDER BY id DESC LIMIT 1", (M,))
    return cur.fetchone()[0]


def _wrong(code):
    return "000000" if code != "000000" else "111111"


def test_otp_requests_are_limited_per_number(client):                    # bug 7
    codes = [client.post("/apply", data={"mobile": M}).status_code for _ in range(7)]
    assert codes[0] == 302 and codes[-1] == 429


def test_otp_uses_a_secure_generator(client, db, monkeypatch):           # bug 8
    import app as app_module
    monkeypatch.setattr(app_module.secrets, "randbelow", lambda n: 123456)
    client.post("/apply", data={"mobile": M})
    assert _latest_code(db) == "123456"


def test_otp_is_locked_after_five_wrong_guesses(client, db):             # bug 10
    client.post("/apply", data={"mobile": M})
    code = _latest_code(db)
    for _ in range(5):
        client.post("/verify", data={"otp": _wrong(code)})
    client.post("/verify", data={"otp": code})
    with client.session_transaction() as s:
        assert not s.get("verified_mobile")


def test_otp_field_rejects_non_digits(client):                           # bug 11
    client.post("/apply", data={"mobile": M})
    body = client.post("/verify", data={"otp": "12ab56"}).get_data(as_text=True)
    assert "6 digits" in body
    assert 'inputmode="numeric"' in client.get("/verify").get_data(as_text=True)


def test_resend_creates_a_new_otp(client, db):                           # bug 12
    client.post("/apply", data={"mobile": M})
    assert client.post("/resend").status_code == 302
    cur = db.cursor()
    cur.execute("SELECT count(*) FROM otps WHERE mobile=%s", (M,))
    assert cur.fetchone()[0] == 2


def test_otp_cannot_be_used_twice(client, db):                           # bug 13
    client.post("/apply", data={"mobile": M})
    code = _latest_code(db)
    client.post("/verify", data={"otp": code})
    with client.session_transaction() as s:
        s.pop("verified_mobile", None)
        s["apply_mobile"] = M
    client.post("/verify", data={"otp": code})
    with client.session_transaction() as s:
        assert not s.get("verified_mobile")


def test_wrong_otp_message_helps(client, db):                            # bug 14
    client.post("/apply", data={"mobile": M})
    body = client.post("/verify", data={"otp": _wrong(_latest_code(db))}).get_data(as_text=True)
    assert "not correct" in body and "attempt" in body