

from flask import Flask, request, render_template, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///todo.db"
db = SQLAlchemy(app)

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), nullable=False)
    desc = db.Column(db.String(500), nullable=False)
    date = db.Column(db.DateTime, default =datetime.utcnow)

    def __repr__(self):
        return {self.title} - {self.desc}

@app.route('/')
def home():
    todo = Todo.query.all()
    return render_template('index.html', todo=todo)

@app.route('/post', methods=['GET', 'POST'])
def post():
    if request.method == 'POST':
        title = request.form['title']
        desc = request.form['desc']
        todo = Todo(title=title, desc=desc)
        db.session.add(todo)
        db.session.commit()

        if title != '' and desc != '':
            return redirect('/')
    return redirect('/')

@app.route('/delete/<int:id>')
def delete(id):
    data = Todo.query.get(id)
    db.session.delete(data)
    db.session.commit()
    return redirect('/')

@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    if request.method == 'POST':
        title = request.form['title']
        desc = request.form['desc']
        todo = Todo.query.get(id)
        todo.title = title
        todo.desc = desc
        db.session.add(todo)
        db.session.commit()
        return redirect('/')
    todo = Todo.query.get(id)
    return render_template('update.html', todo=todo)




with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)