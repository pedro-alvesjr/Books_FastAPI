from fastapi import FastAPI, Body
from pydantic import BaseModel

app = FastAPI()


class Book:
    id: int
    title: str
    author: str
    description: str
    rating: int

    def __init__(self, id, title, author, description, rating):
        self.id = id
        self.title = title
        self.author = author
        self.description = description
        self.rating = rating


class BookRequest(BaseModel):
    id: int
    title: str
    author: str
    description: str
    rating: int


BOOKS = [
    Book(1, 'Bible', 'The Holy Spirit', 'Best book of all time', 5),
    Book(2, 'Star Wars', 'Author Two', 'Book description', 3),
    Book(3, 'Rome, Sweet Home', 'Scott Hahn', 'Book description', 5),
    Book(4, 'Praying', 'Author Two', 'Book description', 4),
    Book(5, 'Path', 'Josémaria Escrivá', 'Book description', 5)
]


@app.get('/books/')
def show_all_books():
    return BOOKS


@app.post('/create_book')
def create_book(book_request: BookRequest):
    new_book = Book(**book_request.dict())
    BOOKS.append(book_request)