from flask import Blueprint, request, jsonify
from entities.user import db
from adapters.auth import token_required
from use_cases import user_use_cases

routes = Blueprint('routes', __name__)

# Rota de Registro
@routes.route('/register', methods=['POST'])
def register():
    """
    Cadastro de novo usuário
    ---
    tags:
      - Usuário
    requestBody:
      required: true
      content:
        application/json:
          schema:
            type: object
            properties:
              username:
                type: string
              password:
                type: string
            required:
              - username
              - password
    responses:
      201:
        description: Usuário criado
      400:
        description: Dados inválidos
      409:
        description: Username já existe
    """
    return user_use_cases.register_user(request, db)

# Rota de Login
@routes.route('/login', methods=['POST'])
def login():
    """
    Login do usuário
    ---
    tags:
      - Usuário
    security:
      - basicAuth: []
    responses:
      200:
        description: Token JWT retornado
      401:
        description: Falha na autenticação
    """
    return user_use_cases.login_user(request)

# Rotas protegidas
@routes.route('/upload_image', methods=['POST'])
@token_required
def upload_image(current_user):
    """
    Upload de imagem do usuário (500x500)
    ---
    tags:
      - Usuário
    consumes:
      - multipart/form-data
    parameters:
      - in: formData
        name: image
        type: file
        required: true
        description: Imagem do usuário
    responses:
      200:
        description: Upload realizado com sucesso
      400:
        description: Erro no upload
      401:
        description: Não autorizado
    """
    if 'image' not in request.files:
        return {'error': 'Nenhum arquivo enviado'}, 400
    file = request.files['image']
    if file.filename == '':
        return {'error': 'Nome de arquivo vazio'}, 400
    try:
        img = Image.open(file)
        img = img.convert('RGB')
        img = img.resize((500, 500))
        upload_folder = os.path.join(current_app.root_path, 'static', 'profilePics')
        os.makedirs(upload_folder, exist_ok=True)
        filename = f'user_{current_user.id}.jpg'
        file_path = os.path.join(upload_folder, filename)
        img.save(file_path, optimize=True, quality=85)
        # Associa caminho ao usuário
        current_user.image_path = f'static/profilePics/{filename}'
        db.session.commit()
        return {'message': 'Imagem enviada e otimizada com sucesso'}, 200
    except Exception as e:
        return {'error': str(e)}, 400

@routes.route('/profile', methods=['GET'])
@token_required
def get_own_profile(current_user):
    return user_use_cases.get_own_profile(current_user)

@routes.route('/profile', methods=['PUT'])
@token_required
def update_own_profile(current_user):
    return user_use_cases.update_own_profile(current_user, request)

@routes.route('/users', methods=['GET'])
@token_required
def get_all_users(current_user):
    return user_use_cases.get_all_users(current_user)

@routes.route('/users/<int:user_id>', methods=['GET'])
@token_required
def get_user_by_id(current_user, user_id):
    return user_use_cases.get_user_by_id(current_user, user_id)

@routes.route('/users/<int:auth_id>', methods=['DELETE'])
@token_required
def delete_user(current_user, auth_id):
    return user_use_cases.delete_user(current_user, auth_id)
