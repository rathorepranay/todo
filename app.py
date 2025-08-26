from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_migrate import Migrate

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///todo.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
migrte = Migrate(app, db)
# Todo model
class Todo(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.String(500), nullable=False)
    dateCreated = db.Column(db.DateTime, default=datetime.utcnow)
    done = db.Column(db.Boolean, default=False)  # checkbox column

    def __repr__(self):
        return f"{self.sno} - {self.title}"

with app.app_context():
    db.create_all()

# Home route
@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        title = request.form.get('title')
        desc = request.form.get('desc')
        if title and desc:
            todo = Todo(title=title, description=desc)
            db.session.add(todo)
            db.session.commit()
        return redirect(url_for('home'))

    alltodo = Todo.query.all()
    return render_template('index.html', alltodo=alltodo)

# Delete todo
@app.route('/delete/<int:sno>')
def delete(sno):
    todo = Todo.query.get_or_404(sno)
    db.session.delete(todo)
    db.session.commit()
    return redirect(url_for('home'))

# Update todo
@app.route('/update/<int:sno>', methods=['GET', 'POST'])
def update(sno):
    todo = Todo.query.get_or_404(sno)
    if request.method == 'POST':
        todo.title = request.form['title']
        todo.description = request.form['desc']
        db.session.commit()
        return redirect(url_for('home'))
    return render_template('update.html', todo=todo)

# Toggle checkbox
@app.route('/toggle/<int:sno>', methods=['POST'])
def toggle(sno):
    todo = Todo.query.get_or_404(sno)
    todo.done = not todo.done
    db.session.commit()
    return jsonify({'success': True, 'done': todo.done})

# About page
@app.route('/about')
def about():
    return render_template('about.html')

if __name__ == "__main__":
    app.run(debug=True)
