from flask import Flask, jsonify, render_template, request, redirect, url_for, session
from database import register_student

app = Flask(__name__)


@app.route('/')
def home(): 
    return render_template('Main.html')

@app.route('/student')
def student():
    return render_template('student.html')

@app.route('/login', methods=['GET', 'POST'])
def login():

    if request.method == 'POST':

        data = request.get_json()

        # We'll check the database here

        return jsonify({
            "success": True,
            "redirect": "/student"
        })

    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():

    if request.method == 'POST':

        data = request.get_json()

        student_id = register_student(data)

        return jsonify({
            "success": True,
            "message": "Registration successful!",
            "redirect": f"/registration-success/{student_id}"
        })

    return render_template('register.html')

@app.route('/registration-success/<int:student_id>')
def registration_success(student_id):

    return render_template(
        'registration_success.html',
        student_id=student_id
    )


@app.route('/Admin')
def admin():
    return render_template('Admin.html')


if __name__ =='__main__':
    app.run(debug=True)