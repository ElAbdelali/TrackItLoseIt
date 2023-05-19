from flask import (Flask, render_template, request, flash, session, jsonify,
                   redirect)
from datetime import datetime
from model import connect_to_db, db
from jinja2 import StrictUndefined

import crud, model
import spoonacularsearch

app = Flask(__name__)
app.secret_key = "dev"
app.jinja_env.undefined = StrictUndefined

@app.route('/')
def homepage():
    """View homepage"""
    
    return render_template('homepage.html')

@app.route('/tdee')
def index():
    return render_template('calculate_tdee.html')

@app.route('/calculate', methods=['POST'])
def calculate():
    gender = request.form.get('gender')
    age = int(request.form.get('age'))
    weight = float(request.form.get('weight'))
    height = float(request.form.get('height'))
    activity = request.form.get('activity')

    # Calculate BMR based on gender
    if gender == 'male':
        bmr = 66 + (6.23 * weight) + (12.7 * height) - (6.8 * age)
    else:
        bmr = 655 + (4.35 * weight) + (4.7 * height) - (4.7 * age)

    # Calculate TDEE based on activity level
    if activity == 'sedentary':
        tdee = bmr * 1.2
    elif activity == 'lightly_active':
        tdee = bmr * 1.375
    elif activity == 'moderately_active':
        tdee = bmr * 1.55
    elif activity == 'very_active':
        tdee = bmr * 1.725
    else:
        tdee = bmr * 1.9

    return redirect('/result?gender={}&age={}&weight={}&height={}&activity={}&bmr={}&tdee={}'.format(
        gender, age, weight, height, activity, bmr, tdee))

@app.route('/result')
def result():
    gender = request.args.get('gender')
    age = int(request.args.get('age'))
    weight = float(request.args.get('weight'))
    height = float(request.args.get('height'))
    activity = request.args.get('activity')
    bmr = float(request.args.get('bmr'))
    tdee = float(request.args.get('tdee'))

    return render_template('result.html', gender=gender, age=age, weight=weight, height=height,
                           activity=activity, bmr=bmr, tdee=tdee)
    
@app.route('/signup', methods=['GET','POST'])
def signup():
    if request.method == 'POST':
        # Retrieve form data
        username = request.form.get('username')
        password = request.form.get('password')
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        date_of_birth = request.form.get('date_of_birth')
        email = request.form.get('email')

        # Create a new user object
        new_user = crud.create_user(
            username=username,
            password=password,
            first_name=first_name,
            last_name=last_name,
            date_of_birth=date_of_birth,
            email=email,
            created_at=datetime.datetime.now()
        )

        db.session.add(new_user)
        db.session.commit()

        # Flash a success message
        # flash('Signup successful', 'success')

        # Redirect to the homepage
        return redirect('/')
    else:
        return render_template('signup.html')


if __name__ == "__main__":
    connect_to_db(app)
    app.run(host="0.0.0.0", debug=True)