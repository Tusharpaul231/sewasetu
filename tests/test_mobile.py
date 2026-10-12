import pytest

@pytest.mark.parametrize("typed, expected", [
    ("", "enter your mobile number"),
    ("98765abcde", "digits only"),
    ("98765", "exactly 10 digits"),
])
def test_apply_error_tells_what_is_wrong(client, typed, expected):
    body = client.post("/apply", data={"mobile": typed}).get_data(as_text=True)
    assert expected in body
    assert "Something went wrong" not in body