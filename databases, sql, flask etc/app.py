from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///example.db"
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)

# Create tables (run once)
with app.app_context():
    db.create_all()


@app.route("/users/create/<name>")
def create_user(name):
    u = User(name=name)
    db.session.add(u)
    db.session.commit()
    return f"User {name} created with id {u.id}"

@app.route("/users")
def list_users():
    users = User.query.all()
    return ", ".join(f"{u.id}:{u.name}" for u in users)
