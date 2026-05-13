from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from ..models import User
from .. import db

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        user = User.query.filter_by(username=username).first()
        if user and user.password == password:
            # Armazenamos os dados básicos na sessão
            session['user'] = user.to_dict()
            return redirect(url_for('feed.index'))
        
        flash('Usuário ou senha incorretos!', 'danger')
    
    return render_template('auth/login.html')

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        nome = request.form.get('nome')
        password = request.form.get('password')
        
        if User.query.filter_by(username=username).first():
            flash('Este @username já existe!', 'warning')
        else:
            new_user = User(username=username, nome=nome, password=password)
            db.session.add(new_user)
            db.session.commit()
            flash('Conta criada com sucesso! Faça login.', 'success')
            return redirect(url_for('auth.login'))
            
    return render_template('auth/login.html', register_mode=True)

@auth_bp.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('auth.login'))
