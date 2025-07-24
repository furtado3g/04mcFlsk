import jwt
from functools import wraps
from flask import request, jsonify, current_app
from entities.user import AuthUser

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if 'Authorization' in request.headers:
            try:
                token = request.headers['Authorization'].split(" ")[1]
            except IndexError:
                return jsonify({'message': 'O Bearer token não está no formato correto'}), 401
        if not token:
            return jsonify({'message': 'O token está ausente!'}), 401
        try:
            data = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=["HS256"])
            current_user = AuthUser.query.get(data['auth_user_id'])
            if not current_user:
                return jsonify({'message': 'Usuário do token não encontrado'}), 401
        except jwt.ExpiredSignatureError:
            return jsonify({'message': 'O token expirou!'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'message': 'Token inválido!'}), 401
        return f(current_user, *args, **kwargs)
    return decorated
