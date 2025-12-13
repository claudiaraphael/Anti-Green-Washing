from flask import Blueprint, jsonify, request
from extensions import db
from model.user import User
from schemas.user_schemas import UserInputSchema, UserResponseSchema

# Criar blueprint padrão do Flask
users_bp = Blueprint('users', __name__)


@users_bp.route('/users', methods=['POST'])
def create_user():
    """
    Cria um novo usuário no banco de dados.
    """
    try:
        data = request.get_json()

        # Validar com Pydantic
        validated_data = UserInputSchema(**data)

        # Criar instância do usuário
        new_user = User(
            username=validated_data.username,
            email=validated_data.email
        )

        # Adicionar e commitar
        db.session.add(new_user)
        db.session.commit()

        # Retornar resposta
        return jsonify({
            "message": "Usuário criado com sucesso",
            "user": {
                "id": new_user.id,
                "username": new_user.username,
                "email": new_user.email,
                "date_created": new_user.date_created.isoformat() if new_user.date_created else None
            }
        }), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 400


@users_bp.route('/users', methods=['GET'])
def get_all_users():
    """
    Lista todos os usuários.
    """
    users = User.query.all()
    return jsonify({
        "users": [
            {
                "id": u.id,
                "username": u.username,
                "email": u.email,
                "date_created": u.date_created.isoformat() if u.date_created else None
            }
            for u in users
        ]
    }), 200


@users_bp.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    """
    Busca um usuário pelo ID.
    """
    user = User.query.get_or_404(user_id)
    return jsonify({
        "id": user.id,
        "username": user.username,
        "email": user.email,
        "date_created": user.date_created.isoformat() if user.date_created else None
    }), 200


@users_bp.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    """
    Deleta um usuário pelo ID.
    """
    user = User.query.get_or_404(user_id)

    try:
        db.session.delete(user)
        db.session.commit()
        return jsonify({"message": "Usuário deletado com sucesso"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 400
