"""
BLUEPRINTS

é uma forma de separar a aplicação em modulos para separar
a lógica de diferentes recursos em arquivos e URLs diferentes
Mantém o código escalavel.

"""
from flask import Flask, request, jsonify, Blueprint
from extensions import db
from app import app

from schemas import *

from model.user import User

@app.route('/user', methods=["POST"])
def new_user(form: UserInputSchema):
    new_user = User(username=form.username, email=form.email)
    
    try:
        db.session.add(new_user)
        db.session.commit()

# form é uma propriedade padrao do flask para receber os dados do formulario do frontend


 # ROUTES

    @app.route('/books', methods=['POST'])
        def add_book():
        data = request.get_json()
        newBook = Book(title=data['title'], author=data['author'], description=data['description'])
        db.session.add(newBook)
        db.session.commit()
        return jsonify({'message': 'livro inserido com sucesso'}), 201

    @app.route('/books', methods=['GET'])
    def get_all():
    books = Book.query.all()
    return jsonify([book.as_dict() for book in books])

    @app.route('/books/<uuid:book_id>', methods=['GET'])
    def get_book(book_id):
    book = Book.query.get_or_404(book_id)
    return jsonify(book.as_dict())

    @app.route('/books/<uuid:book_id>', methods=['PATCH'])
    def update_book(book_id):
    book = Book.query.get_or_404(book_id)
    data = request.get_json()

    for key, value in data.items():
        setattr(book, key, value)
    
    db.session.commit()
    return jsonify({'message': 'Livro atualizado com sucesso'})

    @app.route('/books/<uuid:book_id>', methods=['DELETE'])
    def delete(book_id):
    book = Book.query.get_or_404(book_id)
    db.session.delete(book)
    db.session.commit()
    return jsonify({'message': 'Livro removido do com sucesso'})
