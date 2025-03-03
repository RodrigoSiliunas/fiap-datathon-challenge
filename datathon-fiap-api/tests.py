from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_predict_no_user():
    """Teste para prever notícias sem fornecer user_id (cold-start)."""
    response = client.get("/predict/?top_n=5")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 5
    assert "page" in data[0]

def test_predict_with_user():
    """Teste para prever recomendações para um usuário específico. Que no caso não existe."""
    response = client.get("/predict/?user_id=user123&top_n=3")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 3
    assert "page" in data[0]

def test_predict_invalid_user():
    """Teste para um user_id que não existe no dataset. Também cold_start, um tanto redundante."""
    response = client.get("/predict/?user_id=usuario_inexistente&top_n=3")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 3

if __name__ == "__main__":
    import pytest
    pytest.main()
