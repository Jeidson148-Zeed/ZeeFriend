from . import db
from datetime import datetime

class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    nome = db.Column(db.String(120), nullable=False)
    password = db.Column(db.String(120), nullable=False)
    bio = db.Column(db.String(255), default="Apaixonado por tecnologia e café. ☕💻")
    profile_pic = db.Column(db.String(255))
    cover_pic = db.Column(db.String(255))
    
    # Relacionamento: um usuário tem muitos posts
    posts = db.relationship('Post', backref='author', lazy=True)

    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'nome': self.nome,
            'bio': self.bio
        }

class Post(db.Model):
    __tablename__ = 'posts'
    
    id = db.Column(db.Integer, primary_key=True)
    texto = db.Column(db.Text, nullable=False)
    foto = db.Column(db.String(255))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    
    # FK para o autor
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'texto': self.texto,
            'foto': self.foto,
            'autor': self.author.username,
            'timestamp': self.timestamp.strftime('%Y-%m-%d %H:%M:%S')
        }
