from flask import Flask, render_template, request, session, redirect
from flask_mysqldb import MySQL
import MySQLdb.cursors
import bcrypt
import mysql.connector

# cnx = mysql.connector.connect(user='root', password='my-secret-pw',
#                               host='127.0.0.1', database='my-database')
# cursor = cnx.cursor()

# query = "SELECT * FROM my_table"
# cursor.execute(query)

# for row in cursor:
#     print(row)

# cursor.close()
# cnx.close()

app = Flask(__name__)
app.secret_key = 'secret_key'

class LibraryWorker:

    def __init__(self, username, password):
        self.username = username
        self.password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

def login(self):
    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cur.execute('SELECT * FROM workers WHERE username = %s', (self.username,))
    worker = cur.fetchone()
    cur.close()
    if worker and bcrypt.checkpw(self.password.encode('utf-8'), worker['password'].encode('utf-8')):
        session['loggedin'] = True
        session['id'] = worker['id']
        session['username'] = worker['username']
        return True
    else:
        return False

def checkout(self, book):
    if book.status == 'available':
        book.status = 'checked out'
        book.patron_id = session['id']
        return True
    else:
        return False

def checkin(self, book):
    if book.status == 'checked out':
        book.status = 'available'
        book.patron_id = None
        return True
    else:
        return False

class LibraryPatron:
    def __init__(self, username, password):
        self.username = username
        self.password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    def login(self):
        cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cur.execute('SELECT * FROM patrons WHERE username = %s', (self.username,))
        patron = cur.fetchone()
        cur.close()
        if patron and bcrypt.checkpw(self.password.encode('utf-8'), patron['password'].encode('utf-8')):
            session['loggedin'] = True
            session['id'] = patron['id']
            session['username'] = patron['username']
            return True
        else:
            return False

    def search(self, keyword):
        cur = mysql.connection.cursor()
        cur.execute('SELECT * FROM books WHERE title LIKE %s OR author LIKE %s', ('%' + keyword + '%', '%' + keyword + '%'))
        data = cur.fetchall()
        cur.close()
        return data

    def hold(self, book):
        if book.status == 'available':
            book.status = 'on hold'
            return True
        else:
            return False

class Book:
    def __init__(self, title, author):
        self.title = title
        self.author = author
        self.status = 'available'
        self.patron_id = None

# Configure MySQL
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'cs232'
app.config['MYSQL_PASSWORD'] = 'cs232-pw'
app.config['MYSQL_DB'] = 'library'
mysql = MySQL(app)

# Define routes and corresponding view functions
@app.route('/')
def index():
    if 'loggedin' in session:
        cur = mysql.connection.cursor()
        cur.execute('SELECT * FROM books')
        data = cur.fetchall()
        cur.close()
        return render_template('index.html', data=data)
    return redirect('/login')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if 'worker' in request.form:
            user = LibraryWorker(username, password)
        else:
            user = LibraryPatron(username, password)
        if user.login():
            return redirect('/')
        else:
            return 'Invalid username or password'
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('username', None)
    return redirect('/login')

@app.route('/search', methods=['GET', 'POST'])
def search():
    if 'loggedin' in session:
        if request.method == 'POST':
            keyword = request.form['keyword']
            user = LibraryPatron(session['username'], '')
            data = user.search(keyword)
            return render_template('search.html', data=data)
        return render_template('search.html')
    return redirect('/login')

@app.route('/checkout/<int:id>')
def checkout(id):
    if 'loggedin' in session:
        cur = mysql.connection.cursor()
        cur.execute('SELECT * FROM books WHERE id = %s', (id,))
        book_data = cur.fetchone()
        book = Book(book_data['title'], book_data['author'])
    user = LibraryWorker(session['username'], '')
    if user.checkout(book):
        cur.execute('UPDATE books SET status = %s, patron_id = %s WHERE id = %s', ('checked out', session['id'], id))
        mysql.connection.commit()
        cur.close()
        return 'Book checked out successfully'
    else:
        cur.close()
        return 'Book not available'
    return redirect('/login')

@app.route('/checkin/<int:id>')
def checkin(id):
    if 'loggedin' in session:
        cur = mysql.connection.cursor()
        cur.execute('SELECT * FROM books WHERE id = %s', (id,))
        book_data = cur.fetchone()
        book = Book(book_data['title'], book_data['author'])
        user = LibraryWorker(session['username'], '')
        if user.checkin(book):
            cur.execute('UPDATE books SET status = %s, patron_id = NULL WHERE id = %s', ('available', id))
            mysql.connection.commit()
            cur.close()
            return 'Book checked in successfully'
        else:
            cur.close()
        return 'Book already checked in'
    return redirect('/login')

@app.route('/hold/<int:id>')
def hold(id):
    if 'loggedin' in session:
        cur = mysql.connection.cursor()
        cur.execute('SELECT * FROM books WHERE id = %s', (id,))
        book_data = cur.fetchone()
        book = Book(book_data['title'], book_data['author'])
        user = LibraryPatron(session['username'], '')
        if user.hold(book):
            cur.execute('UPDATE books SET status = %s WHERE id = %s', ('on hold', id))
            mysql.connection.commit()
            cur.close()
            return 'Hold placed successfully'
        else:
            cur.close()
            return 'Book not available'
    return redirect('/login')

# Run the app
if __name__ == '__main__':
    app.run(debug=True)