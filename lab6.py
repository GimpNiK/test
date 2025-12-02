# 4. Страница с таблицей данных.
# 6. FastAPI «Hello».
# 10. Простейший REST API список задач.
# 5. REST API для заметок.
# 9. Подключение SQLAlchemy.

from flask import Flask,render_template

app = Flask(__name__, template_folder = ".")

@app.route("/hello")
def hello():
    return "Hello"

from random import randint
@app.route("/table")
def table():
    return render_template("table.html", header = "Table", table = [[randint(1,10) for column in range(10)] for string in range(3)])

app.run(debug=True)