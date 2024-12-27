from flask import Flask, render_template, request, redirect, url_for, send_file, jsonify
import pyodbc
import pandas as pd
import os
from config import conn_str

app = Flask(__name__)

# Home Page - List all books
@app.route('/')
def index():
    conn = pyodbc.connect(conn_str)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Inventory")
    books = cursor.fetchall()
    conn.close()
    return render_template('index.html', books=books)

# Add a new book
@app.route('/add', methods=['GET', 'POST'])
def add_book():
    if request.method == 'POST':
        title = request.form['title']
        author = request.form['author']
        genre = request.form['genre']
        pub_date = request.form['publication_date']
        isbn = request.form['isbn']

        conn = pyodbc.connect(conn_str)
        cursor = conn.cursor()
        cursor.execute('INSERT INTO Inventory (Title, Author, Genre, PublicationDate, ISBN) VALUES (?, ?, ?, ?, ?)', 
                       (title, author, genre, pub_date, isbn))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))

    return render_template('add_book.html')

# Export books data
@app.route('/export/<file_format>')
def export_books(file_format):
    conn = pyodbc.connect(conn_str)
    df = pd.read_sql("SELECT * FROM Inventory", conn)
    conn.close()

    if file_format == 'csv':
        file_path = os.path.join('exports', 'books.csv')
        df.to_csv(file_path, index=False)
    elif file_format == 'json':
        file_path = os.path.join('exports', 'books.json')
        df.to_json(file_path, orient='records')

    return send_file(file_path, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
