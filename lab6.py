# 4. Страница с таблицей данных.
# 6. FastAPI «Hello».
# 10. Простейший REST API список задач.
# 5. REST API для заметок.
# 9. Подключение SQLAlchemy.
from random import randint
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy import Column, Integer, String, Text, Boolean, create_engine

from flask import Flask,render_template,jsonify,request

app = Flask(__name__, template_folder = ".")
DATABASE_URL = "postgresql://postgres:123456@localhost/lab6"
engine = create_engine(DATABASE_URL)
Base = declarative_base()

class Task(Base):
    __tablename__ = "tasks"
    id = Column(Integer, primary_key=True)
    title = Column(String(200), nullable=False)
    description = Column(Text, nullable=True)
    completed = Column(Boolean, default=False)
    
    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description or '',
            'completed': self.completed
        }

Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)

@app.route("/hello")
def hello():
    return "Hello"

@app.route("/table")
def table():
    return render_template("table.html", header = "Table", table = [[randint(1,10) for column in range(10)] for string in range(3)])


@app.route('/api/tasks', methods=['GET'])
def get_tasks():
    with Session() as session:
        tasks = session.query(Task).all()
        return jsonify([t.to_dict() for t in tasks]), 200

@app.route('/api/tasks/<int:task_id>', methods=['GET'])
def get_task(task_id):
    with Session() as session:
        task = session.query(Task).get(task_id)
        if task:
            return jsonify(task.to_dict()), 200
        return jsonify({'error': 'Task not found'}), 404

@app.route('/api/tasks', methods=['POST'])
def create_task():
    data = request.json
    if not data or 'title' not in data:
        return jsonify({'error': 'Title is required'}), 400
    
    with Session() as session:
        task = Task(
            title=data['title'],
            description=data.get('description', ''),
            completed=data.get('completed', False)
        )
        session.add(task)
        session.commit()
        session.refresh(task)
        return jsonify(task.to_dict()), 201

@app.route('/api/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    data = request.json
    if data is None:
        return jsonify({'error': 'No JSON data provided'}), 400
    
    with Session() as session:
        task = session.query(Task).get(task_id)
        if not task:
            return jsonify({'error': 'Task not found'}), 404
        
        if 'title' in data: task.title = data['title']
        if 'description' in data: task.description = data['description']
        if 'completed' in data: task.completed = data['completed']
        
        session.commit()
        session.refresh(task)
        return jsonify(task.to_dict()), 200

@app.route('/api/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    with Session() as session:
        task = session.query(Task).get(task_id)
        if not task:
            return jsonify({'error': 'Task not found'}), 404
        
        session.delete(task)
        session.commit()
        return jsonify({'message': 'Task deleted successfully'}), 200

@app.route('/api/tasks/<int:task_id>/toggle', methods=['PATCH'])
def toggle_task(task_id):
    with Session() as session:
        task = session.query(Task).get(task_id)
        if not task:
            return jsonify({'error': 'Task not found'}), 404
        
        task.completed = not task.completed
        session.commit()
        session.refresh(task)
        return jsonify(task.to_dict()), 200

app.run(debug = True)
