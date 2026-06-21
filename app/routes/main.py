from flask import Blueprint, render_template
from flask_login import login_required
from app.models.ticket import Ticket
from app.models.employee import Empleado
from app.models.technician import Tecnico

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
@login_required
def index():
    ticket_count = Ticket.query.count()
    employee_count = Empleado.query.count()
    technician_count = Tecnico.query.count()
    recent_tickets = Ticket.query.order_by(Ticket.fecha_creacion.desc()).limit(5).all()
    
    return render_template('dashboard/index.html', 
                           ticket_count=ticket_count,
                           employee_count=employee_count,
                           technician_count=technician_count,
                           recent_tickets=recent_tickets)
