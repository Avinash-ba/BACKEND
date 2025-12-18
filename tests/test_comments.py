import sys
import os
import json
import pytest

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import server
from app.db import db

flask_app = server.app


@pytest.fixture
def client():
    flask_app.config["TESTING"] = True
    flask_app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"

    with flask_app.test_client() as client:
        with flask_app.app_context():
            db.create_all()
        yield client
        with flask_app.app_context():
            db.drop_all()


def test_create_comment(client):
    response = client.post(
        "/tasks/1/comments",
        data=json.dumps({"content": "Test comment"}),
        content_type="application/json"
    )
    assert response.status_code == 201


def test_get_comments(client):
    client.post(
        "/tasks/1/comments",
        data=json.dumps({"content": "Another comment"}),
        content_type="application/json"
    )
    response = client.get("/tasks/1/comments")
    assert response.status_code == 200


def test_update_comment(client):
    post = client.post(
        "/tasks/1/comments",
        data=json.dumps({"content": "Old"}),
        content_type="application/json"
    )
    cid = post.json["id"]
    response = client.put(
        f"/comments/{cid}",
        data=json.dumps({"content": "Updated"}),
        content_type="application/json"
    )
    assert response.status_code == 200


def test_delete_comment(client):
    post = client.post(
        "/tasks/1/comments",
        data=json.dumps({"content": "Delete me"}),
        content_type="application/json"
    )
    cid = post.json["id"]
    response = client.delete(f"/comments/{cid}")
    assert response.status_code == 200
