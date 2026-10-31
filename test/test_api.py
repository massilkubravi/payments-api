def test_home(client):
    response = client.get("/")

    assert response.status_code == 200
    assert response.json() == {
        "message": "Welcome to Payments API"
    }


def test_create_account(client):
    response = client.post(
        "/accounts",
        json={
            "owner_name": "Test User",
            "initial_balance": 5000
        }
    )

    assert response.status_code == 200
    assert response.json()["owner_name"] == "Test User"
    assert response.json()["balance"] == 5000