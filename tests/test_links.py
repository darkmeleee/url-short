def test_shorten_requires_auth(client):
    r = client.post("/shorten", json={"url": "https://example.com"})
    assert r.status_code == 401


def test_shorten_and_redirect(client, user_credentials, login):
    client.post("/auth/register", json=user_credentials)
    token = login(user_credentials["email"], user_credentials["password"])

    r = client.post(
        "/shorten",
        json={"url": "https://example.com"},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert r.status_code == 200, r.text
    body = r.json()
    assert body["target_url"] == "https://example.com/"
    assert body["key"]
    assert body["owner_id"] is not None

    key = body["key"]

    ref = client.get(f"/link?key={key}", follow_redirects=False)
    assert ref.status_code in (302, 307)
    assert ref.headers["location"] == "https://example.com/"


def test_redirect_not_found(client):
    r = client.get("/link?key=does-not-exist", follow_redirects=False)
    assert r.status_code == 404
