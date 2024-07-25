from flask import Flask, jsonify, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@127.0.0.1/taskdb'
db = SQLAlchemy(app)

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Task %r>' % self.id

@app.route('/api/tasks', methods=['GET', 'POST'])
def tasks():
    if request.method == 'POST':
        task_content = request.json['content']
        new_task = Todo(content=task_content)
        db.session.add(new_task)
        db.session.commit()
        return jsonify({'id': new_task.id, 'content': new_task.content, 'date_created': new_task.date_created}), 201
    else:
        tasks = Todo.query.order_by(Todo.date_created).all()
        tasks_list = [{'id': task.id, 'content': task.content, 'date_created': task.date_created} for task in tasks]
        return jsonify(tasks_list)

@app.route('/api/tasks/<int:id>', methods=['DELETE', 'PUT'])
def task(id):
    task = Todo.query.get_or_404(id)
    if request.method == 'DELETE':
        db.session.delete(task)
        db.session.commit()
        return jsonify({'result': 'Task deleted'})
    else:
        data = request.json
        task.content = data['content']
        db.session.commit()
        return jsonify({'id': task.id, 'content': task.content, 'date_created': task.date_created})

if __name__ == "__main__":
    app.run(debug=True)
