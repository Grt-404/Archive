from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime

app = Flask(__name__)

todos = []

@app.route('/')
def index():
    return render_template('index.html', todos=todos)

@app.route('/add', methods=['POST'])
def add_todo():
    task = request.form.get('task')
    if task:
        todos.append({
            'id': len(todos) + 1,
            'task': task,
            'created': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'completed': False
        })
    return redirect(url_for('index'))

@app.route('/delete/<int:todo_id>')
def delete_todo(todo_id):
    global todos
    todos = [t for t in todos if t['id'] != todo_id]
    return redirect(url_for('index'))

@app.route('/complete/<int:todo_id>')
def complete_todo(todo_id):
    for todo in todos:
        if todo['id'] == todo_id:
            todo['completed'] = not todo['completed']
    return redirect(url_for('index'))

@app.route('/stats')
def stats():
    total = len(todos)
    completed = sum(1 for t in todos if t['completed'])
    remaining = total - completed
    return render_template('stats.html', total=total, completed=completed, remaining=remaining)
# so that all ip's can access the app and it runs on port 5000 with debug mode enabled
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
