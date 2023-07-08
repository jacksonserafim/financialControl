from flask import Blueprint, render_template, redirect, url_for, request, flash
from .models import Expense
from . import db
from datetime import datetime
from flask_login import login_required, current_user

views = Blueprint('views', __name__)

# Rota para a página inicial
@views.route('/', methods=['GET'])
@login_required
def home():
    try:
        expenses = Expense.query.filter_by(user_id=current_user.id)
        total_value = sum(expense.value for expense in expenses)
        return render_template('home.html', user=current_user, total_value=total_value)
    except Exception as e:
        flash('Ocorreu um erro ao carregar as despesas.', category='error')
        return redirect(url_for('views.home'))

# Rota para adicionar uma nova despesa
@views.route('/despesas', methods=['GET', 'POST'])
@login_required
def expense():
    if request.method == 'POST':
        try:
            name = request.form.get('name')
            value_str = request.form.get('value')
            value_str = value_str.replace('R$', '').replace('.', '').replace(',', '.').strip()
            value = float(value_str) if value_str else 0.0
            is_installment = bool(request.form.get('is_installment'))
            installment_count = int(request.form.get('installment_count'))
            date = request.form.get('date')
            due_date = '0/0/0000'
            comment = request.form.get('comment')
            default_cat = request.form.get('category')

            # Mapear a categoria padrão
            match default_cat:
                case '1':
                    default_cat = 'Alimentação'
                case '2':
                    default_cat = 'Transporte'
                case '3':
                    default_cat = 'Moradia'
                case '4':
                    default_cat = 'Lazer'
                case '5':
                    default_cat = 'Educação'

            if is_installment:
                installment_value_str = request.form.get('installment_value')
                installment_value_str = installment_value_str.replace('R$', '').replace('.', '').replace(',', '.').strip()
                installment_value = float(installment_value_str)
                due_date = request.form.get('due_date')

                value = installment_value * installment_count  # Somar valor total das parcelas
                date = datetime.now().date()

            # Cria uma instância de Expense
            expense = Expense(
                name=name,
                value=value,
                is_installment=is_installment,
                installment_count=installment_count,
                installment_value=value / installment_count,
                due_date=due_date,
                user_id=current_user.id,
                date=date,
                comment=comment,
                default_cat=default_cat
            )

            # Salve a despesa no banco de dados
            db.session.add(expense)
            db.session.commit()

            flash('Despesa adicionada', category='success')
        except Exception as e:
            flash(f'Ocorreu um erro ao atualizar a despesa. {e}', category='error')
            db.session.rollback()

    return render_template('expense.html', user=current_user)

# Rota para editar uma despesa existente
@views.route('/edit/<int:expense_id>', methods=['GET', 'POST'])
@login_required
def edit_expense(expense_id):
    expense = Expense.query.get_or_404(expense_id)

    if request.method == 'POST':
        try:
            # Obtenha os dados enviados no formulário de edição
            name = request.form['name']
            value_str = request.form.get('value')
            value_str = value_str.replace('R$', '').replace('.', '').replace(',', '.').strip()
            value = float(value_str) if value_str else 0.0
            is_installment = bool(request.form.get('is_installment'))
            installment_value = float(request.form.get('installment_value')) if is_installment else None
            installment_count = int(request.form.get('installment_count')) if is_installment else None
            due_date = request.form.get('due_date') if is_installment else None
            comment = request.form.get('comment')
            default_cat = request.form.get('category')

            # Mapear a categoria padrão
            match default_cat:
                case '1':
                    default_cat = 'Alimentação'
                case '2':
                    default_cat = 'Transporte'
                case '3':
                    default_cat = 'Moradia'
                case '4':
                    default_cat = 'Lazer'
                case '5':
                    default_cat = 'Educação'

            # Atualize os campos da despesa existente
            expense.name = name
            expense.value = value
            expense.is_installment = is_installment
            expense.installment_value = installment_value
            expense.installment_count = installment_count
            expense.due_date = due_date
            expense.comment = comment
            expense.default_cat = default_cat
            # Outros campos de atualização

            # Salve as alterações no banco de dados
            db.session.commit()

            flash('Despesa atualizada', category='success')
            return redirect(url_for('views.home'))
        except Exception as e:
            flash(f'Ocorreu um erro ao atualizar a despesa. {e}', category='error')
            db.session.rollback()

    return render_template('edit_expense.html', expense=expense, user=current_user)

@views.route('/delete/<int:expense_id>', methods=['GET'])
@login_required
def delete_expense(expense_id):
    try:
        expense = Expense.query.get_or_404(expense_id)
        db.session.delete(expense)
        db.session.commit()
        flash(f'Despesa {expense.name} excluída.', category='success')
    except Exception as e:
        flash('Ocorreu um erro ao tentar excluir.', category='error')
        db.session.rollback()

    return redirect(url_for('views.home'))
