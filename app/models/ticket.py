from app import db
from datetime import datetime

# Tabla intermedia Muchos a Muchos
ticket_tecnico = db.Table('ticket_tecnico',
    db.Column('id_asignacion', db.Integer, primary_key=True),
    db.Column('ticket_id', db.Integer, db.ForeignKey('tickets.id_ticket'), nullable=False),
    db.Column('tecnico_id', db.Integer, db.ForeignKey('tecnicos.id_tecnico'), nullable=False),
    db.Column('fecha_asignacion', db.DateTime, default=datetime.utcnow)
)

class Ticket(db.Model):
    __tablename__ = 'tickets'
    id = db.Column('id_ticket', db.Integer, primary_key=True)
    descripcion = db.Column(db.Text, nullable=False)
    prioridad = db.Column(db.Enum('Baja', 'Media', 'Alta', 'Crítica'), default='Baja')
    estado = db.Column(db.Enum('Abierto', 'En progreso', 'En espera', 'Resuelto', 'Cerrado'), default='Abierto')
    fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow)
    fecha_cierre = db.Column(db.DateTime, nullable=True)
    
    empleado_id = db.Column(db.Integer, db.ForeignKey('empleados.id_empleado'), nullable=False)
    categoria_id = db.Column(db.Integer, db.ForeignKey('categorias.id_categoria'), nullable=False)

    # Relación muchos a muchos con técnicos
    tecnicos_asignados = db.relationship('Tecnico', secondary=ticket_tecnico, back_populates='tickets_asignados')
    
    # Relación uno a muchos con intervenciones
    intervenciones = db.relationship('Intervencion', backref='ticket', lazy=True)

    @property
    def tiempo_resolucion_dias(self):
        if self.fecha_cierre and self.fecha_creacion:
            delta = self.fecha_cierre - self.fecha_creacion
            return delta.days
        return None
