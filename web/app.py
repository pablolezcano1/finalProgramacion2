from flask import Flask, render_template, request, redirect, url_for, flash
import requests

app = Flask(__name__)
app.secret_key = 'tu_clave_secreta'  # Necesario para usar flash

API_BASE_URL = "http://localhost:8000"  # URL de tu API FastAPI

@app.route('/')
def index():
    return redirect(url_for('users'))

@app.route('/users')
def users():
    response = requests.get(f"{API_BASE_URL}/users/")
    users = response.json()
    return render_template('users.html', users=users)

@app.route('/users/create', methods=['GET', 'POST'])
def create_user():
    if request.method == 'POST':
        user_data = {
            "name": request.form['name'],
            "email": request.form['email']
        }
        response = requests.post(f"{API_BASE_URL}/users/", json=user_data)
        if response.status_code == 200:
            flash('Usuario creado exitosamente', 'success')
            return redirect(url_for('users'))
        else:
            flash('Error al crear el usuario', 'error')
    return render_template('create_user.html')

@app.route('/users/<int:user_id>/edit', methods=['GET', 'POST'])
def edit_user(user_id):
    if request.method == 'POST':
        user_data = {
            "name": request.form['name'],
            "email": request.form['email']
        }
        response = requests.put(f"{API_BASE_URL}/users/{user_id}", json=user_data)
        if response.status_code == 200:
            flash('Usuario actualizado exitosamente', 'success')
            return redirect(url_for('users'))
        else:
            flash('Error al actualizar el usuario', 'error')
    else:
        response = requests.get(f"{API_BASE_URL}/users/{user_id}")
        user = response.json()
        return render_template('edit_user.html', user=user)

@app.route('/users/<int:user_id>/delete', methods=['POST'])
def delete_user(user_id):
    response = requests.delete(f"{API_BASE_URL}/users/{user_id}")
    if response.status_code == 200:
        flash('Usuario eliminado exitosamente', 'success')
    else:
        flash('Error al eliminar el usuario', 'error')
    return redirect(url_for('users'))

@app.route('/tasks')
def tasks():
    user_id = request.args.get('user_id')
    if user_id:
        response = requests.get(f"{API_BASE_URL}/users/{user_id}/tasks")
    else:
        response = requests.get(f"{API_BASE_URL}/tasks/")
    tasks = response.json()
    
    # Filtrar tareas completadas
    tasks = [task for task in tasks if task['status'] != 'completada']
    
    users_response = requests.get(f"{API_BASE_URL}/users/")
    users = users_response.json()
    
    return render_template('tasks.html', tasks=tasks, users=users, selected_user_id=user_id)

@app.route('/tasks/create', methods=['GET', 'POST'])
def create_task():
    if request.method == 'POST':
        task_data = {
            "title": request.form['title'],
            "description": request.form['description'],
            "status": request.form['status'],
            "user_id": int(request.form['user_id'])
        }
        response = requests.post(f"{API_BASE_URL}/users/{task_data['user_id']}/tasks", json=task_data)
        if response.status_code == 200:
            flash('Tarea creada exitosamente', 'success')
            return redirect(url_for('tasks'))
        else:
            flash('Error al crear la tarea', 'error')
    
    # GET request
    users_response = requests.get(f"{API_BASE_URL}/users/")
    users = users_response.json()
    return render_template('create_task.html', users=users)

@app.route('/tasks/<int:task_id>/edit', methods=['GET', 'POST'])
def edit_task(task_id):
    if request.method == 'POST':
        task_data = {
            "title": request.form['title'],
            "description": request.form['description'],
            "status": request.form['status'],
            "user_id": int(request.form['user_id'])
        }
        response = requests.put(f"{API_BASE_URL}/tasks/{task_id}", json=task_data)
        if response.status_code == 200:
            flash('Tarea actualizada exitosamente', 'success')
            return redirect(url_for('tasks'))
        else:
            flash('Error al actualizar la tarea', 'error')
    else:
        response = requests.get(f"{API_BASE_URL}/tasks/{task_id}")
        task = response.json()
        users_response = requests.get(f"{API_BASE_URL}/users/")
        users = users_response.json()
        return render_template('edit_task.html', task=task, users=users)

@app.route('/tasks/<int:task_id>/delete', methods=['POST'])
def delete_task(task_id):
    response = requests.delete(f"{API_BASE_URL}/tasks/{task_id}")
    if response.status_code == 200:
        flash('Tarea eliminada exitosamente', 'success')
    else:
        flash('Error al eliminar la tarea', 'error')
    return redirect(url_for('tasks'))

if __name__ == '__main__':
    app.run(debug=True)