def _add(db, mobile, name, no, bank):
    cur = db.cursor()
    cur.execute(
        "INSERT INTO applications (application_no, applicant_name, mobile, dob, gender, "
        "marital_status, village, block, bank_account, ifsc, status, submitted_at) "
        "VALUES (%s,%s,%s,'1950-01-01','Male','Married','V','Sonari',%s,'SBIN0001234',"
        "'PENDING', now()) RETURNING id", (no, name, mobile, bank))
    new_id = cur.fetchone()[0]
    db.commit()
    return new_id


def _login_as(client, mobile):
    with client.session_transaction() as s:
        s["logged_in"] = True
        s["portal_mobile"] = mobile


def test_citizen_can_open_own_application(client, db):
    mine = _add(db, "9000000001", "Me Myself", "SSP26000001", "111111111111")
    _login_as(client, "9000000001")
    assert client.get("/application/%d" % mine).status_code == 200


def test_citizen_cannot_open_someone_elses_application(client, db):
    _add(db, "9000000001", "Me Myself", "SSP26000001", "111111111111")
    theirs = _add(db, "9000000002", "Secret Person", "SSP26000002", "999988887777")
    _login_as(client, "9000000001")
    resp = client.get("/application/%d" % theirs)
    body = resp.get_data(as_text=True)
    assert resp.status_code in (403, 404)
    assert "Secret Person" not in body and "999988887777" not in body


def test_admin_can_open_any_application(client, db):
    theirs = _add(db, "9000000002", "Secret Person", "SSP26000002", "999988887777")
    with client.session_transaction() as s:
        s["logged_in"] = True
        s["admin"] = True
    assert client.get("/application/%d" % theirs).status_code == 200