from flask import Blueprint, jsonify, request, session, flash, redirect, url_for, render_template
from ..models import Checklist, db

checklist_bp = Blueprint('checklist', __name__)

# Rota para exibir a página do checklist
@checklist_bp.route('/checklist')
def checklist_page():
    if 'user_id' not in session:
        flash('Faça login para acessar esta página.', 'warning')
        return redirect(url_for('auth.login'))
    
    return render_template('checklist.html')

# Rota para obter a lista de itens do checklist
@checklist_bp.route('/_checklist', methods=['GET'])
def get_checklist():
    if 'user_id' not in session:
        return jsonify({"error": "Usuário não autenticado"}), 401
    
    user_id = session['user_id']
    items = Checklist.query.filter_by(user_id=user_id).all()
    return jsonify([{"id": item.id, "name": item.name, "checked": item.checked} for item in items])

# Rota para adicionar um novo item ao checklist
@checklist_bp.route('/save_checklist', methods=['POST'])
def add_checklist_item():
    if 'user_id' not in session:
        return jsonify({"error": "Usuário não autenticado"}), 401

    data = request.json
    if not data or 'name' not in data:
        return jsonify({"error": "Dados inválidos"}), 400

    new_item = Checklist(name=data['name'], user_id=session['user_id'])
    db.session.add(new_item)
    db.session.commit()
    
    return jsonify({"id": new_item.id, "name": new_item.name, "checked": new_item.checked}), 201

# Rota para alternar o status de um item (marcado/desmarcado)
@checklist_bp.route('/checklist/<int:item_id>', methods=['PATCH'])
def toggle_checklist_item(item_id):
    if 'user_id' not in session:
        return jsonify({"error": "Usuário não autenticado"}), 401

    item = Checklist.query.get_or_404(item_id)
    if item.user_id != session['user_id']:
        return jsonify({"error": "Acesso negado"}), 403

    item.checked = not item.checked
    db.session.commit()

    return jsonify({"id": item.id, "checked": item.checked})

# Rota para excluir um item do checklist
@checklist_bp.route('/checklist/<int:item_id>', methods=['DELETE'])
def delete_checklist_item(item_id):
    if 'user_id' not in session:
        return jsonify({"error": "Usuário não autenticado"}), 401

    item = Checklist.query.get_or_404(item_id)
    if item.user_id != session['user_id']:
        return jsonify({"error": "Acesso negado"}), 403

    db.session.delete(item)
    db.session.commit()
    
    return jsonify({"message": "Item removido"}), 200