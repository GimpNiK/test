# 4. Страница с таблицей данных.
# 6. FastAPI «Hello».
# 10. Простейший REST API список задач.
# 5. REST API для заметок.
# 9. Подключение SQLAlchemy.

from flask import Flask,render_template

app = Flask(__name__)

@app.route("/hello")
def hello():
    return "Hello"

