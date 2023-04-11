from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


#TODO: 1:Estilizar app

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Todos(db.Model):
    _id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.String(500), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow())


@app.route('/', methods=['POST', 'GET'])
def home():
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        todo = Todos(title=title, description=description)
        db.session.add(todo)
        db.session.commit()
    
    
    
    
    all_todos = Todos.query.all()
    return render_template('index.html', todos=all_todos)


@app.route('/create', methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        todos = Todos(title=title, description=description)
        db.session.add(todos)
        db.session.commit()
        return redirect(url_for('index'))
    return redirect('/', todos=todos)
    
@app.route('/delete/<int:_id>', methods=['GET','POST'])
def delete(_id):
    todos = Todos.query.filter_by(_id=_id).first()
    db.session.delete(todos)
    db.session.commit()
    return redirect('/')
    
@app.route('/update/<int:_id>', methods=['GET', 'POST'])
def update(_id):
    if request.method=='POST':
        title = request.form['title']
        description = request.form['description']
        todo = Todos.query.filter_by(_id=_id).first()
        todo.title = title
        todo.description = description
        db.session.add(todo)
        db.session.commit()
        return redirect('/')
    todo = Todos.query.filter_by(_id=_id).first()
    return render_template('edit.html', todo=todo)

if __name__ == '__main__':
    app.run(debug=True)