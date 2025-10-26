"""
Unit tests for API
"""
import io
import pickle
from fastapi.testclient import TestClient
from sklearn.linear_model import LinearRegression
from main import app

client = TestClient(app)


def test_health():
    """
        Test healthcheck route
    """
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_load_model_success():
    """
        Test success for model load route
    """
    model = LinearRegression()
    data = pickle.dumps(model)
    file = io.BytesIO(data)

    response = client.post(
        "/model/load",
        files={"data": ("model.pkl", file, "application/octet-stream")}
    )

    assert response.status_code == 200
    assert response.json() == {"message": "Model loaded successfully"}


def test_error_load_model():
    model = io.BytesIO(b"Not a LinearRegression model")

    response = client.post(
        "/model/load",
        files={"data": ("model.pkl", model, "application/octet-stream")}
    )

    assert response.status_code == 400
    assert "Cannot load model" in response.json()["detail"]
