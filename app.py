from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tasks.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Modelo de datos
>>>>>>> ac7c540 (app.py created online with Bitbucket)
class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), nullable=False)
    completed = db.Column(db.Boolean, default=False)

# Ruta de inicio
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        task_title = request.form.get("title")
        if task_title:
            new_task = Task(title=task_title)
            db.session.add(new_task)
            db.session.commit()
            return redirect(url_for("index"))

    tasks = Task.query.all()
    return render_template("index.html", tasks=tasks)

# Ruta para marcar tareas como completadas
@app.route("/complete/<int:task_id>")
def complete(task_id):
    task = Task.query.get(task_id)
    if task:
        task.completed = True
        db.session.commit()
    return redirect(url_for("index"))

# Ruta para eliminar una tarea
@app.route("/delete/<int:task_id>")
def delete(task_id):
    task = Task.query.get(task_id)
    if task:
        db.session.delete(task)
        db.session.commit()
    return redirect(url_for("index"))

if __name__ == "__main__":
    with app.app_context():  # Esto asegura que estés dentro del contexto de la aplicación
    	db.create_all()
    app.run(host="0.0.0.0", port=5000)
