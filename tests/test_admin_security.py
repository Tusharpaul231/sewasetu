import os
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def _add(db, mobile, no):
    cur = db.cursor()
    cur.execute(
        "INSERT INTO applications (application_no, applicant_name, mobile, dob, gender, "
        "marital_status, village, block, bank_account, ifsc, status, submitted_at) "
        "VALUES (%s,'Test','%s','1950-01-01','Male','Married','V','Sonari','123456789012',"
        "'SBIN0001234','PENDING', now()) RETURNING id" % ("%s", mobile), (no,))
    new_id = cur.fetchone()[0]
    db.commit()
    return new_id


def _status(db, app_id):
    cur = db.cursor()
    cur.execute("SELECT status FROM applications WHERE id = %s", (app_id,))
    return cur.fetchone()[0]


def test_citizen_cannot_approve_or_reject(client, db):          # bug 48
    app_id = _add(db, "9000000001", "SSP26000001")
    with client.session_transaction() as s:
        s["logged_in"] = True
        s["portal_mobile"] = "9000000002"
    assert client.post("/admin/approve/%d" % app_id).status_code == 403
    assert client.post("/admin/reject/%d" % app_id).status_code == 403
    assert _status(db, app_id) == "PENDING"


def test_admin_can_approve(client, db):                          # guard
    app_id = _add(db, "9000000001", "SSP26000001")
    with client.session_transaction() as s:
        s["logged_in"] = True
        s["admin"] = True
    client.post("/admin/approve/%d" % app_id)
    assert _status(db, app_id) == "APPROVED"


def test_old_vendor_secrets_are_gone_from_the_source():        # bugs 49, 50
    src = open(os.path.join(ROOT, "app", "app.py"), encoding="utf-8").read()
    ini = open(os.path.join(ROOT, "app", "config", "app.ini"), encoding="utf-8").read()
    assert "sewasetu@123" not in src
    assert "donotshare" not in ini and "sewasetu123" not in ini


def test_app_refuses_to_start_without_secrets():                # bugs 49, 50
    env = {k: v for k, v in os.environ.items() if k not in ("SECRET_KEY", "ADMIN_PASSWORD")}
    result = subprocess.run([sys.executable, "-c", "import app"],
                            cwd=os.path.join(ROOT, "app"), env=env, capture_output=True)
    assert result.returncode != 0


def test_admin_login_uses_configured_password_only(client):     # bug 49
    old = client.post("/admin", data={"username": "admin", "password": "sewasetu@123"})
    assert old.status_code == 200                               # re-shown, not logged in
    good = client.post("/admin", data={"username": "admin",
                                       "password": os.environ["ADMIN_PASSWORD"]})
    assert good.status_code == 302


def test_admin_login_survives_non_english_input(client):
    resp = client.post("/admin", data={"username": "অ", "password": "পাসওয়ার্ড"})
    assert resp.status_code == 200