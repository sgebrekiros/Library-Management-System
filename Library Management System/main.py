from flask import Flask, request, render_template,redirect,url_for
import pymysql


app = Flask(__name__)



@app.route('/')
def index():
    return render_template("login.html")
database = {'tigi': 'pass', 
            'bitu':'secret', 
            'user':'user'}

@app.route('/login', methods = ['GET', 'POST'])

def login():
    name = request.form['username']
    pwd = request.form['password']
    if name not in database:
        return redirect(url_for('index', info = 'Invalid User'))

    else:
        if database[name]!=pwd:
            return redirect(url_for('index', info = 'Invalid password'))
        else:
            return redirect(url_for('Home'))

# # Routing
@app.route('/Home')
def Home():
    return render_template('index1.html')

def db_connection():
    conn = pymysql.connect(
        host='localhost',
        user='root',
        password='cs232-pw',
        database='library'
        )
    return conn

def create_tables():
    conn = db_connection()
    cursor = conn.cursor()
    book_table = """
    CREATE TABLE IF NOT EXISTS book (
        id INT AUTO_INCREMENT PRIMARY KEY,
        title VARCHAR(80) UNIQUE NOT NULL,
        author VARCHAR(120) NOT NULL)
        """
    worker_table = """
    CREATE TABLE IF NOT EXISTS worker (
        id INT AUTO_INCREMENT PRIMARY KEY,
        username VARCHAR(80) UNIQUE NOT NULL,
        password VARCHAR(120) NOT NULL)
        """
    patron_table = """
    CREATE TABLE IF NOT EXISTS patron (
        id INT AUTO_INCREMENT PRIMARY KEY,
        username VARCHAR(80) UNIQUE NOT NULL,
        password VARCHAR(120) NOT NULL
        )
        """
    cursor.execute(worker_table)
    cursor.execute(patron_table)
    cursor.execute(book_table)
    conn.commit()
    cursor.close()
    conn.close()


create_tables()




@app.route('/add_patron', methods=['POST'])
def add_patron():
    title = request.form['title']
    author= request.form['author']
    conn = db_connection()
    cursor = conn.cursor()
    book_query = "SELECT * FROM book WHERE title = %s"
    cursor.execute(book_query, (title,))
    workera = cursor.fetchone()


    if workera:
        return 'THE BOOK ALREADY EXISTS'

    else:
        query = "INSERT INTO book (title, author) VALUES (%s, %s)"
        cursor.execute(query, (title, author))
        conn.commit()
        cursor.close()
        conn.close()
        return 'BOOK CHECKED IN SUCCESFULLY'
    # username = request.form['username']
    # password = request.form['password']
    # conn = db_connection()
    # cursor = conn.cursor()
    # query = "INSERT INTO patron (username, password) VALUES (%s, %s)"
    # cursor.execute(query, (username, password))
    # conn.commit()
    # cursor.close()
    # conn.close()
    # return 'Patron added successfully'



@app.route('/search', methods=['GET', 'POST'])
def search():
    title = request.form.get('title')
    conn = db_connection()
    cursor = conn.cursor()
    
    worker_query = "SELECT * FROM book WHERE title = %s"
    cursor.execute(worker_query, (title,))
    worker = cursor.fetchone()
    
    # patron_query = "SELECT * FROM patron WHERE username = %s"
    # cursor.execute(patron_query, (title,))
    # patron = cursor.fetchone()
    
    cursor.close()
    conn.close()
    
    if worker:
        return 'Book is here.'
    # elif patron:
    #     return f"Patron with username {username} exists."
    else:
        return 'Does not exist'
    
@app.route('/delete', methods=['POST'])
def delete_user():
    title = request.form['title']
    # author= request.form['author']
    conn = db_connection()
    cursor = conn.cursor()
    
    worker_query = "DELETE FROM book WHERE title = %s"
    cursor.execute(worker_query, (title,))
    rows_affectedw = cursor.rowcount


    
    # # patron_query = "DELETE FROM book WHERE username = %s"
    # # cursor.execute(patron_query, (username,)    
    # rows_affectedp = cursor.rowcount
    conn.commit()
    cursor.close()
    conn.close()
    
    if  rows_affectedw <= 0:
        return f"No book with title {title}  was found."
    else:
        return f"Book with title {title} was successfully checked out."
    




# @app.route('/search', methods=['GET', 'POST'])
# def search():
#     conn = db_connection()
#     # cursor = conn.cursor()
#     username = request.form.get('username')
#     worker = conn.execute('SELECT * FROM worker WHERE username = ?', (username,)).fetchone()
#     patron = conn.execute('SELECT * FROM patron WHERE username = ?', (username,)).fetchone()
    
#     if worker:
#         return f"Worker with username {username} exists."
#     elif patron:
#         return f"Patron with username {username} exists."
#     else:
#         return f"No worker or patron with username {username}found."
#     # worker1 = "SELECT * FROM worker WHERE username = ?",(username,).fetchone()
#     # # Worker.query.filter_by(username=username).first()
#     # # patron1 = "SELECT * FROM patron WHERE username = ?",(username,).fetchone()
#     # # Patron.query.filter_by(username=username).first()
#     # cursor.execute(worker1, (username))
  
    
#     # if worker1:
#     #     return f"Worker with username {username} exists."
#     # # elif patron1:
#     # #     return f"Patron with username {username} exists."
#     # else:
#     #     return f"No worker or patron with username {username} found."
    
#     # username = request.form['username']
#     # password = request.form['password']
#     # conn = db_connection()
#     # cursor = conn.cursor()
#     # query = "INSERT INTO worker (username, password) VALUES (%s, %s)"
#     # cursor.execute(query, (username, password))
#     # conn.commit()
#     # cursor.close()
#     # conn.close()
#     # return 'Worker added successfully'







if __name__ == '__main__':
    app.run(debug=True)