from flask import Flask, render_template, request
import pickle
import numpy as np
import pandas as pd
import mysql.connector


popular_df = pd.read_pickle(open('popular.pkl', 'rb'))
pt = pd.read_pickle(open('pt.pkl', 'rb'))
books = pd.read_pickle(open('books.pkl', 'rb'))
similarity_scores = pd.read_pickle(open('similarity_scores.pkl', 'rb'))

app = Flask(__name__)

# app.config['MYSQL_HOST'] = 'localhost'
# app.config['MYSQL_USER'] = 'chakri'
# app.config['MYSQL_PASSWORD'] = 'Chakri@1905'
# app.config['MYSQL_DB'] = 'book_ratings'
#
# mysql = MySQL(app)

mydb = mysql.connector.connect(
  host="localhost",
  user="chakri",
  password="Chakri@1905",
  database="bookratingsdb",
auth_plugin='mysql_native_password'
)
print(mydb)


@app.route('/')
def index():
    return render_template('index.html',
                           book_name=list(popular_df['Book-Title'].values),
                           author=list(popular_df['Book-Author'].values),
                           image=list(popular_df['Image-URL-M'].values),
                           votes=list(popular_df['num_ratings'].values),
                           rating=list(popular_df['avg_rating'].values)
                           )


@app.route('/recommend')
def recommend_ui():
    return render_template('recommend.html')


@app.route('/users')
def users_ui():
    return render_template('users.html')


@app.route('/users_ratings', methods=['GET','POST'])
def users():
    global data
    if request.method == 'POST':
        mycursor = mydb.cursor()

        user_id = request.form['user_id']
        isbn = request.form['isbn']
        rating = request.form['rating']
        Book_title=request.form['Book_title']
        data=[]
        data.append(user_id)
        data.append(isbn)
        data.append(Book_title)
        data.append(rating)
        data.append('Rating submitted successfully!')
        mycursor.execute("INSERT INTO bookratings (User_ID, ISBN, Book_Rating,Book_title) VALUES (%s, %s, %s,%s)", (user_id, isbn, rating,Book_title))
        mydb.commit()
        print(mycursor.rowcount, "record inserted.")
        # return 'Rating submitted successfully!'
    return render_template('users.html',data=data)


@app.route('/recommend_books', methods=['post'])
def recommend():
    user_input = request.form.get('user_input')
    index = np.where(pt.index == user_input)[0][0]
    similar_items = sorted(list(enumerate(similarity_scores[index])), key=lambda x: x[1], reverse=True)[1:5]

    data = []
    for i in similar_items:
        item = []
        temp_df = books[books['Book-Title'] == pt.index[i[0]]]
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Title'].values))
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Author'].values))
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Image-URL-M'].values))

        data.append(item)

    print(data)

    return render_template('recommend.html', data=data)


if __name__ == '__main__':
    app.run(debug=True)
