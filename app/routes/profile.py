from flask import Blueprint, render_template, session, redirect, url_for
from ..models import Post, User
from .. import db

profile_bp = Blueprint('profile', __name__)

@profile_bp.route('/perfil/<username>')
def user_profile(username):
    if 'user' not in session:
        return redirect(url_for('auth.login'))
        
    target_user = User.query.filter_by(username=username).first()
    if not target_user:
        return "Usuário não encontrado", 404
        
    # Usando o relacionamento target_user.posts
    posts = Post.query.filter_by(user_id=target_user.id).order_by(Post.timestamp.desc()).all()
    
    return render_template('profile/index.html', 
                           posts=posts, 
                           profile_user=target_user, 
                           current_user=session['user'])
