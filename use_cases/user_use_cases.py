from flask import request, jsonify
from entities.user import AuthUser, User, db
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
from datetime import datetime, timedelta
from flask import current_app

# Cadastro de usuário

def register_user(request, db):
    data = request.get_json()
    if not data or not data.get('username') or not data.get('password'):
        return jsonify({'message': 'Username e password são obrigatórios'}), 400

    if AuthUser.query.filter_by(username=data['username']).first():
        return jsonify({'message': 'Este username já existe'}), 409

    new_auth_user = AuthUser(username=data['username'])
    new_auth_user.set_password(data['password'])
    new_user_profile = User(auth_user=new_auth_user)
    db.session.add(new_auth_user)
    db.session.add(new_user_profile)
    db.session.commit()
    return jsonify({'message': 'Novo usuário criado com sucesso!'}), 201

# Login de usuário

def login_user(request):
    auth = request.authorization
    if not auth or not auth.username or not auth.password:
        return jsonify({'message': 'Não foi possível verificar'}), 401, {'WWW-Authenticate': 'Basic realm="Login obrigatório!"'}
    auth_user = AuthUser.query.filter_by(username=auth.username).first()
    if not auth_user or not auth_user.check_password(auth.password):
        return jsonify({'message': 'Username ou password incorretos'}), 401, {'WWW-Authenticate': 'Basic realm="Login obrigatório!"'}
    token = jwt.encode({
        'auth_user_id': auth_user.id,
        'exp': datetime.utcnow() + timedelta(hours=8)
    }, current_app.config['SECRET_KEY'], algorithm="HS256")
    return jsonify({'token': token})

# Obter o próprio perfil

def get_own_profile(current_user):
    profile = User.query.filter_by(auth_user_id=current_user.id).first()
    if not profile:
        return jsonify({'message': 'Perfil não encontrado'}), 404
    return jsonify(profile.to_dict())

# Atualizar o próprio perfil

def update_own_profile(current_user, request):
    profile = User.query.filter_by(auth_user_id=current_user.id).first()
    if not profile:
        return jsonify({'message': 'Perfil não encontrado'}), 404
    data = request.get_json()
    profile.bloodType = data.get('bloodType', profile.bloodType)
    profile.motorcycle = data.get('motorcycle', profile.motorcycle)
    profile.partner = data.get('partner', profile.partner)
    profile.godfather = data.get('godfather', profile.godfather)
    profile.emergencyContact = data.get('emergencyContact', profile.emergencyContact)
    profile.emergencyPhone = data.get('emergencyPhone', profile.emergencyPhone)
    profile.formerMC = data.get('formerMC', profile.formerMC)
    profile.address = data.get('address', profile.address)
    profile.workAddress = data.get('workAddress', profile.workAddress)
    profile.actualFunction = data.get('actualFunction', profile.actualFunction)
    db.session.commit()
    return jsonify({'message': 'Perfil atualizado com sucesso!', 'profile': profile.to_dict()})

# Listar todos os usuários

def get_all_users(current_user):
    users = User.query.all()
    return jsonify([user.to_dict() for user in users])

# Obter usuário por ID

def get_user_by_id(current_user, user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({'message': 'Usuário não encontrado'}), 404
    return jsonify(user.to_dict())

# Deletar usuário

def delete_user(current_user, auth_id):
    user_to_delete = AuthUser.query.get(auth_id)
    if not user_to_delete:
        return jsonify({'message': 'Usuário não encontrado'}), 404
    db.session.delete(user_to_delete)
    db.session.commit()
    return jsonify({'message': 'Usuário deletado com sucesso'})
