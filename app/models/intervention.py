from app import db
from datetime import datetime

class Intervencion(db.Model):
    __tablename__ = 'intervenciones'
    id = db.Column('id_intervencion', db.Integer, primary_key=True)
    ticket_id = db.Column(db.Integer, db.ForeignKey('tickets.id_ticket'), nullable=False)
    tecnico_id = db.Column(db.Integer, db.ForeignKey('tecnicos.id_tecnico'), nullable=False)
    descripcion = db.Column(db.Text, nullable=False)
    fecha = db.Column(db.DateTime, default=datetime.utcnow)
