from datetime import date


def _verified(client):
    with client.session_transaction() as s:
        s["verified_mobile"] = "9876543210"


def test_name_of_only_digits_is_rejected(client):
    _verified(client)
    resp = client.post("/form/1", data={"applicant_name": "12345", "dob": "1950-02-25"})
    assert resp.status_code == 200 and "using letters" in resp.get_data(as_text=True)


def test_bank_account_with_letters_is_rejected(client):
    _verified(client)
    resp = client.post("/form/3", data={"bank_account": "12ab56789012", "ifsc": "SBIN0001234"})
    assert resp.status_code == 200 and "only digits" in resp.get_data(as_text=True)


def test_date_picker_format_is_accepted(client):
    _verified(client)
    resp = client.post("/form/1", data={"applicant_name": "Sita Devi", "dob": "1950-02-25"})
    assert resp.status_code == 302


def test_typed_date_is_read_day_first(client):
    import app as app_module
    assert app_module.parse_dob("01/02/1950") == date(1950, 2, 1)