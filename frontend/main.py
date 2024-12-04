from flask import Flask, render_template, request, redirect, url_for, jsonify
import requests
import os, datetime, time

API_BASE_URL = "http://backend:8000"

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

# Route to send the new plan to the API
@app.route('/add-plan', methods=['POST'])
def add_plan():
    # Extract data from the form fields
    goal = request.form['goal']
    deadline = request.form['deadline']
    daily_hours = request.form['daily_hours']

    # Create payload for the API request
    payload = {
        'goal': goal,
        'deadline': datetime.datetime.strptime(deadline, '%Y-%m-%d').date().strftime('%Y-%m-%d'),
        'daily_hours': float(daily_hours)
    }

    # Send data to the API endpoint
    response = requests.post(f'{API_BASE_URL}/api/v1/plans/', json=payload)
    
    # Check if the API request was successful
    if response.status_code == 201:
        time.sleep(5)
        return "Error", 500
    else:
        return "Error adding plan", 500

# Route to reset the database
@app.route('/reset-database', methods=['GET'])
def reset_database():
    response = requests.delete(f"{API_BASE_URL}/api/v1/plans/")

    if response.status_code == 200:
        return render_template('index.html')
    else:
        return "Error while resetting database", 500

if __name__ == '__main__':
    app.run(debug=True, port=3000, host='0.0.0.0')