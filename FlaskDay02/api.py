from flask_smorest import Blueprint, abort
from schemas import BookSchema
from flask.views import MethodView

book_blp = Blueprint('books', 'books', url_prefix='/books', description='Operations on books')

# 데이터 저장소
books = []

# 엔드포인트 구현...
@book_blp.route('/')
class Booklist(MethodView):
    @book_blp.response(200, BookSchema(many=True))
    def get(self):
        return books
    
    @book_blp.arguments(BookSchema)
    @book_blp.response(201, BookSchema)
    def post(self, new_data):
        new_data['id'] = len(books) + 1
        books.append(new_data)
        return new_data
    
@book_blp.route('/<int:book_id>')
class Book(MethodView):
    @book_blp.response(200, BookSchema)
    def get(self, book_id):
        book = next((book for book in books if book ['id'] == book_id), None)
        if book is None:
            abort(404, message= "book not found.")
        return book
    
    @book_blp.arguments(BookSchema)
    @book_blp.response(200, BookSchema)
    def put(self, new_data, book_id):
        book = next((book for book in books if book ['id']== book_id), None)
        if book is None:
            abort(404, message = 'Book not found.')
        book.update(new_data)
        return book
    
    @book_blp.response(204)
    def delete(self, book_id):
        global books
        book = next((book for book in books if book['id'] == book_id), None)
        if book is None:
            abort(404, message = "Book not found.")
            books = [book for book in books if book['id'] != book_id]
            return ''