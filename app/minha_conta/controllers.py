from flask import Blueprint, request, render_template, flash, g, session, redirect, url_for, Markup
from flask_login import current_user, login_required
from app import db

from app.minha_conta.models import Pedido, Pagamento

minha_conta = Blueprint('minha_conta', __name__)

@minha_conta.route('/minha-conta')
@login_required
def minha_conta_info():
    return 'minha conta'

@minha_conta.route('/minha-conta/meus-pedidos')
@login_required
def meus_pedidos():
    # pagamento = Pagamento('boleto')
    # db.session.add(pagamento)
    # db.session.commit()
    
    # pagamento = Pagamento.query.filter_by(descricao='boleto').first()
    # db.session.delete(pagamento)
    # db.session.commit()

    # pedido = Pedido(20.35, 'aguardando pagamento', 1, 1)
    # db.session.add(pedido)
    # db.session.commit()

    # CONSULTA DE TODOS OS PEDIDOS DE UM CLIENTE
    pedidos = Pedido.query.filter_by(cliente_id=current_user.id).all()
    pagamentos = []
    for pedido in pedidos:
        pagamento = Pagamento.query.filter_by(id=pedido.pagamento_id).first()
        pagamentos.append(pagamento.descricao)
    pedidos = zip(pedidos, pagamentos)
    return render_template('/minha_conta/meus_pedidos.html', pedidos=pedidos)