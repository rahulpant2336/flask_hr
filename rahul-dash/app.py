from flask import Flask, redirect, url_for, render_template, request
from flask_mysqldb import MySQL
import yaml
from wtforms import Form, StringField, TextAreaField, PasswordField, validators


app = Flask(__name__)

# CONFIGURE db
db = yaml.load(open('db.yaml'))
app.config['MYSQL_HOST'] = db['mysql_host']
app.config['MYSQL_USER'] = db['mysql_user']
app.config['MYSQL_PASSWORD'] = db['mysql_password']
app.config['MYSQL_DB'] = db['mysql_db']

mysql = MySQL(app)

@app.route('/', methods=['GET', 'POST'])
def register_page():
    if request.method == 'POST':
        #FETCH FORM DATA
        userDetails = request.form
        first_name = userDetails['first_name']
        last_name = userDetails['last_name']
        email = userDetails['email']
        password = userDetails['password']

        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO users(first_name,last_name,email,password) VALUES(%s, %s,%s, %s)",first_name, last_name, email, password)
        mysql.connection.commit()
        cur.close()
        return 'success'

    return render_template('register.html')


@app.route('/users')
def users():
    cur = mysql.connection.cursor()
    resultValue = cur.execute("SELECT * FROM users")
    if resultValue > 0:
        userDetails = cur.fecthall()
        return render_template('users.html', userDetails=userDetails)



if __name__ == '__main__':
   app.run(debug = True)
