from flask import Flask
from adapters.routes import routes
from entities.user import db
from flask import Flask
from flasgger import Swagger

app = Flask(__name__, static_folder='uploads', static_url_path='/static')
app.config['SECRET_KEY'] = 'uma-chave-super-secreta-e-dificil-de-adivinhar'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///moto_clube.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

swagger = Swagger(app)
db.init_app(app)

# Registra o blueprint das rotas
app.register_blueprint(routes, url_prefix='/api/v1')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, port=5000)