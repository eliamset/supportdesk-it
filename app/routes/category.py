from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required
from app.models.category import Categoria
from app import db

category_bp = Blueprint('category', __name__, url_prefix='/categories')

@category_bp.route('/')
@login_required
def list():
    categories = Categoria.query.all()
    return render_template('category/list.html', categories=categories)

@category_bp.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    if request.method == 'POST':
        nombre = request.form.get('nombre_categoria')
        new_cat = Categoria(nombre_categoria=nombre)
        db.session.add(new_cat)
        db.session.commit()
        flash('Categoría creada exitosamente', 'success')
        return redirect(url_for('category.list'))
        
    return render_template('category/form.html', title='Nueva Categoría')

@category_bp.route('/update/<int:id>', methods=['GET', 'POST'])
@login_required
def update(id):
    cat = Categoria.query.get_or_404(id)
    if request.method == 'POST':
        cat.nombre_categoria = request.form.get('nombre_categoria')
        db.session.commit()
        flash('Categoría actualizada', 'success')
        return redirect(url_for('category.list'))
        
    return render_template('category/form.html', category=cat, title='Editar Categoría')

@category_bp.route('/delete/<int:id>', methods=['POST'])
@login_required
def delete(id):
    cat = Categoria.query.get_or_404(id)
    db.session.delete(cat)
    db.session.commit()
    flash('Categoría eliminada', 'warning')
    return redirect(url_for('category.list'))
