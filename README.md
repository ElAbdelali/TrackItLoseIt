# Track It, Lose It
## _Hackbright Capstone Project_

Track It, Lose It is a Web Application developed to provide a structured and accessible web application for personal weight management. Whether the goal is weight loss, weight gain, or weight maintenance, this application streamlines the process of tracking health and fitness data while offering access to calorie-specific recipes. By combining features such as calculating TDEE, weight tracking and exercise monitoring, Track It, Lose It facilitates accountability and makes it easier for users to achieve their weight goals.

## Features
- **Personalized Webpage**: Each user can create a personal account, ensuring privacy and customization.
- **Total Daily Energy Expenditure (TDEE) Calculation**: Users can input critical information such as weight, height, age, and activity levels to calculate their Total Daily Energy Expenditure. This calculation helps guide dietary choices and track progress.
- **Daily Weight Input and Visualization**: Users can record their weight daily, and the application visually represents this data using Chart.js. The graphical representation allows users to monitor their weight loss or gain over time.
- **Daily Log Notes**: Users can input daily notes, including details such as weigh-ins, workouts, and food consumed. This feature encourages users to maintain a holistic view of their health and fitness routines.
- **Access to Spoonacular Web API**: The application integrates with the Spoonacular Web API, allowing users to search for calorie-specific recipes. This feature helps users discover new, healthy recipes and incorporate them into their meal plans.

## Tech Stack
Category | Tech
--- | --- 
**Backend** | Flask, Python, PostgreSQL, SQLAlchemy
**Frontend** | JavaScript, HTML, CSS, Bootstrap
**API** | Spoonacular API
**Other** |  Jinja

## TDEE Calculation based on User input in Track it, Lose it
![TDEE Calculation](https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExZTI0MzMxYjc3NTNmMDU0YjcxNWI1NWE1NDdjYTRhNjE4ZGZjNDQzZSZlcD12MV9pbnRlcm5hbF9naWZzX2dpZklkJmN0PWc/6H3Mo9uakSttH3zki9/giphy.gif)

## Installation
To set up Track It, Lose It locally, follow these steps:

1. Clone this repository to your local machine:
   ```sh
   git clone https://github.com/ElAbdelali/TrackItLoseIt.git
   ```

2. Navigate to the project's root directory in your command line interface.
3. Set up a virtual environment:
   ```sh
   virtualenv env
   source env/bin/activate
   ```

4. Install the required dependencies:
   ```sh
   pip3 install -r requirements.txt
   ```

5. Create trackitloseit db in PostgreSQL and run the model.py to create the tables. Make sure you have PostgreSQL installed:
   ```sh
   python3 model.py
   ```

6. Start the server to launch Track It, Lose It:
   ```sh
   python3 server.py
   ```

## Author
Abdelali Eljaouhari, Hackbright Graduate
[Github](https://github.com/ElAbdelali/TrackItLoseIt)
[LinkedIn](https://www.linkedin.com/in/ali-eljaouhari/)

