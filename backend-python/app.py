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

#This method stores a sent message, exposing the http endpoint for the frontend
#to call. There should be three frontend methods to send the three different
#types of messages, each setting values that aren't used to the null equivalent
#for each value.
@app.route('/send_message', methods=['GET'])
def send_message():
    #Get all fields from incoming json request
    text = request.args.get('text')
    if (text == None || len(text > 1000)):
        raise ValueError("Text can only be up to 1000 characters")
    width = request.args.get('width')
    height = request.args.get('height')
    duration = request.args.get('duration')
    video_source = request.args.get('videosource')
    sender = request.args.get('sender')
    if (sender == None):
        raise ValueError("Cannot have no sender on a message")
    receiver = request.args.get('receiver')
    if (sender == None):
        raise ValueError("Cannot have no receiver on a message")
    with db.cursor() as cur:
        sql = "INSERT INTO Messages VALUES(%s,%d,%d,%s,%s,%s,%s)"
        cur.execute(sql, (text, width, height, duration, video_source, sender, receiver))
        db.commit()

#Gets the paginated list of messages between sender and receiver specified
#(or vice versa)
@app.route('/fetch_message', methods=['GET'])
def fetch_message():
    sender = request.args.get('sender')
    if (sender == None):
        raise ValueError("Cannot have no sender on a message")
    receiver = request.args.get('receiver')
    if (sender == None):
        raise ValueError("Cannot have no receiver on a message")
    #Get all fields from incoming json request
    per_page = request.args.get('requestsperpage')
    page_number = request.args.get('page')
    header = "SET @rank=0\n\n"
    select = "SELECT @rank:=rank+1 AS rank, text, senttime FROM MESSAGES "
    where_clause1 = "WHERE (sender = %s and receiver = %s) "
    where_clause2 = "OR (sender = %s and receiver = %s)"
    optional_where_clause = ""
    if (per_page != None and page_number != None):
        pagination = "WHERE rank BETWEEN %d and %d" % ((page_number-1), (page_number-1) + per_page)
        optional_where_clause = optional_where_clause + pagination
    order_by = "ORDER BY sentime asc"
    sql = header + select + where_clause1 + where_clause2 + optional_where_clause + order_by
    with db.cursor(cursors.DictCursor) as cur:
        cur.execute(sql, (sender, receiver, receiver, sender))
        result_set = cursor.fetchall()
        if not result_set:
            raise ValueError("No messages found between users %s and %s" % sender, receiver)
        return result_set