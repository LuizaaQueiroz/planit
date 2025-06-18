from flask import Flask, render_template, request, redirect, url_for, make_response
from models import db, User, Task, Note, Event
from datetime import datetime
from xhtml2pdf import pisa
from io import BytesIO
import calendar

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///planit.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'your_secret_key'

db.init_app(app)

with app.app_context():
    db.create_all()

# -------- Dashboard --------
@app.route('/')
def dashboard():
    user_id = 1

    total_tasks = Task.query.filter_by(user_id=user_id).count()
    completed_tasks = Task.query.filter_by(user_id=user_id, status='Concluída').count()
    percent = int((completed_tasks / total_tasks) * 100) if total_tasks > 0 else 0

    recent_tasks = Task.query.filter(
        Task.user_id == user_id,
        Task.status != 'Concluída'
    ).order_by(Task.due_date.asc().nullslast()).limit(5).all()

    notes_count = Note.query.filter_by(user_id=user_id).count()

    today = datetime.today().date()
    upcoming_tasks = Task.query.filter(
        Task.user_id == user_id,
        Task.due_date >= today
    ).order_by(Task.due_date.asc()).limit(5).all()

    today = datetime.today()
    return render_template(
        'dashboard.html',
        total_tasks=total_tasks,
        completed_tasks=completed_tasks,
        percent=percent,
        recent_tasks=recent_tasks,
        notes_count=notes_count,
        upcoming_tasks=upcoming_tasks,
        year=today.year,
        month=today.month
    )

# -------- Tasks --------
@app.route('/tasks')
def list_tasks():
    user_id = 1
    status_filter = request.args.get('status')

    if status_filter == 'pendentes':
        tasks = Task.query.filter_by(user_id=user_id, status='Pendente').all()
    elif status_filter == 'concluidas':
        tasks = Task.query.filter_by(user_id=user_id, status='Concluída').all()
    else:
        tasks = Task.query.filter_by(user_id=user_id).all()

    return render_template('tasks.html', tasks=tasks, status_filter=status_filter)

@app.route('/tasks/create', methods=['GET', 'POST'])
def create_task():
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        due_date_str = request.form.get('due_date')
        due_date = datetime.strptime(due_date_str, '%Y-%m-%d').date() if due_date_str else None

        new_task = Task(title=title, description=description, due_date=due_date, user_id=1)
        db.session.add(new_task)
        db.session.commit()
        return redirect(url_for('list_tasks'))
    return render_template('create_task.html')

@app.route('/tasks/delete/<int:id>')
def delete_task(id):
    task = Task.query.get_or_404(id)
    db.session.delete(task)
    db.session.commit()
    return redirect(url_for('list_tasks'))

@app.route('/tasks/complete/<int:id>')
def complete_task(id):
    task = Task.query.get_or_404(id)
    task.status = 'Concluída'
    db.session.commit()
    return redirect(url_for('list_tasks'))

@app.route('/tasks/complete_from_dashboard/<int:id>')
def complete_task_from_dashboard(id):
    task = Task.query.get_or_404(id)
    task.status = 'Concluída'
    db.session.commit()
    return redirect(url_for('dashboard'))

@app.route('/tasks/pdf')
def generate_tasks_pdf():
    tasks = Task.query.filter_by(user_id=1).all()
    html = render_template('tasks_pdf.html', tasks=tasks)
    result = BytesIO()
    pisa_status = pisa.CreatePDF(html, dest=result)
    if pisa_status.err:
        return "Erro ao gerar o PDF", 500
    response = make_response(result.getvalue())
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = 'inline; filename=tarefas.pdf'
    return response

# -------- Notes --------
@app.route('/notes')
def list_notes():
    notes = Note.query.filter_by(user_id=1).all()
    return render_template('notes.html', notes=notes)

@app.route('/notes/create', methods=['GET', 'POST'])
def create_note():
    if request.method == 'POST':
        content = request.form['content']
        new_note = Note(content=content, user_id=1)
        db.session.add(new_note)
        db.session.commit()
        return redirect(url_for('list_notes'))
    return render_template('create_note.html')

@app.route('/notes/delete/<int:id>')
def delete_note(id):
    note = Note.query.get_or_404(id)
    db.session.delete(note)
    db.session.commit()
    return redirect(url_for('list_notes'))

# -------- Calendar Redirect --------
@app.route('/calendar')
def calendar_redirect():
    today = datetime.today()
    return redirect(url_for('calendar_view', year=today.year, month=today.month))

# -------- Calendar View --------
@app.route('/calendar/<int:year>/<int:month>')
def calendar_view(year, month):
    user_id = 1

    if month < 1 or month > 12:
        return redirect(url_for('calendar_redirect'))

    cal = calendar.Calendar()
    month_days = list(cal.itermonthdays(year, month))

    month_start = datetime(year, month, 1)
    month_end = datetime(year + (month // 12), (month % 12) + 1, 1)

    month_tasks = Task.query.filter(
        Task.user_id == user_id,
        Task.due_date >= month_start,
        Task.due_date < month_end
    ).all()

    month_events = Event.query.filter(
        Event.user_id == user_id,
        Event.date >= month_start.date(),
        Event.date < month_end.date()
    ).all()

    events_by_day = {}
    for task in month_tasks:
        if task.due_date:
            day = task.due_date.day
            events_by_day.setdefault(day, []).append({
                'type': 'task',
                'title': task.title,
                'time': task.due_date.time() if task.due_date.time() else None,
                'id': None
            })

    for event in month_events:
        day = event.date.day
        events_by_day.setdefault(day, []).append({
            'type': 'event',
            'title': event.title,
            'time': event.time,
            'id': event.id
        })

    prev_month = month - 1 if month > 1 else 12
    prev_year = year - 1 if month == 1 else year
    next_month = month + 1 if month < 12 else 1
    next_year = year + 1 if month == 12 else year

    current_date = datetime.today()

    return render_template(
        'calendar.html',
        year=year,
        month=month,
        month_name=calendar.month_name[month],
        month_days=month_days,
        events_by_day=events_by_day,
        prev_year=prev_year,
        prev_month=prev_month,
        next_year=next_year,
        next_month=next_month,
        current_date=current_date
    )

# -------- Criar evento --------
@app.route('/events/create/<int:year>/<int:month>/<int:day>', methods=['GET', 'POST'])
def create_event_for_day(year, month, day):
    user_id = 1
    if request.method == 'POST':
        title = request.form['title']
        time_str = request.form['time']
        time_obj = datetime.strptime(time_str, '%H:%M').time() if time_str else None
        new_event = Event(title=title, date=datetime(year, month, day).date(), time=time_obj, user_id=user_id)
        db.session.add(new_event)
        db.session.commit()
        return redirect(url_for('calendar_view', year=year, month=month))
    return render_template('create_event_for_day.html', year=year, month=month, day=day)

# -------- Excluir evento --------
@app.route('/events/delete/<int:id>')
def delete_event(id):
    event = Event.query.get_or_404(id)
    target_year = event.date.year
    target_month = event.date.month
    db.session.delete(event)
    db.session.commit()
    return redirect(url_for('calendar_view', year=target_year, month=target_month))

if __name__ == '__main__':
    app.run(debug=True)
