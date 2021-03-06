import sys
sys.path.append('/home/bazilio/GT-Covid19-Atendimento/app')

# Importações básicas
from flask import Flask
from flask_cors import CORS
from flask_login import LoginManager
from models.models import AdmSaude
from controller.database import Database
from controller.pdfInclusao import incluiPdf
import logging

# Importação de rotas 
from blueprints.about import about
from blueprints.login import login
from blueprints.admin import menuAdmin
from blueprints.atendimento import atendimento
from blueprints.menuAtendente import menuAtendente
from blueprints.registrarUsuario import registrarUsuario
from blueprints.registrarPaciente import registrarPaciente
from blueprints.primeiroAtendimento import primeiroAtendimento
from blueprints.historico import historico

if incluiPdf():
    from blueprints.pdfAgendamento import pdfAgendamento

app = Flask(__name__)

# Configura log para ser gerado em arquivo e no stdout (saida padrao)
log_format = '%(asctime)s  %(levelname)s %(filename)s: %(message)s'
logging.basicConfig(filename='telemonitoramento.log', format=log_format, level=logging.DEBUG)
logging.getLogger().addHandler(logging.StreamHandler(sys.stdout))

app.config.from_pyfile('config.py')

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "Login.loginMetodo"

@login_manager.user_loader
def getUsuario(usuario_id):
    db = Database()

    return db.selectIf(AdmSaude, id=usuario_id)

app.register_blueprint(about, url_prefix='/')
app.register_blueprint(login, url_prefix='/')
app.register_blueprint(menuAdmin, url_prefix='/')
app.register_blueprint(atendimento, url_prefix='/')
app.register_blueprint(menuAtendente, url_prefix='/')
app.register_blueprint(registrarUsuario, url_prefix='/')
app.register_blueprint(registrarPaciente, url_prefix='/')
app.register_blueprint(primeiroAtendimento, url_prefix='/')
app.register_blueprint(historico, url_prefix='/')

if incluiPdf():
    app.register_blueprint(pdfAgendamento, url_prefix='/')

CORS(app)

if __name__ == '__main__':
    if 'dev' in sys.argv: #Em desenvolvimento, rodar em https para fazer funcionar o serviceWorker
        app.run(host='0.0.0.0', port=5000, debug=True, ssl_context='adhoc')
    else:
        app.run(host='0.0.0.0', port=5000, debug=True)
