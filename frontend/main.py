from flask import Flask, render_template, request, redirect, url_for, jsonify
import requests
import datetime

API_BASE_URL = "http://backend:8000"

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html', error_message='')

# Route to send the new plan to the API
@app.route('/add-plan', methods=['POST'])
def add_plan():
    # Extract data from the form fields
    goal = request.form['goal']
    deadline = request.form['deadline']
    daily_hours = request.form['daily_hours']

    if datetime.datetime.now().date() > datetime.datetime.strptime(deadline, '%Y-%m-%d').date():
        return render_template('index.html', error_message="Invalid deadline")
    
    if float(daily_hours) <= 0:
        return render_template('index.html', error_message="Invalid study time")

    # Create payload for the API request
    payload = {
        'goal': goal,
        'deadline': datetime.datetime.strptime(deadline, '%Y-%m-%d').date().strftime('%Y-%m-%d'),
        'daily_hours': float(daily_hours)
    }

    # Send data to the API endpoint
    response = requests.post(f'{API_BASE_URL}/api/v1/plans/', json=payload)
    if response.status_code != 201:
        return "Error adding plan", 500
    
    response = requests.get(f'{API_BASE_URL}/api/v1/plans/')
    if response.status_code != 200:
        return "Plans not found", 400

    return render_template('plans.html', plans=response.json())

@app.route('/plans', methods=['GET'])
def get_plans():
    response = requests.get(f'{API_BASE_URL}/api/v1/plans/')
    if(response.status_code == 200):
        return render_template('plans.html', plans=response.json())
    
@app.route('/delete-plan/<int:id>', methods=['POST'])
def delete_plan(id):
    response = requests.delete(f'{API_BASE_URL}/api/v1/plans/{id}')
    if response.status_code == 200:
        return redirect(url_for('get_plans'))
    else:
        return "Error adding plan", 500

@app.route('/get-tasks/<int:id>', methods=['GET'])
def get_tasks(id):
    response_task = requests.get(f'{API_BASE_URL}/api/v1/plans/{id}/tasks')
    if response_task.status_code != 200:
        return "Error getting tasks", 500

    response_plan = requests.get(f'{API_BASE_URL}/api/v1/plans/{id}')
    if response_plan.status_code != 200:
        return "Error getting tasks", 500
    
    return render_template('tasks.html', tasks=response_task.json(), plan=response_plan.json())        

@app.route('/toggle-task/<int:plan_id>/<int:task_id>', methods=['POST'])
def toggle_task(plan_id, task_id):
    data = request.get_json()
    completed = data.get('completed')
    payload = {
        'completed': completed
    }
    update_task = requests.patch(f'{API_BASE_URL}/api/v1/plans/{plan_id}/tasks/{task_id}', json=payload)
    if update_task.status_code != 200:
        return 'Error', 500

    response_tasks = requests.get(f'{API_BASE_URL}/api/v1/plans/{plan_id}/tasks')
    if response_tasks.status_code != 200:
        return 'Error', 500

    num_completed_tasks = 0
    for task in response_tasks.json():
        if task['completed'] == True:
            num_completed_tasks = num_completed_tasks + 1

    if len(response_tasks.json()) == 0:
        progress = 0.0
    else:
        progress = num_completed_tasks / len(response_tasks.json())

    payload = {
        'progress': progress
    }

    response_plan = requests.patch(f'{API_BASE_URL}/api/v1/plans/{plan_id}', json=payload)
    if response_plan.status_code != 200:
        return 'Error', 500

    response_plan = requests.get(f'{API_BASE_URL}/api/v1/plans/{plan_id}')
    if response_plan.status_code != 200:
        return 'Error', 500

    return render_template('tasks.html', tasks=response_tasks.json(), plan=response_plan.json())

@app.route('/form-task/<int:plan_id>/<int:task_id>', methods=['POST'])
def update_task_form(plan_id, task_id):
    response_tasks = requests.get(f'{API_BASE_URL}/api/v1/plans/{plan_id}/tasks')
    if response_tasks.status_code != 200:
        return 'Error', 500

    task = [task for task in response_tasks.json() if task['id'] == task_id]

    if len(task) == 0:
        return "Task not found", 404

    task = task[0]

    return render_template('update-task.html', task=task)

@app.route('/update-task/<int:plan_id>/<int:task_id>', methods=['POST'])
def update_task(plan_id, task_id):
    data = request.get_json()

    description = data.get('description')
    completed = data.get('completed')
    payload = {
        'description': description,
        'completed': completed
    }
    
    response_task = requests.patch(f'{API_BASE_URL}/api/v1/plans/{plan_id}/tasks/{task_id}', json=payload)
    if response_task.status_code != 200:
        return 'Error', 500

    response_tasks = requests.get(f'{API_BASE_URL}/api/v1/plans/{plan_id}/tasks')
    if response_tasks.status_code != 200:
        return 'Error', 500

    num_completed_tasks = 0
    for task in response_tasks.json():
        if task['completed'] == True:
            num_completed_tasks = num_completed_tasks + 1

    if len(response_tasks.json()) == 0:
        progress = 0.0
    else:
        progress = num_completed_tasks / len(response_tasks.json())

    payload = {
        'progress': progress
    }

    response_plan = requests.patch(f'{API_BASE_URL}/api/v1/plans/{plan_id}', json=payload)
    if response_plan.status_code != 200:
        return 'Error', 500

    return redirect(url_for('get_tasks', id=plan_id))

@app.route('/delete-task/<int:plan_id>/<int:task_id>', methods=['POST'])
def delete_task(plan_id, task_id):
    response = requests.delete(f'{API_BASE_URL}/api/v1/plans/{plan_id}/tasks/{task_id}')
    if response.status_code != 200:
        return "Error deleting task", 500
    
    response_tasks = requests.get(f'{API_BASE_URL}/api/v1/plans/{plan_id}/tasks')
    if response_tasks.status_code != 200:
        return 'Error', 500

    num_completed_tasks = 0
    for task in response_tasks.json():
        if task['completed'] == True:
            num_completed_tasks = num_completed_tasks + 1

    if len(response_tasks.json()) == 0:
        progress = 0.0
    else:
        progress = num_completed_tasks / len(response_tasks.json())

    payload = {
        'progress': progress
    }

    response_plan = requests.patch(f'{API_BASE_URL}/api/v1/plans/{plan_id}', json=payload)
    if response_plan.status_code != 200:
        return 'Error', 500

    return redirect(url_for('get_tasks', id=plan_id))

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