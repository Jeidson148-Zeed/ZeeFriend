import os
from flask import Blueprint, render_template, request, redirect, url_for, session, current_app
from ..models import Post, User
from .. import db

feed_bp = Blueprint('feed', __name__)

@feed_bp.route('/')
def index():
    if 'user' not in session:
        return redirect(url_for('auth.login'))
    
    # Busca todos os posts ordenados pelo mais recente
    posts = Post.query.order_by(Post.timestamp.desc()).all()
    return render_template('feed/index.html', posts=posts, user=session['user'])

@feed_bp.route('/postar', methods=['POST'])
def postar():
    if 'user' not in session:
        return redirect(url_for('auth.login'))
        
    user_id = session['user']['id']
    texto = request.form.get('texto')
    foto = request.files.get('foto')
    
    nome_foto = None
    if foto and foto.filename:
        nome_foto = foto.filename
        caminho = os.path.join(current_app.config['UPLOAD_FOLDER'], nome_foto)
        # Garantir que o diretório existe (caso tenha sido deletado)
        os.makedirs(os.path.dirname(caminho), exist_ok=True)
        foto.save(caminho)
    
    new_post = Post(texto=texto, foto=nome_foto, user_id=user_id)
    db.session.add(new_post)
    db.session.commit()
    
    return redirect(url_for('feed.index'))
