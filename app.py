from flask import Flask, render_template, request, redirect, session
from flask_cors import CORS
from datetime import datetime
import sqlite3
import json

from flask import jsonify 

app = Flask(__name__)
CORS(app)

app.secret_key = 'OfirTalCode'

if __name__ == '__main__':
    app.run(debug=True)

@app.route('/', methods = ['POST', 'GET'])
def home():
    if 'username' in session:
        user_type = session["user_type"]
        username = session['username']
        return render_template('home.html', user_type = user_type, username=username)
    else:
        user_type = "guest"
        return render_template('home.html', user_type = user_type)

@app.route('/login_page', methods = ['POST', 'GET'])
def login_page():
    return render_template('login.html')

@app.route('/login', methods = ['POST', 'GET'])
def login():
    if request.method == "POST":
        username = request.form.get('username')
        password = request.form.get('password')
        existing_users = query(f"SELECT * FROM users WHERE username = '{username}' AND password='{password}'")
        if existing_users:
            user_data = existing_users[0]
            session['username'] = user_data[1]
            session['password'] = user_data[2]
            session['user_type'] = user_data[3]  

            return redirect('/')
        else:
            return render_template('login.html', error='No user was found, please contact the administrator')

@app.route('/logout', methods = ['POST', 'GET'])
def logout():
    session.pop('username', None)
    session.pop('password', None)
    session.pop('user_type', None)
    return redirect('/')

@app.route('/new_lead', methods = ['POST'])
def new_lead():
    name = request.form.get('name')
    phone = request.form.get('phone')
    Date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    contact = "no"
    contact_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    insert_new_lead(values=f"'{name}', '{phone}', '{Date}', '{contact}', '{contact_date}'")  
    return jsonify({})


@app.route('/admin', methods = ['GET','POST'])
def admin():
    user_type = session["user_type"]
    username = session['username']
    leads =query(sql=f"SELECT * FROM leads")
    users= query(sql=f"SELECT * FROM users")
    classes = query(sql=f"SELECT * FROM classes")
    if request.method == 'GET':  
        return render_template('admin.html',user_type = user_type, username=username,leads=leads,users=users,classes=classes)
    if request.method == 'POST':  
        action = request.form.get('action')  
        if action == "contact":
            lead_id = request.form.get('lead_id')
            contact_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            query(sql=f"UPDATE leads SET contact='yes', contact_date='{contact_date}' WHERE id={lead_id}")
        if action == "reset_password":
            user_id = request.form.get('user_id')
            query(sql=f"UPDATE users SET password='12345' WHERE id={user_id}")
        if action == "delete_user":
            user_id = request.form.get('user_id')
            query(sql=f"DELETE FROM users WHERE id={user_id}")
        if action == "add_user":
            username = request.form.get('username')
            password ="12345"
            permission = request.form.get('permission')
            if permission == "user" or "admin":
                permission = permission
            else:
                permission = "user"
            query(sql=f"INSERT INTO users (username,password,permission) VALUES ('{username}','{password}', '{permission}')")
        if action == "delete_class":
            class_id = request.form.get('class_id')
            query(sql=f"DELETE FROM classes WHERE class_id={class_id}")
        if action == "add_class":
            class_name = request.form.get('class_name')
            day = request.form.get('day')
            hour = request.form.get('hour')
            query(sql=f"INSERT INTO classes (class_name,class_day,class_hour,subscribers) VALUES ('{class_name}','{day}', '{hour}', 0)")
        return render_template('admin.html',user_type = user_type, username=username,leads=leads,users=users,classes=classes)


@app.route('/classes', methods = ['POST', 'GET'])
def classes():
    if 'username' in session:
        user_type = session["user_type"]
        username = session['username']
        return render_template('classes.html', user_type = user_type, username=username)
    else:
        return render_template('login.html')
 
@app.route('/api/classes', methods = ['GET'])
def api_classes():
    classes_json = []
    username = session.get('username')
    user_id =query(sql=f"SELECT id FROM users WHERE username='{username}'")[0][0]
    existing_classes = query(f"SELECT * FROM classes")
    subscribers_in_class = [sub[0] for sub in query(sql=f"SELECT class_id FROM classes_subscribers WHERE user_id={user_id}")]
    for exist_class in existing_classes:
        if exist_class[0] not in subscribers_in_class:
            class_json = {"id": exist_class[0], "className": exist_class[1], "day": exist_class[2], "hour": exist_class[3], "subscribers": exist_class[4], "userInClass":False}
            classes_json.append(class_json)
        else:
            class_json = {"id": exist_class[0], "className": exist_class[1], "day": exist_class[2], "hour": exist_class[3], "subscribers": exist_class[4], "userInClass":True}
            classes_json.append(class_json)
    return json.dumps(classes_json)


@app.route('/api/classes/book', methods=['POST', 'GET'])
def book_class():
    if request.method == 'POST':
        try:
            data_received = request.json
            username = session.get('username')
            class_id = data_received.get('id')
            user_id =query(sql=f"SELECT id FROM users WHERE username='{username}'")[0][0]

            query(sql=f"UPDATE classes SET subscribers=subscribers+1 WHERE class_id={class_id}")
            query(sql=f"INSERT INTO classes_subscribers (user_id,class_id) VALUES ('{user_id}','{class_id}')")
            return json.dumps({"success": True})

        except:
            return json.dumps({"error": "error happend"})

@app.route('/api/classes/remove', methods=['POST', 'GET'])
def remove_class():
    if request.method == 'POST':
        try:
            data_received = request.json
            username = session.get('username')
            class_id = data_received.get('id')
            user_id =query(sql=f"SELECT id FROM users WHERE username='{username}'")[0][0]

            query(sql=f"UPDATE classes SET subscribers=subscribers-1 WHERE class_id={class_id}")
            query(sql=f"DELETE FROM classes_subscribers WHERE user_id={user_id} AND class_id={class_id}")

            return json.dumps({"success": True})
        except:
            return json.dumps({"error": "error happend"})

## db

def query(sql:str="", db_name="pilates.db"):
    with sqlite3.connect(db_name) as conn:
        cur = conn.cursor()
        rows = cur.execute(sql)
        return list(rows)    
    

# def create_table(table="users"):
#     sql = f"CREATE TABLE IF NOT EXISTS {table} (username TEXT, password TEXT)"
#     query(sql)

# def create_table(table="leads"):
#     sql = f"CREATE TABLE IF NOT EXISTS {table} (name TEXT, phone TEXT, Date TEXT)"
#     query(sql)

# def create_table(table="leads"):
#     sql = f"CREATE TABLE IF NOT EXISTS {table} (name TEXT, phone TEXT, Date TEXT)"
#     query(sql)

# create_table()
    
def insert_new_lead(table="leads", values=""):
    sql = f"INSERT INTO {table} (name, phone, Date, contact, contact_date) VALUES ({values})"
    query(sql)


# def create_table(table="classes"):
#     sql = f"CREATE TABLE IF NOT EXISTS {table} (class_id NT AUTO_INCREMENT PRIMARY KEY, class_name TEXT, class_day TEXT, class_hour INT)"
#     query(sql)
    
# def create_table(table="classes_subscribers"):
#     sql = f"CREATE TABLE IF NOT EXISTS {table} (subscriber_id INT AUTO_INCREMENT PRIMARY KEY)"
#     query(sql)

# create_table()
    
