from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)

def test_signup_and_unregistration():
    activity = "Programming Class"
    email = "tester@mergington.edu"

    # ensure not already signed up
    resp = client.delete(f"/activities/{activity}/participants?email={email}")
    # accept either 404 or 400 depending on state
    assert resp.status_code in (400, 404)

    # sign up
    resp = client.post(f"/activities/{activity}/signup?email={email}")
    assert resp.status_code == 200
    assert "Signed up" in resp.json().get("message", "")

    # signing up again should fail
    resp = client.post(f"/activities/{activity}/signup?email={email}")
    assert resp.status_code == 400

    # unregister
    resp = client.delete(f"/activities/{activity}/participants?email={email}")
    assert resp.status_code == 200
    assert "Unregistered" in resp.json().get("message", "")

    # unregister again should error
    resp = client.delete(f"/activities/{activity}/participants?email={email}")
    assert resp.status_code == 400
