from app import db

class Categoria(db.Model):
    __tablename__ = 'categorias'
    id = db.Column('id_categoria', db.Integer, primary_key=True)
    nombre_categoria = db.Column(db.String(100), nullable=False)

    # Relación uno a muchos: Una categoría puede tener muchos tickets
    tickets = db.relationship('Ticket', backref='categoria', lazy=True)
