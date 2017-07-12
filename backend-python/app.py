import bcrypt
import flask
import pymysql
import pymysql.cursors

app = flask.Flask(__name__)
db = pymysql.connect(
    user='root',
    password='testpass',
    host='db',
    database='challenge',
)

@app.route('/test')
def test():
    with db.cursor() as cur:
        cur.execute("SELECT col FROM test;")
        result, = cur.fetchone()
        return flask.jsonify({
            'result': result,
            'backend': 'python',
        })

@app.route('/register/')
def register(username='rohan', password='anicepassword'):
    with db.cursor() as cur:
        salt = bcrypt.gensalt()
        sql = "INSERT INTO Users VALUES(%s,%s,%s)"
        cur.execute(sql, (username, salt, password))
        db.commit()