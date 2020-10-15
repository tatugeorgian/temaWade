from http.server import HTTPServer, SimpleHTTPRequestHandler
import re
import mysql.connector
import json

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="admin",
    database='books'
)


def create_book(row):
    if 'isbn' in row.keys():
        return Book(str(row['title']), str(row['author']), float(row['price']), row['isbn'])
    return Book(str(row['title']), str(row['author']), float(row['price']))


class Book:
    def __init__(self, title, author, price, isbn=None):
        self.title = title
        self.author = author
        self.isbn = isbn
        self.price = price


class GetHandler(SimpleHTTPRequestHandler):

    def do_GET(self):
        if self.path == '/books':
            mycursor = mydb.cursor(dictionary=True)
            mycursor.execute("SELECT * FROM books")
            rows = mycursor.fetchall()
            result = json.dumps(list(map(lambda row: create_book(row).__dict__, rows)))
            self._send_resp(200, result, {"Content-type": "application/json"})

        if re.search("/books/.+", self.path):
            mycursor = mydb.cursor(dictionary=True)
            sql = "SELECT * FROM books WHERE isbn = %s"
            mycursor.execute(sql, (self.path.split('/')[-1],))
            row = mycursor.fetchone()
            if (row):
                result = json.dumps(create_book(row).__dict__)
                self._send_resp(200, result, {"Content-type": "application/json"})
            else:
                self._send_empty_resp(404, {})
                return

            print('getting book with id ' + self.path.split('/')[-1])

    def do_POST(self):
        if self.path == '/books':
            print('creating book')
            body = self.rfile.read(int(self.headers['Content-Length']))
            book = create_book(json.loads(body))
            mycursor = mydb.cursor()

            sql = "INSERT INTO books (title, author, price, isbn) VALUES (%s, %s, %s, %s)"
            val = (book.title, book.author, book.price, book.isbn)
            mycursor.execute(sql, val)
            mydb.commit()
            result = json.dumps(book.__dict__)
            self._send_resp(201, result, {'Content-type': 'application/json'})

    def do_DELETE(self):
        if self.path == '/books':
            sql = "DELETE FROM books"
            mycursor = mydb.cursor()
            mycursor.execute(sql)
            mydb.commit()
            self._send_empty_resp(204, {'Content-type': 'application/json'})
            return
        if re.search("/books/.+", self.path):
            sql = "DELETE FROM books where isbn = %s"
            mycursor = mydb.cursor()
            mycursor.execute(sql, (self.path.split('/')[-1],))
            mydb.commit()
            print('deleting book with id ' + self.path.split('/')[-1])
            self._send_empty_resp(204, {'Content-type': 'application/json'})
            return

    def do_PUT(self):
        if re.search("/books/.+", self.path):
            body = self.rfile.read(int(self.headers['Content-Length']))
            book = create_book(json.loads(body))
            mycursor = mydb.cursor()
            sql = "UPDATE books SET title = %s, author = %s, price = %s WHERE isbn = %s"
            val = (book.title, book.author, book.price, self.path.split('/')[-1])
            mycursor.execute(sql, val)
            mydb.commit()
            print('replacing book with id ' + self.path.split('/')[-1])
            result = json.dumps(book.__dict__)
            self._send_resp(200, result, {'Content-type': 'application/json'})

    def _send_resp(self, code, response, headers):
        self.send_response(code)
        for header_name in headers:
            self.send_header(header_name, headers[header_name])
        self.end_headers()
        self.wfile.write(response.encode())

    def _send_empty_resp(self, code, headers):
        self.send_response(code)
        for header_name in headers:
            self.send_header(header_name, headers[header_name])
        self.end_headers()


if __name__ == '__main__':
    Handler = GetHandler
    try:
        httpd = HTTPServer(("localhost", 8080), Handler)
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("exiting")
        exit()
