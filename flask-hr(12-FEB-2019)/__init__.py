from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_mysqldb import MySQL
import yaml
from flask_user import roles_required

app = Flask(__name__)
db = yaml.load(open('db.yaml'))
app.secret_key = '3242353645646'

app.config['MYSQL_HOST'] = db['mysql_host']
app.config['MYSQL_USER'] = db['mysql_user']
app.config['MYSQL_PASSWORD'] = db['mysql_password']
app.config['MYSQL_DB'] = db['mysql_db']

mysql = MySQL(app)



@app.route('/')
def Index():
    return render_template('register.html')



@app.route('/register', methods = ['POST'])
def insert():

    if request.method == "POST":
        flash("Registration success!!!")
        first_name = str(request.form['first_name'])
        middle_name = str(request.form['middle_name'])
        last_name = str(request.form['last_name'])
        email = str(request.form['email'])
        phone = request.form['phone']
        password = str(request.form['password'])
        role = 2
        confirm_password = str(request.form['confirm_password'])
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO students (first_name, middle_name, last_name, email, phone, password, confirm_password, role) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
                    (first_name, middle_name, last_name, email, phone, password, confirm_password, role))
        mysql.connection.commit()
        return redirect(url_for('Index'))




@app.route('/delete/<string:id_data>', methods = ['GET'])
def delete(id_data):
    flash("Record Has Been Deleted Successfully")
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM students WHERE id=%s", (id_data,))
    mysql.connection.commit()
    return redirect(url_for('Index'))





@app.route('/update',methods=['POST','GET'])
def update():

    if request.method == 'POST':
        id_data = request.form['id']
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        cur = mysql.connection.cursor()
        cur.execute("""
               UPDATE students
               SET name=%s, email=%s, phone=%s
               WHERE id=%s
            """, (name, email, phone, id_data))
        flash("Data Updated Successfully")
        mysql.connection.commit()
        return redirect(url_for('Index'))


@app.route('/login')
def login():
    return render_template('login.html', title="data")

@app.route('/dashboard')
def dashboard():
    return render_template('evalution-form.html')

@app.route('/login-check', methods = ['POST'])
def checkLogin():

    if request.method == 'POST':
        error = None
        email = str(request.form['email'])
        password = str(request.form['password'])
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM students WHERE email ='"+email+"' AND password ='"+password+"'")
        data = cur.fetchone()

        if len(data) is 1:
            return redirect(url_for('dashboard', students=data))

        else:
            return 'Invalid User'






if __name__ == "__main__":
    app.run(debug=True)
