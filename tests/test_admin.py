from app.models import User


def test_admin_users_forbidden_for_regular_user(client, user_credentials, login):
    client.post("/auth/register", json=user_credentials)
    token = login(user_credentials["email"], user_credentials["password"])

    r = client.get("/admin/users", headers={"Authorization": f"Bearer {token}"})
    assert r.status_code == 403


def test_admin_users_allowed_for_admin(client, db_session, admin_credentials, login):
    client.post("/auth/register", json=admin_credentials)

    admin = db_session.query(User).filter(User.email == admin_credentials["email"]).first()
    assert admin is not None
    admin.role = "admin"
    db_session.commit()

    token = login(admin_credentials["email"], admin_credentials["password"])

    r = client.get("/admin/users", headers={"Authorization": f"Bearer {token}"})
    assert r.status_code == 200, r.text
    body = r.json()
    assert isinstance(body, list)
    assert any(u["email"] == admin_credentials["email"] for u in body)
