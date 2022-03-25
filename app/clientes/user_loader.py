from app import lm
from app.clientes.models import Cliente


@lm.user_loader
def load_user(user_id):
    return Cliente.query.get(user_id)