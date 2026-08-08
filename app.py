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

        student_id = register_student(request.form)

        return render_template(
            'registration_success.html',
            student_id=student_id
        )

    return render_template('register.html')

@app.route('/Admin')
def admin():
    return render_template('Admin.html')


if __name__ =='__main__':
    app.run(debug=True)