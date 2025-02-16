from flask import Blueprint, render_template, request, flash, redirect, url_for, session
from ..models import Note, db

notes_bp = Blueprint('notes', __name__)

# Rota para exibir todas as notas do usuário
@notes_bp.route('/notes')
def notes_page():
    if 'user_id' not in session:
        flash('Faça login para acessar esta página.', 'warning')
        return redirect(url_for('auth.login'))
    
    user_id = session['user_id']
    notes = Note.query.filter_by(user_id=user_id).all()
    return render_template('notes.html', user_name=session['user_name'], notes=notes)

# Rota para salvar uma nova nota
@notes_bp.route('/save_note', methods=['POST'])
def save_note():
    if 'user_id' not in session:
        flash('Faça login para acessar esta página.', 'warning')
        return redirect(url_for('auth.login'))
    
    title = request.form['title']
    content = request.form['content']
    user_id = session['user_id']

    if not title or not content:
        flash('Título e conteúdo são obrigatórios.', 'danger')
        return redirect(url_for('notes.notes_page'))

    new_note = Note(title=title, content=content, user_id=user_id)
    db.session.add(new_note)
    db.session.commit()

    flash('Nota salva com sucesso!', 'success')
    return redirect(url_for('notes.notes_page'))

# Rota para editar uma nota existente
@notes_bp.route('/edit_note/<int:note_id>', methods=['GET', 'POST'])
def edit_note(note_id):
    if 'user_id' not in session:
        flash('Faça login para acessar esta página.', 'warning')
        return redirect(url_for('auth.login'))
    
    note = Note.query.get_or_404(note_id)
    if note.user_id != session['user_id']:
        flash('Você não tem permissão para editar esta nota.', 'danger')
        return redirect(url_for('notes.notes_page'))

    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']

        if not title or not content:
            flash('Título e conteúdo são obrigatórios.', 'danger')
            return redirect(url_for('notes.edit_note', note_id=note_id))

        note.title = title
        note.content = content
        db.session.commit()

        flash('Nota editada com sucesso!', 'success')
        return redirect(url_for('notes.notes_page'))
    
    return render_template('edit_note.html', note=note)

# Rota para excluir uma nota
@notes_bp.route('/delete_note/<int:note_id>', methods=['POST'])
def delete_note(note_id):
    if 'user_id' not in session:
        flash('Faça login para acessar esta página.', 'warning')
        return redirect(url_for('auth.login'))
    
    note = Note.query.get_or_404(note_id)
    if note.user_id != session['user_id']:
        flash('Você não tem permissão para excluir esta nota.', 'danger')
        return redirect(url_for('notes.notes_page'))

    db.session.delete(note)
    db.session.commit()

    flash('Nota excluída com sucesso!', 'success')
    return redirect(url_for('notes.notes_page'))