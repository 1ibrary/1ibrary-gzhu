from yitu.models.book import Book
from yitu.services.gzhu.book_details import BookDetails
import json


def change_detail():
    books = Book.query.all()
    book_details = BookDetails()
    for book in books:
        temp = book_details.get_details(book.book_key)
        data = json.dumps(temp["data"])
        book.detail_data = data
