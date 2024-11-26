from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

# Crear una instancia de la aplicación Flask
app = Flask(__name__)

# Configuración de la base de datos SQLite
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tasks.db'  # URL de conexión a la base de datos
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Deshabilita las notificaciones de cambios para mejorar el rendimiento

# Inicialización de SQLAlchemy para gestionar la base de datos
db = SQLAlchemy(app)

# Modelo de datos para representar una tarea
class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # Identificador único de la tarea
    title = db.Column(db.String(80), nullable=False)  # Título de la tarea, requerido
    completed = db.Column(db.Boolean, default=False)  # Estado de la tarea (completada o no)

# Ruta principal para mostrar y añadir tareas
@app.route("/", methods=["GET", "POST"])
def index():
    """
    Maneja la página de inicio.
    - GET: Muestra la lista de tareas.
    - POST: Añade una nueva tarea a la base de datos.
    """
    if request.method == "POST":
        task_title = request.form.get("title")  # Obtiene el título de la tarea del formulario
        if task_title:
            new_task = Task(title=task_title)  # Crea una nueva instancia de Task
            db.session.add(new_task)  # Añade la tarea a la sesión
            db.session.commit()  # Guarda los cambios en la base de datos
            return redirect(url_for("index"))  # Redirige a la página principal

    tasks = Task.query.all()  # Recupera todas las tareas de la base de datos
    return render_template("index.html", tasks=tasks)  # Renderiza la plantilla con las tareas

# Ruta para marcar una tarea como completada
@app.route("/complete/<int:task_id>")
def complete(task_id):
    """
    Marca una tarea como completada.
    - task_id: ID de la tarea a completar.
    """
    task = Task.query.get(task_id)  # Obtiene la tarea por su ID
    if task:
        task.completed = True  # Actualiza el estado de la tarea
        db.session.commit()  # Guarda los cambios en la base de datos
    return redirect(url_for("index"))  # Redirige a la página principal

# Ruta para eliminar una tarea
@app.route("/delete/<int:task_id>")
def delete(task_id):
    """
    Elimina una tarea de la base de datos.
    - task_id: ID de la tarea a eliminar.
    """
    task = Task.query.get(task_id)  # Obtiene la tarea por su ID
    if task:
        db.session.delete(task)  # Elimina la tarea de la sesión
        db.session.commit()  # Guarda los cambios en la base de datos
    return redirect(url_for("index"))  # Redirige a la página principal

# Punto de entrada de la aplicación
if __name__ == "__main__":
    # Asegura que las tablas en la base de datos estén creadas antes de ejecutar la app
    with app.app_context():
        db.create_all()  # Crea las tablas definidas en los modelos si no existen
    # Ejecuta la aplicación en el puerto 5000
    app.run(host="0.0.0.0", port=5000)
