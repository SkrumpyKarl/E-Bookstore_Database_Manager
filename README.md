E-Bookstore Database
This is a Python program developed in Visual Studio Code (VSC) that uses the SQLite extension to manage a database of books. The program is written in Python 3.11, and the SQLite extension is used to retrieve and display databases and tables in the SQLite Explorer output window.

The program is configured to use a database called "ebookstore_db.db" that includes a table named "books". If the database does not exist, the program will create it and save it in the same directory as the program file. A confirmation message will be displayed indicating the successful creation of the database.

## Requirements
The following modules are required to run the program:

- sqlite3
- pandas

## Installation
To install the required modules, run the following commands in a terminal:

## Copy code
- pip install sqlite3
- pip install pandas

## Usage
To run the program, open the ebookstore.py file in VSC and run it in a Python environment. The program will create a database named ebookstore_db.db in the same directory as the program file, if it does not exist. The database will include a table named books.

The program includes the following functions:

- add_book(): adds a new book to the database
- view_book(): displays information about a specific book
- view_all_books(): displays information about all books in the database
- search_book(): searches for a book in the database based on title, author, or ISBN
- delete_book(): deletes a book from the database based on its ISBN

Note that the program is currently configured to work with a database named 'ebookstore_db.db'. If you wish to use a different database, you will need to modify the code accordingly.
