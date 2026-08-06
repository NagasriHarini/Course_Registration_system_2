from flask import Flask, render_template, request, redirect, url_for, session
from database import register_student
app = Flask(__name__)


@app.route('/')
def home(): 
    return render_template('Main.html')

@app.route('/student')
def student():
    return render_template('student.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():

    if request.method == 'POST':

        data = request.form

        register_student(data)
        return 'successfully registered'
    return render_template('register.html')

@app.route('/Admin')
def admin():
    return render_template('Admin.html')


if __name__ =='__main__':
    app.run(debug=True)