from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Books(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    author = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    date = db.Column(db.DateTime, default=datetime.now())

    def __repr__(self):
        return f'<Books {self.id}>'


@app.route('/')
@app.route('/Home')
def home():
    return render_template('index.html')


@app.route('/books')
@app.route('/books.html')
def books():
    details = Books.query.order_by(Books.date.desc()).all()
    return render_template('books.html', books=details)\


@app.route('/books/<int:book_id>')
def book_detail(book_id):
    book = Books.query.get(book_id)
    return render_template('book_detail.html', book=book)


@app.route('/books/<int:book_id>/delete')
def book_delete(book_id):
    book = Books.query.get_or_404(book_id)
    try:
        db.session.delete(book)
        db.session.commit()
        return redirect('/books.html')
    except:
        return "An error occurred while deleting!"


@app.route('/books/<int:book_id>/edit', methods=['POST', "GET"])
def edit(book_id):
    book = Books.query.get(book_id)
    if request.method == "POST":
        book.title = request.form['title']
        book.author = request.form['author']
        book.description = request.form['description']
        try:
            db.session.commit()
            return redirect('/books')
        except:
            return "An error occurred while updating!!"
    else:
        return render_template('edit.html', book=book)


@app.route('/add', methods=["POST", "GET"])
def add():
    if request.method == "POST":
        title = request.form['title']
        author = request.form['author']
        description = request.form['description']

        book = Books(title=title, author=author, description=description)
        try:
            db.session.add(book)
            db.session.commit()
            return redirect('/books')
        except:
            return "An error occurred while adding a new book!"
    else:
        return render_template('add.html')


if __name__ == '__main__':
    app.run(debug=True)
