import os

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))

def main():



    # Prompt user to choose a book.
    book_isbn = (input("\nISBN: "))
    book_title = (input("\nTitle: "))
    book_author = (input("\nAuthor: "))
    book = db.execute("SELECT isbn, title, author, year FROM books WHERE isbn = :isbn OR title = :title OR author = :author",
                        {"isbn": book_isbn, "title": book_title, "author": book_author}).fetchone()


    # Make sure book is valid.
    if book is None:
        print("Error: No such book.")
        return

    # List book.
    books = db.execute("SELECT isbn, title, author, year FROM books WHERE isbn = :book_isbn OR title = :book_title OR author = :book_author",
                            {"book_isbn": book_isbn, "book_title": book_title, "book_author": book_author}).fetchall()





    print("\nBook:")
    for book in books:
        print(book.isbn)
        print(book.title)
        print(book.author)
        print(book.year)


    if len(books) == 0:
        print("No books.")

if __name__ == "__main__":
    main()
