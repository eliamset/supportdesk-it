from app import db

class Empleado(db.Model):
    __tablename__ = 'empleados'
    id = db.Column('id_empleado', db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    area = db.Column(db.String(100), nullable=False)
    correo = db.Column(db.String(100), unique=True, nullable=False)
    telefono = db.Column(db.String(20))

    # Relación uno a muchos: Un empleado puede tener muchos tickets
    tickets = db.relationship('Ticket', backref='solicitante', lazy=True)
