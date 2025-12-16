from flask import Blueprint, jsonify, request
from extensions import db
from model.comment import Comment
from schemas.comment_schemas import CommentInputSchema, CommentResponseSchema

# Criar blueprint padrão do Flask
comment_bp = Blueprint('comment', __name__)

# create


@comment_bp.route('/comment', methods=['POST'])
def create_comment():
    """
    Cria um novo comentário no banco de dados.
    """
    try:
        data = request.get_json()

        # Validar com Pydantic
        validated_data = CommentInputSchema(**data)

        # Criar instância do comentário
        new_comment = Comment(
            author=validated_data.author_name or "Anônimo",
            text=validated_data.text,
            n_estrela=validated_data.n_estrela
        )
        new_comment.product_id = validated_data.product_id

        # Adicionar e commitar
        db.session.add(new_comment)
        db.session.commit()

        # Retornar resposta
        return jsonify({
            "message": "Comentário criado com sucesso",
            "comment": {
                "id": new_comment.id,
                "author": new_comment.author,
                "text": new_comment.text,
                "n_estrela": new_comment.n_estrela,
                "product_id": new_comment.product_id,
                "date_inserted": new_comment.date_inserted.isoformat() if new_comment.date_inserted else None
            }
        }), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 400

# read history


@comment_bp.route('/comment', methods=['GET'])
def get_all_comment():
    """
    Lista todos os comentários.
    """
    comment = Comment.query.all()
    return jsonify({
        "comment": [
            {
                "id": c.id,
                "author": c.author,
                "text": c.text,
                "n_estrela": c.n_estrela,
                "product_id": c.product_id,
                "date_inserted": c.date_inserted.isoformat() if c.date_inserted else None
            }
            for c in comment
        ]
    }), 200

# read


@comment_bp.route('/comment/<int:comment_id>', methods=['GET'])
def get_comment(comment_id):
    """
    Busca um comentário pelo ID.
    """
    comment = Comment.query.get_or_404(comment_id)
    return jsonify({
        "id": comment.id,
        "author": comment.author,
        "text": comment.text,
        "n_estrela": comment.n_estrela,
        "product_id": comment.product_id,
        "date_inserted": comment.date_inserted.isoformat() if comment.date_inserted else None
    }), 200

# read all comments from a product


@comment_bp.route('/comment/product/<int:product_id>', methods=['GET'])
def get_comment_by_product(product_id):
    """
    Lista todos os comentários de um produto específico.
    """
    comment = Comment.query.filter_by(product_id=product_id).all()
    return jsonify({
        "comment": [
            {
                "id": c.id,
                "author": c.author,
                "text": c.text,
                "n_estrela": c.n_estrela,
                "date_inserted": c.date_inserted.isoformat() if c.date_inserted else None
            }
            for c in comment
        ]
    }), 200

# delete


@comment_bp.route('/comment/<int:comment_id>', methods=['DELETE'])
def delete_comment(comment_id):
    """
    Deleta um comentário pelo ID.
    """
    comment = Comment.query.get_or_404(comment_id)

    try:
        db.session.delete(comment)
        db.session.commit()
        return jsonify({"message": "Comentário deletado com sucesso"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 400
