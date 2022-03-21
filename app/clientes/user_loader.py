from app import lm
from app.clientes.models import Cliente


@lm.user_loader
def load_user(id):
    return Cliente.query.get(id)