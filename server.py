from flask import (Flask, render_template, request, flash, session, jsonify,
                   redirect)
import datetime
from model import connect_to_db, db
from jinja2 import StrictUndefined

import crud, model
from crud import create_user
import spoonacularsearch

app = Flask(__name__)
app.secret_key = "dev"
app.jinja_env.undefined = StrictUndefined

@app.route('/')
def homepage():
    """View homepage"""
    
    return render_template('homepage.html')

@app.route('/calculate', methods=['GET', 'POST'])
def calculate():
    if request.method == 'POST':
        gender = request.form.get('gender')
        age = int(request.form.get('age'))
        weight = float(request.form.get('weight'))
        height = float(request.form.get('height'))
        activity = request.form.get('activity')

        # Perform calculations based on the form inputs
        bmr = calculate_bmr(gender, age, weight, height)
        tdee = calculate_tdee(bmr, activity)

        return render_template('calculate_tdee.html', tdee=tdee)
    else:
        return render_template('calculate_tdee.html')

def calculate_bmr(gender, age, weight, height):

    if gender == 'male':
        bmr = 88.362 + (13.397 * weight) + (4.799 * height) - (5.677 * age)
    else:
        bmr = 447.593 + (9.247 * weight) + (3.098 * height) - (4.330 * age)

    return bmr

def calculate_tdee(bmr, activity):
    # Define activity multipliers based on the selected activity level
    activity_multipliers = {
        'sedentary': 1.2,
        'lightly_active': 1.375,
        'moderately_active': 1.55,
        'very_active': 1.725,
        'super_active': 1.9
    }

    # Calculate TDEE by multiplying BMR with the activity multiplier
    tdee = bmr * activity_multipliers.get(activity, 1.2)

    return tdee

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
def register_user():
        """Create new User"""
        username = request.form.get('username')
        password = request.form.get('password')
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        date_of_birth = request.form.get('date_of_birth')
        email = request.form.get('email')
        
        # Create a new user object
        user = create_user(
            username,
            password,
            first_name,
            last_name,
            date_of_birth,
            email,
            created_at=datetime.datetime.now()
        )

        user_exists = crud.get_user_by_email(email)
        if user_exists:
            flash("Cannot create an account with that email. Try again.")
        else:
            # user = crud.create_user(email, password, first_name, last_name, date_of_birth, email, created_at=datetime.datetime.now())
            db.session.add(user)
            db.session.commit()
        flash("Account created! Please log in.")

        return render_template('homepage.html')

@app.route('/chart')
def chart():
    return render_template('weight_tracker.html')
if __name__ == "__main__":
    connect_to_db(app)
    app.run(host="0.0.0.0", debug=True)