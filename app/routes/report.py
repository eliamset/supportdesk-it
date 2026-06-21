from flask import Blueprint, render_template, request
from flask_login import login_required
from app.models import Ticket, Tecnico
from app import db
from sqlalchemy import func

report_bp = Blueprint('report', __name__, url_prefix='/reports')

@report_bp.route('/')
@login_required
def index():
    # Tickets por estado
    status_counts = db.session.query(Ticket.estado, func.count(Ticket.id)).group_by(Ticket.estado).all()
    
    # Tickets por técnico (Resueltos vs Pendientes)
    # Definimos 'Resueltos' como Resuelto o Cerrado
    tech_stats = []
    tecnicos = Tecnico.query.all()
    for t in tecnicos:
        resueltos = db.session.query(func.count(Ticket.id)).join(Ticket.tecnicos_asignados).filter(
            Tecnico.id == t.id,
            Ticket.estado.in_(['Resuelto', 'Cerrado'])
        ).scalar()
        
        pendientes = db.session.query(func.count(Ticket.id)).join(Ticket.tecnicos_asignados).filter(
            Tecnico.id == t.id,
            Ticket.estado.in_(['Abierto', 'En progreso', 'En espera'])
        ).scalar()
        
        # Tiempo promedio de resolución (en días)
        avg_time = db.session.query(
            func.avg(func.datediff(Ticket.fecha_cierre, Ticket.fecha_creacion))
        ).join(Ticket.tecnicos_asignados).filter(
            Tecnico.id == t.id,
            Ticket.fecha_cierre.isnot(None)
        ).scalar()
        
        tech_stats.append({
            'nombre': t.nombre,
            'resueltos': resueltos or 0,
            'pendientes': pendientes or 0,
            'avg_time': round(avg_time, 2) if avg_time else 0
        })

    return render_template('report/index.html', 
                           status_counts=status_counts,
                           tech_stats=tech_stats)
