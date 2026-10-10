from datetime import datetime
import app as app_module

def test_countdown_uses_ist_not_server_time(monkeypatch):
    # 31 Oct 2026, 23:30 IST -> 30 minutes left -> 0 whole hours, but still open
    monkeypatch.setattr(app_module, "now_ist", lambda: datetime(2026, 10, 31, 23, 30))
    assert app_module.deadline_remaining() == 0

def test_window_is_closed_after_midnight_ist(monkeypatch):
    monkeypatch.setattr(app_module, "now_ist", lambda: datetime(2026, 11, 1, 0, 0, 30))
    assert app_module.deadline_remaining() is None

def test_application_number_year_follows_ist(monkeypatch):
    monkeypatch.setattr(app_module, "now_ist", lambda: datetime(2027, 1, 1, 0, 10))
    assert app_module.new_application_no().startswith("SSP27")