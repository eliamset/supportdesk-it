from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app.models.user import Usuario
from app import db

user_bp = Blueprint('user', __name__, url_prefix='/users')


def admin_required(f):
    """Decorador: solo permite acceso al rol 'admin'."""
    from functools import wraps
    @wraps(f)
    def decorated(*args, **kwargs):
        if not current_user.is_authenticated or current_user.rol != 'admin':
            flash('Acceso restringido. Solo los administradores pueden gestionar usuarios.', 'danger')
            return redirect(url_for('main.index'))
        return f(*args, **kwargs)
    return decorated


@user_bp.route('/')
@login_required
@admin_required
def list():
    users = Usuario.query.order_by(Usuario.rol, Usuario.username).all()
    return render_template('user/list.html', users=users)


@user_bp.route('/create', methods=['GET', 'POST'])
@login_required
@admin_required
def create():
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '').strip()
        confirm  = request.form.get('confirm_password', '').strip()
        rol      = request.form.get('rol')

        # Validaciones
        if not username or not password or not rol:
            flash('Todos los campos son obligatorios.', 'danger')
            return render_template('user/form.html', title='Nuevo Usuario')

        if password != confirm:
            flash('Las contraseñas no coinciden.', 'danger')
            return render_template('user/form.html', title='Nuevo Usuario')

        if len(password) < 6:
            flash('La contraseña debe tener al menos 6 caracteres.', 'warning')
            return render_template('user/form.html', title='Nuevo Usuario')

        if Usuario.query.filter_by(username=username).first():
            flash(f'El nombre de usuario "{username}" ya está en uso.', 'danger')
            return render_template('user/form.html', title='Nuevo Usuario')

        new_user = Usuario(username=username, rol=rol)
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()
        flash(f'Usuario "{username}" creado exitosamente.', 'success')
        return redirect(url_for('user.list'))

    return render_template('user/form.html', title='Nuevo Usuario')


@user_bp.route('/update/<int:id>', methods=['GET', 'POST'])
@login_required
@admin_required
def update(id):
    user = Usuario.query.get_or_404(id)

    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        rol      = request.form.get('rol')
        password = request.form.get('password', '').strip()
        confirm  = request.form.get('confirm_password', '').strip()

        if not username or not rol:
            flash('El nombre de usuario y el rol son obligatorios.', 'danger')
            return render_template('user/form.html', user=user, title='Editar Usuario')

        # Verificar duplicado de username (excluyendo al mismo usuario)
        existing = Usuario.query.filter_by(username=username).first()
        if existing and existing.id != user.id:
            flash(f'El nombre de usuario "{username}" ya está en uso por otro usuario.', 'danger')
            return render_template('user/form.html', user=user, title='Editar Usuario')

        user.username = username
        user.rol = rol

        # Solo cambiar contraseña si se proporcionó una nueva
        if password:
            if password != confirm:
                flash('Las contraseñas no coinciden.', 'danger')
                return render_template('user/form.html', user=user, title='Editar Usuario')
            if len(password) < 6:
                flash('La contraseña debe tener al menos 6 caracteres.', 'warning')
                return render_template('user/form.html', user=user, title='Editar Usuario')
            user.set_password(password)

        db.session.commit()
        flash(f'Usuario "{username}" actualizado correctamente.', 'success')
        return redirect(url_for('user.list'))

    return render_template('user/form.html', user=user, title='Editar Usuario')


@user_bp.route('/delete/<int:id>', methods=['POST'])
@login_required
@admin_required
def delete(id):
    user = Usuario.query.get_or_404(id)

    # No permitir que el admin se elimine a sí mismo
    if user.id == current_user.id:
        flash('No puedes eliminar tu propia cuenta de administrador.', 'danger')
        return redirect(url_for('user.list'))

    username = user.username
    db.session.delete(user)
    db.session.commit()
    flash(f'Usuario "{username}" eliminado correctamente.', 'warning')
    return redirect(url_for('user.list'))
