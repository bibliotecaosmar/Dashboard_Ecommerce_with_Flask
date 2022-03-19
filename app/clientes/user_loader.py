from app import lm
from app.clientes.models import Cliente

# @lm.user_loader
# def load_user(id):
#     return Cliente.query.filter_by(id=id).first()

@lm.user_loader
def load_user(user_id):
    return Cliente.query.get(int(user_id))