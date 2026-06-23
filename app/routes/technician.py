import re
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required
from app.models.technician import Tecnico
from app import db

technician_bp = Blueprint('technician', __name__, url_prefix='/technicians')

@technician_bp.route('/')
@login_required
def list():
    technicians = Tecnico.query.all()
    return render_template('technician/list.html', technicians=technicians)

@technician_bp.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    if request.method == 'POST':
        nombre = request.form.get('nombre')
        especialidad = request.form.get('especialidad')
        estado = request.form.get('estado')
        
        if not re.match(r'^[a-zA-ZáéíóúÁÉÍÓÚñÑ\s]+$', nombre):
            flash('Error: El nombre contiene caracteres inválidos o emojis.', 'danger')
            return render_template('technician/form.html', title='Nuevo Técnico')
            
        new_tech = Tecnico(nombre=nombre, especialidad=especialidad, estado=estado)
        db.session.add(new_tech)
        db.session.commit()
        flash('Técnico creado exitosamente', 'success')
        return redirect(url_for('technician.list'))
        
    return render_template('technician/form.html', title='Nuevo Técnico')

@technician_bp.route('/update/<int:id>', methods=['GET', 'POST'])
@login_required
def update(id):
    tech = Tecnico.query.get_or_404(id)
    if request.method == 'POST':
        nombre = request.form.get('nombre')
        if not re.match(r'^[a-zA-ZáéíóúÁÉÍÓÚñÑ\s]+$', nombre):
            flash('Error: El nombre contiene caracteres inválidos o emojis.', 'danger')
            return render_template('technician/form.html', technician=tech, title='Editar Técnico')
            
        tech.nombre = nombre
        tech.especialidad = request.form.get('especialidad')
        tech.estado = request.form.get('estado')
        db.session.commit()
        flash('Técnico actualizado', 'success')
        return redirect(url_for('technician.list'))
        
    return render_template('technician/form.html', technician=tech, title='Editar Técnico')

@technician_bp.route('/delete/<int:id>', methods=['POST'])
@login_required
def delete(id):
    from flask_login import current_user
    if current_user.rol != 'admin':
        flash('Solo los administradores pueden eliminar técnicos.', 'danger')
        return redirect(url_for('technician.list'))
        
    tech = Tecnico.query.get_or_404(id)
    
    from app.models.ticket import ticket_tecnico
    from app.models.intervention import Intervencion
    
    # Eliminar en cascada las asignaciones e intervenciones
    db.session.execute(ticket_tecnico.delete().where(ticket_tecnico.c.tecnico_id == tech.id))
    Intervencion.query.filter_by(tecnico_id=tech.id).delete()
    
    db.session.delete(tech)
    db.session.commit()
    flash(f'Técnico "{tech.nombre}" eliminado correctamente', 'warning')
    return redirect(url_for('technician.list'))
