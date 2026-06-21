from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app.models import Ticket, Empleado, Tecnico, Categoria, Intervencion, Usuario
from app import db
from datetime import datetime

ticket_bp = Blueprint('ticket', __name__, url_prefix='/tickets')

@ticket_bp.route('/')
@login_required
def list():
    status_filter = request.args.get('estado')
    priority_filter = request.args.get('prioridad')
    tech_filter = request.args.get('tecnico_id')
    
    query = Ticket.query
    
    if status_filter:
        query = query.filter(Ticket.estado == status_filter)
    if priority_filter:
        query = query.filter(Ticket.prioridad == priority_filter)
    if tech_filter:
        query = query.join(Ticket.tecnicos_asignados).filter(Tecnico.id == tech_filter)
        
    tickets = query.all()
    tecnicos = Tecnico.query.all()
    return render_template('ticket/list.html', tickets=tickets, tecnicos=tecnicos)

@ticket_bp.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    if request.method == 'POST':
        descripcion = request.form.get('descripcion')
        prioridad = request.form.get('prioridad')
        empleado_id = request.form.get('empleado_id')
        categoria_id = request.form.get('categoria_id')
        
        # Regla de negocio: No duplicados (mismo solicitante, categoría, descripción en el mismo día)
        today = datetime.utcnow().date()
        duplicate = Ticket.query.filter(
            Ticket.empleado_id == empleado_id,
            Ticket.categoria_id == categoria_id,
            Ticket.descripcion == descripcion,
            db.func.date(Ticket.fecha_creacion) == today
        ).first()
        
        if duplicate:
            flash('Ya existe un ticket idéntico creado el día de hoy.', 'danger')
        else:
            new_ticket = Ticket(
                descripcion=descripcion,
                prioridad=prioridad,
                empleado_id=empleado_id,
                categoria_id=categoria_id
            )
            db.session.add(new_ticket)
            db.session.commit()
            flash('Ticket creado exitosamente', 'success')
            return redirect(url_for('ticket.list'))
            
    empleados = Empleado.query.all()
    categorias = Categoria.query.all()
    return render_template('ticket/form.html', empleados=empleados, categorias=categorias, title='Nuevo Ticket')

@ticket_bp.route('/view/<int:id>')
@login_required
def view(id):
    ticket = Ticket.query.get_or_404(id)
    tecnicos = Tecnico.query.filter_by(estado='activo').all()
    return render_template('ticket/view.html', ticket=ticket, tecnicos=tecnicos)

@ticket_bp.route('/assign/<int:id>', methods=['POST'])
@login_required
def assign(id):
    ticket = Ticket.query.get_or_404(id)
    tecnico_id = request.form.get('tecnico_id')
    tecnico = Tecnico.query.get(tecnico_id)
    
    if ticket.estado == 'Cerrado':
        flash('No se puede asignar técnicos a un ticket cerrado.', 'danger')
    elif tecnico.estado == 'inactivo':
        flash('No se puede asignar a un técnico inactivo.', 'danger')
    else:
        if tecnico not in ticket.tecnicos_asignados:
            ticket.tecnicos_asignados.append(tecnico)
            db.session.commit()
            flash(f'Técnico {tecnico.nombre} asignado.', 'success')
        else:
            flash('El técnico ya está asignado a este ticket.', 'info')
            
    return redirect(url_for('ticket.view', id=id))

@ticket_bp.route('/intervention/<int:id>', methods=['POST'])
@login_required
def add_intervention(id):
    ticket = Ticket.query.get_or_404(id)
    descripcion = request.form.get('descripcion')
    tecnico_id = request.form.get('tecnico_id') # En un sistema real, esto vendría del usuario logueado si es técnico
    
    if ticket.estado == 'Cerrado':
        flash('No se pueden agregar intervenciones a un ticket cerrado.', 'danger')
        return redirect(url_for('ticket.view', id=id))
        
    new_int = Intervencion(ticket_id=id, tecnico_id=tecnico_id, descripcion=descripcion)
    db.session.add(new_int)
    
    # Si estaba abierto, pasarlo a En progreso
    if ticket.estado == 'Abierto':
        ticket.estado = 'En progreso'
        
    db.session.commit()
    flash('Intervención registrada.', 'success')
    return redirect(url_for('ticket.view', id=id))

@ticket_bp.route('/update_status/<int:id>', methods=['POST'])
@login_required
def update_status(id):
    ticket = Ticket.query.get_or_404(id)
    new_status = request.form.get('estado')
    
    if ticket.estado == 'Cerrado':
        flash('Un ticket cerrado no puede ser modificado.', 'danger')
        return redirect(url_for('ticket.view', id=id))
    
    if new_status == 'Cerrado':
        # Regla: No cerrar sin intervenciones
        if not ticket.intervenciones:
            flash('No se puede cerrar un ticket sin al menos una intervención.', 'danger')
            return redirect(url_for('ticket.view', id=id))
        ticket.fecha_cierre = datetime.utcnow()
    
    ticket.estado = new_status
    db.session.commit()
    flash('Estado actualizado.', 'success')
    return redirect(url_for('ticket.view', id=id))

@ticket_bp.route('/update_priority/<int:id>', methods=['POST'])
@login_required
def update_priority(id):
    ticket = Ticket.query.get_or_404(id)
    new_priority = request.form.get('prioridad')
    
    # Regla: Solo cambiar si está abierto o en espera
    if ticket.estado in ['Abierto', 'En espera']:
        ticket.prioridad = new_priority
        db.session.commit()
        flash('Prioridad actualizada.', 'success')
    else:
        flash('La prioridad solo puede cambiarse si el ticket está Abierto o en Espera.', 'warning')
        
    return redirect(url_for('ticket.view', id=id))

@ticket_bp.route('/delete/<int:id>', methods=['POST'])
@login_required
def delete(id):
    if current_user.rol not in ['admin', 'tecnico']:
        flash('No tienes permisos para eliminar tickets.', 'danger')
        return redirect(url_for('ticket.list'))
        
    ticket = Ticket.query.get_or_404(id)
    
    from app.models.ticket import ticket_tecnico
    
    # Eliminar en cascada las intervenciones y asignaciones
    for intervencion in ticket.intervenciones:
        db.session.delete(intervencion)
        
    db.session.execute(ticket_tecnico.delete().where(ticket_tecnico.c.ticket_id == ticket.id))
    
    db.session.delete(ticket)
    db.session.commit()
    
    # Reiniciar el contador de ID a 1 si ya no quedan tickets
    if Ticket.query.count() == 0:
        from sqlalchemy import text
        db.session.execute(text("ALTER TABLE tickets AUTO_INCREMENT = 1"))
        db.session.commit()
        
    flash(f'Ticket #{id} eliminado correctamente.', 'warning')
    return redirect(url_for('ticket.list'))
