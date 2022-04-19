from app.database import db


class Pedido(db.Model):
    __tablename__ = 'pedidos'
    numero = db.Column(db.Integer, primary_key=True, autoincrement=True)
    data_criacao = db.Column(db.DateTime, default=db.func.current_timestamp())
    total = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(30), nullable=False)
    pagamento_id = db.Column(db.Integer, db.ForeignKey('pagamentos.id'), nullable=False)
    cliente_id = db.Column(db.Integer, db.ForeignKey('clientes.id'), nullable=False)
    
    def __init__(self, total, status, pagamento_id, cliente_id):
        self.total = total
        self.status = status
        self.pagamento_id = pagamento_id
        self.cliente_id = cliente_id
    
    def __repr__(self):
        return f'Pedido {self.numero}'

class Pagamento(db.Model):
    __tablename__ = 'pagamentos'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    descricao = db.Column(db.String(50), unique=True, nullable=False)

    #Relacionamentos
    pedidos = db.relationship('Pedido', backref='pagamentos', lazy=True)

    def __init__(self, descricao):
        self.descricao = descricao
    
    def __repr__(self):
        return f'Pagamento {self.descricao}'
