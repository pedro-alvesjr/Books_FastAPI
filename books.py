from typing import Optional
from fastapi import FastAPI, Path, Query, HTTPException
from pydantic import BaseModel, Field

app = FastAPI()


class Book:
    id: int
    title: str
    author: str
    description: str
    rating: int
    published_date: int

    def __init__(self, id, title, author, description, rating, published_date):
        self.id = id
        self.title = title
        self.author = author
        self.description = description
        self.rating = rating
        self.published_date = published_date


class BookRequest(BaseModel):
    id: Optional[int] = Field(description='ID is not needed on create', default=None)
    title: str = Field(min_length=3)
    author: str = Field(min_length=3)
    description: str = Field(min_length=1, max_length=100)
    rating: int = Field(gt=-1, lt=6)
    published_date: int = Field(gt=0, lt=2100)

    model_config = {
        "json_schema_extra": {
            "example": {
                "title": "codingwithroby",
                "author": "Cody",
                "description": "A new description of a book",
                "rating": 5,
                "published_date": 2012
            }
        }
    }


BOOKS = [
    Book(1, 'Bible', 'The Holy Spirit', 'Best book of all time', 5, 1932),
    Book(2, 'Star Wars', 'Author Two', 'Book description', 3, 1967),
    Book(3, 'Rome, Sweet Home', 'Scott Hahn', 'Book description', 5, 2005),
    Book(4, 'Praying', 'Author Two', 'Book description', 4, 2000),
    Book(5, 'Path', 'Josémaria Escrivá', 'Book description', 5, 2019)
]


@app.get('/books')
def show_all_books():
    return BOOKS


@app.get('/books/{book_id}')
def find_book_by_ID(book_id: int = Path(gt=0)):
    for book in BOOKS:
        if book.id == book_id:
            return book
    raise HTTPException(status_code=404, detail='ID not found.')


@app.get('/books/')
def filter_books_by_rating(book_rating: int = Query(gt=0, lt=6)):
    books_to_return = []
    for book in BOOKS:
        if book.rating == book_rating:
            books_to_return.append(book)
    return books_to_return


@app.get('/books/publish/')
def filter_books_by_published_date(published_date: int = Query(gt=0, lt=2100)):
    books_to_return = []
    for book in BOOKS:
        if book.published_date == published_date:
            books_to_return.append(book)
    return books_to_return


@app.post('/create_book')
def create_book(book_request: BookRequest):
    new_book = Book(**book_request.model_dump())
    BOOKS.append(find_book_id(new_book))


def find_book_id(book: Book):
    if len(BOOKS) > 0:
        book.id = BOOKS[-1].id + 1
    else:
        book.id = 1
    return book


@app.put('/books/update_book')
def update_book(book: BookRequest):
    book_changed = False
    for i in range(len(BOOKS)):
        if BOOKS[i].id == book.id:
            BOOKS[i] = book
            book_changed = True
    if not book_changed:
        raise HTTPException(status_code=404, detail='Item not found.')


@app.delete('/books/{book_id}')
def delete_book(book_id: int = Path(gt=0)):
    book_deleted = False
    for i in range(len(BOOKS)):
        if BOOKS[i].id == book_id:
            BOOKS.pop(i)
            book_deleted = True
            break
    if not book_deleted:
        raise HTTPException(status_code=404, detail='Item not found')
