from flask import Blueprint, render_template, redirect, url_for, request
from .models import Expense
from . import db
from datetime import datetime
from flask_login import login_required, current_user

views = Blueprint('views', __name__)


@views.route('/', methods=['GET'])
@login_required
def home():
    return render_template('home.html', user=current_user)


@views.route('/despesas', methods=['GET', 'POST'])
@login_required
def expense():
    if request.method == 'POST':
        name = request.form.get('name')
        value_str = request.form.get('value')
        value_str = value_str.replace('R$', '').replace(',', '.').strip()
        value = float(value_str) if value_str else 0.0  # Converter para float ou definir valor padrão
        is_installment = bool(request.form.get('is_installment'))
        installment_count = int(request.form.get('installment_count'))
        date = request.form.get('date')
        due_date = '0/0/0000'
        comment = request.form.get('comment')

        if is_installment:
            installment_value_str = request.form.get('installment_value')
            installment_value_str = installment_value_str.replace('R$', '').replace(',', '.').strip()
            installment_value = float(installment_value_str)
            due_date = request.form.get('due_date')

            value = installment_value * installment_count  # Somar valor total das parcelas
            date = datetime.now().date()

        # Crie uma nova instância de Expense
        expense = Expense(
            name=name,
            value=value,
            is_installment=is_installment,
            installment_count=installment_count,
            installment_value=value/installment_count,
            due_date=due_date,
            user_id=current_user.id,
            date=date,
            comment=comment
        )

        # Salve a despesa no banco de dados
        db.session.add(expense)
        db.session.commit()

    return render_template('expense.html', user=current_user)
