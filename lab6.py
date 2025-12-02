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

#app.run(debug=True)



from sqlalchemy.orm import declarative_base,Session
from sqlalchemy import Column,Integer,String,create_engine

DATABASE_URL = "postgresql://postgres:123456@localhost/lab6"
Base = declarative_base()
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, autoincrement=True)
    full_name = Column(String(255), nullable=False)

    def __repr__(self):
        return f"User {self.id}: {self.full_name}"
    
engine = create_engine(DATABASE_URL)
Base.metadata.create_all(engine)

# session = Session(bind = engine)
# user = User(full_name = "Valentinov F.A")
# session.add(user)
# session.commit()

# print(session.query(User).all())