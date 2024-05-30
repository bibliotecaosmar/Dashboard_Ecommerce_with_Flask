from app import db

class Usuario(db.Model):
    __tablename__ = "usuarios"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome_usuario = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    senha = db.Column(db.String)
    nome = db.Column(db.String)

    def __init__(self, nome_usuario, email, senha, nome):
        self.nome_usuario = nome_usuario
        self.email = email
        self.senha = senha
        self.nome = nome

    def __repr__(self):
        return '<Usuario %r>' % self.nome_usuario

class Post(db.Model):
    __tablename__ = 'posts'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    conteudo = db.Column(db.text, nullable=False)
    id_usuario = db.Column(db.Integer, db.ForeignKey('usuarios.id'))

    usuario = db.relarionship('Usuario', foreign_keys=id_usuario)

    def __init__(self, conteudo, id_usuario):
        self.conteudo = conteudo
        self.id_usuario = id_usuario

    def __repr__(self):
        return '<Post %r>' % self.id
    