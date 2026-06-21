from app import db

class Tecnico(db.Model):
    __tablename__ = 'tecnicos'
    id = db.Column('id_tecnico', db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    especialidad = db.Column(db.String(100), nullable=False)
    estado = db.Column(db.Enum('activo', 'inactivo'), default='activo')

    # Relación muchos a muchos con tickets a través de tabla intermedia
    tickets_asignados = db.relationship('Ticket', secondary='ticket_tecnico', back_populates='tecnicos_asignados')
    
    # Relación con intervenciones
    intervenciones = db.relationship('Intervencion', backref='tecnico_actuante', lazy=True)
