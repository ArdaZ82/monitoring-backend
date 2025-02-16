from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)  # Asegúrate de que esta línea existe
    role = db.Column(db.String(20), nullable=False, default='user')


class Captura(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)
    ruta = db.Column(db.String(255), nullable=False)

class Tarea(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)
    mensaje = db.Column(db.String(255), nullable=False)
    completada = db.Column(db.Boolean, default=False)
