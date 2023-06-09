from flask import Flask, render_template, redirect, url_for, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

app = Flask(__name__)
app.config.from_pyfile("config.cfg")

db.init_app(app)

# make the table
class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    complete = db.Column(db.Boolean)

with app.app_context():
    db.create_all()

@app.route("/")
def home():
    todo_list = db.session.query(Todo).all()
    return render_template('todo.html' , todo_list = todo_list)

@app.route("/add" ,methods=['POST'])
def add():
    title = request.form.get('title')
    new_todo = Todo(title=title, complete = False)
    db.session.add(new_todo)
    db.session.commit()
    return redirect(url_for('home'))

@app.route("/update/<int:todo_id>")
def update(todo_id):
    todo = db.session.query(Todo).filter(Todo.id == todo_id).first()
    todo.complete = not todo.complete
    db.session.commit()
    return redirect(url_for('home'))

@app.route("/delete/<int:todo_id>")
def delete(todo_id):
    todo = db.session.query(Todo).filter(Todo.id == todo_id).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect(url_for('home'))

if __name__=="__main__":
    app.run()