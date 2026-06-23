import re
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required
from app.models.employee import Empleado
from app import db

employee_bp = Blueprint('employee', __name__, url_prefix='/employees')

@employee_bp.route('/')
@login_required
def list():
    employees = Empleado.query.all()
    return render_template('employee/list.html', employees=employees)

@employee_bp.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    if request.method == 'POST':
        nombre = request.form.get('nombre')
        area = request.form.get('area')
        correo = request.form.get('correo')
        telefono = request.form.get('telefono')
        
        if not re.match(r'^[a-zA-ZáéíóúÁÉÍÓÚñÑ\s]+$', nombre):
            flash('Error: El nombre contiene caracteres inválidos o emojis.', 'danger')
            return render_template('employee/form.html', title='Nuevo Empleado')
        if not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', correo):
            flash('Error: Formato de correo electrónico inválido.', 'danger')
            return render_template('employee/form.html', title='Nuevo Empleado')
        if telefono and not re.match(r'^[0-9+\-\s]+$', telefono):
            flash('Error: El teléfono contiene caracteres inválidos.', 'danger')
            return render_template('employee/form.html', title='Nuevo Empleado')
        
        new_employee = Empleado(nombre=nombre, area=area, correo=correo, telefono=telefono)
        db.session.add(new_employee)
        db.session.commit()
        flash('Empleado creado exitosamente', 'success')
        return redirect(url_for('employee.list'))
        
    return render_template('employee/form.html', title='Nuevo Empleado')

@employee_bp.route('/update/<int:id>', methods=['GET', 'POST'])
@login_required
def update(id):
    employee = Empleado.query.get_or_404(id)
    if request.method == 'POST':
        nombre = request.form.get('nombre')
        correo = request.form.get('correo')
        telefono = request.form.get('telefono')
        
        if not re.match(r'^[a-zA-ZáéíóúÁÉÍÓÚñÑ\s]+$', nombre):
            flash('Error: El nombre contiene caracteres inválidos o emojis.', 'danger')
            return render_template('employee/form.html', employee=employee, title='Editar Empleado')
        if not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', correo):
            flash('Error: Formato de correo electrónico inválido.', 'danger')
            return render_template('employee/form.html', employee=employee, title='Editar Empleado')
        if telefono and not re.match(r'^[0-9+\-\s]+$', telefono):
            flash('Error: El teléfono contiene caracteres inválidos.', 'danger')
            return render_template('employee/form.html', employee=employee, title='Editar Empleado')
            
        employee.nombre = nombre
        employee.area = request.form.get('area')
        employee.correo = correo
        employee.telefono = telefono
        db.session.commit()
        flash('Empleado actualizado', 'success')
        return redirect(url_for('employee.list'))
        
    return render_template('employee/form.html', employee=employee, title='Editar Empleado')

@employee_bp.route('/delete/<int:id>', methods=['POST'])
@login_required
def delete(id):
    from app.models.ticket import ticket_tecnico
    from app.models.intervention import Intervencion
    from app.models.ticket import Ticket

    employee = Empleado.query.get_or_404(id)

    # Verificar tickets activos (no terminados)
    estados_activos = ['Abierto', 'En progreso', 'En espera']
    tickets_activos = [t for t in employee.tickets if t.estado in estados_activos]

    if tickets_activos:
        flash(
            f'No se puede eliminar a "{employee.nombre}" porque tiene '
            f'{len(tickets_activos)} ticket(s) activo(s). '
            'Cierra o reasigna esos tickets primero.',
            'danger'
        )
        return redirect(url_for('employee.list'))

    # Eliminar en cascada: intervenciones → asignaciones → tickets → empleado
    for ticket in employee.tickets:
        Intervencion.query.filter_by(ticket_id=ticket.id).delete()
        db.session.execute(
            ticket_tecnico.delete().where(ticket_tecnico.c.ticket_id == ticket.id)
        )
        db.session.delete(ticket)

    db.session.delete(employee)
    db.session.commit()
    flash(f'Empleado "{employee.nombre}" eliminado correctamente.', 'warning')
    return redirect(url_for('employee.list'))
