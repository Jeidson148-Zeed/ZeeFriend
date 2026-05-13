import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv

# Carregar variáveis de ambiente do arquivo .env
load_dotenv()

# Instância global do SQLAlchemy
db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    
    # Configurações do arquivo .env
    app.secret_key = os.getenv('SECRET_KEY', 'default_secret_key')
    
    # URL do Banco de Dados (Supabase se disponível, senão SQLite local)
    supabase_url = os.getenv('DATABASE_URL')
    if supabase_url and "[SENHA]" not in supabase_url:
        app.config['SQLALCHEMY_DATABASE_URI'] = supabase_url
    else:
        basedir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'zeifriend.db')
        print("AVISO: Usando SQLite local. Configure o DATABASE_URL no seu .env com a senha real.")

    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # Configuração de upload
    app.config['UPLOAD_FOLDER'] = os.path.join('app', 'static', 'uploads')
    
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])

    # Inicializar db com o app
    db.init_app(app)

    # Registrar Blueprints
    from .routes.auth import auth_bp
    from .routes.feed import feed_bp
    from .routes.profile import profile_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(feed_bp)
    app.register_blueprint(profile_bp)

    # Criar tabelas se não existirem
    with app.app_context():
        from . import models  # Importar modelos para registro
        db.create_all()

    return app
