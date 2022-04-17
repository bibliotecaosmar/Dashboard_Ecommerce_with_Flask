from flask import Blueprint, request, render_template, flash, g, session, redirect, url_for, Markup
from flask_login import current_user, login_required
from app import db

from app.conta.models import Pedido, Pagamento

conta = Blueprint('conta', __name__)

@conta.route('/pedidos')
@login_required
def pedidos():
    # pagamento = Pagamento('boleto')
    # db.session.add(pagamento)
    # db.session.commit()
    
    # pagamento = Pagamento.query.filter_by(descricao='boleto').first()
    # db.session.delete(pagamento)
    # db.session.commit()

    # pedido = Pedido(20.35, 'aguardando pagamento', 1, 1)
    # db.session.add(pedido)
    # db.session.commit()
    print(current_user.id)
    return 'pedidos'