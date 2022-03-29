from app import db
from flask_login import UserMixin
  
    
class Cliente(UserMixin, db.Model):
    __tablename__ = 'clientes'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(80), unique=True, nullable=False)
    senha = db.Column(db.String(120), nullable=False)
    status = db.Column(db.Boolean, nullable=False)
    foto_perfil = db.Column(db.LargeBinary)
    data_criacao = db.Column(db.DateTime, default=db.func.current_timestamp())
    data_modificacao = db.Column(db.DateTime, default=db.func.current_timestamp())

    def __init__(self, nome, email, senha, status):
        self.nome = nome
        self.email = email
        self.senha = senha
        self.status = status
    
    def __repr__(self):
        return 'Cliente %r' % self.nome