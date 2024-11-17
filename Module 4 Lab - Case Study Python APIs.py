from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///books.db'
db = SQLAlchemy(app)

class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    book_name = db.Column(db.String(100))
    author = db.Column(db.String(100))
    publisher = db.Column(db.String(100))

db.create_all()

@app.route('/books', methods=['GET'])
def get_books():
    books = Book.query.all()
    return jsonify([{
        "id": book.id,
        "book_name": book.book_name,
        "author": book.author,
        "publisher": book.publisher
    } for book in books])

@app.route('/books/<int:id>', methods=['GET'])
def get_book(id):
    book = Book.query.get(id)
    if not book:
        return jsonify({"error": "Double check the book you entered, is that english? Or even a name of a book?"}), 404
    return jsonify({
        "id": book.id,
        "book_name": book.book_name,
        "author": book.author,
        "publisher": book.publisher
    })

@app.route('/books', methods=['POST'])
def create_book():
    data = request.json
    book = Book(
        book_name=data.get('book_name'),
        author=data.get('author'),
        publisher=data.get('publisher')
    )
    db.session.add(book)
    db.session.commit()
    return jsonify({
        "id": book.id,
        "book_name": book.book_name,
        "author": book.author,
        "publisher": book.publisher
    }), 201

@app.route('/books/<int:id>', methods=['PUT'])
def update_book(id):
    book = Book.query.get(id)
    if not book:
        return jsonify({"error": "Double check the book you entered, is that english? Or even a name of a book?"}), 404
    data = request.json
    book.book_name = data.get('book_name', book.book_name)
    book.author = data.get('author', book.author)
    book.publisher = data.get('publisher', book.publisher)
    db.session.commit()
    return jsonify({
        "id": book.id,
        "book_name": book.book_name,
        "author": book.author,
        "publisher": book.publisher
    })

@app.route('/books/<int:id>', methods=['DELETE'])
def delete_book(id):
    book = Book.query.get(id)
    if not book:
        return jsonify({"error": "Double check the book you entered, is that english? Or even a name of a book?"}), 404
    db.session.delete(book)
    db.session.commit()
    return jsonify({"message": "Booketh Vanisheth"})

if __name__ == '__main__':
    app.run(debug=True)
