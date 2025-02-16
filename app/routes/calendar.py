from flask import Blueprint, render_template, session, flash, redirect, url_for
from ..models import CalendarEvent, db
from datetime import datetime

calendar_bp = Blueprint('calendar', __name__)

# Rota para exibir o calendário
@calendar_bp.route('/calendar')
def calendar_page():
    if 'user_id' not in session:
        flash('Faça login para acessar esta página.', 'warning')
        return redirect(url_for('auth.login'))

    user_id = session['user_id']
    
    # Recuperar eventos do usuário no banco de dados
    events = CalendarEvent.query.filter_by(user_id=user_id).all()
    
    # Formatar eventos para o frontend
    calendar_events = []
    for event in events:
        calendar_events.append({
            'title': event.title,
            'start': event.date.strftime('%Y-%m-%dT%H:%M:%S'),
            'end': event.date.strftime('%Y-%m-%dT%H:%M:%S'),
            'description': event.description,
        })

    return render_template('calendar.html', events=calendar_events)
