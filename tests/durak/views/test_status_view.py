def test_visit_status_page(client):
    assert client.get("/status").json() == {"status": "ok"}
