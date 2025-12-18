from flask import Blueprint, request, jsonify
from .db import db
from .models import Task, Comment

api = Blueprint("api", __name__)

@api.route("/tasks", methods=["GET"])
def get_tasks():
    tasks = Task.query.all()
    return jsonify([{"id": t.id, "title": t.title} for t in tasks])


@api.route("/tasks", methods=["POST"])
def create_task():
    data = request.get_json()
    task = Task(title=data["title"])
    db.session.add(task)
    db.session.commit()
    return jsonify({"id": task.id, "title": task.title})


@api.route("/tasks/<int:id>", methods=["PUT"])
def update_task(id):
    task = Task.query.get_or_404(id)
    task.title = request.json["title"]
    db.session.commit()
    return jsonify({"message": "Task updated"})


@api.route("/tasks/<int:id>", methods=["DELETE"])
def delete_task(id):
    task = Task.query.get_or_404(id)
    db.session.delete(task)
    db.session.commit()
    return jsonify({"message": "Task deleted"})



@api.route("/tasks/<int:task_id>/comments", methods=["POST"])
def add_comment(task_id):
    data = request.get_json()
    comment = Comment(content=data["content"], task_id=task_id)
    db.session.add(comment)
    db.session.commit()
    return jsonify({"id": comment.id, "content": comment.content}), 201



@api.route("/tasks/<int:task_id>/comments", methods=["GET"])
def get_comments(task_id):
    comments = Comment.query.filter_by(task_id=task_id).all()
    return jsonify([{"id": c.id, "content": c.content} for c in comments])


@api.route("/comments/<int:id>", methods=["PUT"])
def update_comment(id):
    comment = Comment.query.get_or_404(id)
    comment.content = request.json["content"]
    db.session.commit()
    return jsonify({"message": "Comment updated"})


@api.route("/comments/<int:id>", methods=["DELETE"])
def delete_comment(id):
    comment = Comment.query.get_or_404(id)
    db.session.delete(comment)
    db.session.commit()
    return jsonify({"message": "Comment deleted"})