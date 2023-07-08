from flask import Blueprint, render_template, request, redirect, make_response, flash, url_for
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from website import db
from datetime import datetime
from flask_login import login_user, login_required, logout_user, current_user

auth = Blueprint('auth', __name__)

# Rota para login de usuário
@auth.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('views.home'))

    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()

        if user:
            if check_password_hash(user.password, password):
                flash('Logado com sucesso!', category='success')
                login_user(user, remember=True)
                user.last_login = datetime.utcnow()
                db.session.commit()
                return redirect(url_for('views.home'))
            else:
                flash('Senha incorreta, tente novamente!', category='error')
        else:
            flash('E-mail não registrado', category='error')

    flash('PROJETO EM DESENVOLVIMENTO - Muitos bugs e falta de funcionalidades', category='primary')
    return render_template('login.html', user=current_user)


# Rota para logout de usuário
@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Sessão encerrada!', category='success')
    return redirect(url_for('auth.login'))


# Rota para cadastro de novo usuário
@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if current_user.is_authenticated:
        return redirect(url_for('views.home'))

    if request.method == 'POST':
        email = request.form['email']
        first_name = request.form['nome']
        last_name = request.form['sobrenome']
        password = request.form['password']
        password_confirm = request.form['password2']

        user = User.query.filter_by(email=email).first()

        if user:
            flash('E-mail já cadastrado!', category='error')
        elif len(email) < 4:
            flash('Insira um email válido', category='error')
        elif len(first_name) < 2:
            flash('Insira um nome válido (Mais que 1 (uma) letra)', category='error')
        elif len(last_name) < 2:
            flash('Insira um sobrenome válido (Mais que 1 (uma) letra)', category='error')
        elif password != password_confirm:
            flash('As senhas devem ser iguais', category='error')
        elif not 7 <= len(password) <= 24:
            flash('A sua senha deve possuir entre 8 e 24 caracteres', category='error')
        else:
            # Criação de um novo usuário
            new_user = User(
                email=email,
                name=first_name,
                last_name=last_name,
                password=generate_password_hash(password, method='scrypt'),
                created_at=datetime.utcnow(),
                last_login=datetime.utcnow()
            )
            db.session.add(new_user)
            db.session.commit()

            login_user(new_user, remember=True)

            flash('Conta criada com sucesso!', category='success')

            # Redirecionar para a rota de sucesso após o processamento do formulário
            response = make_response(redirect(url_for('views.home')))

            # Definir o cabeçalho de cache-control para evitar armazenamento em cache
            response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'

            return response

    return render_template('sign-up.html', user=current_user)
