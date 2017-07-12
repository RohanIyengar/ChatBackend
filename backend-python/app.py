import bcrypt
import flask
from flask import request
import pymysql
import pymysql.cursors

app = flask.Flask(__name__)
db = pymysql.connect(
    user='root',
    password='testpass',
    host='db',
    database='challenge',
)

# Secret key is hardcoded for now. Would not be in the real service
secret_key = '1036627f0f33d90def2480d71cb6a5b712597e5c'

@app.route('/test')
def test():
    with db.cursor() as cur:
        cur.execute("SELECT col FROM test;")
        result, = cur.fetchone()
        return flask.jsonify({
            'result': result,
            'backend': 'python',
        })

@app.route('/register', methods=['GET'])
def register():
    #Front end should catch and display these errors in the 
    #given human readable format
    username = request.args.get('username')
    if (username == None || len(username > 15)):
        raise ValueError("Username needs to be valid <15 alphanumeric string")
    raw_password = request.args.get('password')
    if (raw_password == None || len(password > 15)):
        raise ValueError("Password needs to be valid <15 alphanumeric string")
    with db.cursor() as cur:
        salt = bcrypt.gensalt()
        combined_password = raw_password + salt + secret_key
        hashed_password = bcrypt.hashpw(combined_password, salt)
        sql = "INSERT INTO Users VALUES(%s,%s,%s)"
        cur.execute(sql, (username, salt, hashed_password))
        db.commit()

# Helper function that can be exposed later if needed to authenticate a user
# Returns true if user has correct credentials, false otherwise
def authenticate(username='rohan', raw_password='sample'):
    with db.cursor(cursors.DictCursor) as cur:
        sql = "SELECT salt, password FROM Users where username = %s"
        cur.execute(sql, username)
        result_set = cursor.fetchall()
        if not result_set:
            raise ValueError("Enter a registered username")
        combined_password = raw_password + result_set['salt'] + secret_key
        hashed_password = result_set['passwordhash']
        return bcrypt.hashpw(combined_password, hashed_password) == hashed_password