def test_register_and_login(client, user_credentials, login):
    r = client.post("/auth/register", json=user_credentials)
    assert r.status_code == 201, r.text
    body = r.json()
    assert body["email"] == user_credentials["email"]
    assert body["role"] == "user"
    assert "id" in body

    token = login(user_credentials["email"], user_credentials["password"])
    assert isinstance(token, str)
    assert len(token) > 10


def test_register_duplicate_email(client, user_credentials):
    r1 = client.post("/auth/register", json=user_credentials)
    assert r1.status_code == 201

    r2 = client.post("/auth/register", json=user_credentials)
    assert r2.status_code == 400
    assert r2.json()["detail"] == "Email already registered"


def test_login_wrong_password(client, user_credentials):
    client.post("/auth/register", json=user_credentials)

    r = client.post(
        "/auth/login",
        data={"username": user_credentials["email"], "password": "wrong"},
        headers={"content-type": "application/x-www-form-urlencoded"},
    )
    assert r.status_code == 401
