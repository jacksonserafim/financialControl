from flask import Blueprint, render_template, request, redirect, make_response, flash

auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    return render_template('login.html')


@auth.route('/logout')
def logout():
    return 'LOGOUT'


@auth.route('sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form['email']
        firstName = request.form['nome']
        lastName = request.form['sobrenome']
        senha = request.form['password']
        confirma_senha = request.form['password2']

        if len(email) < 4:
            flash('Insira um email válido', category='error')
        elif len(firstName) < 2:
            flash('Insira um nome válido (Mais que 1 (uma) letra)', category='error')
        elif len(lastName) < 2:
            flash('Insira um sobrenome válido (Mais que 1 (uma) letra)', category='error')
        elif senha != confirma_senha:
            flash('As senhas devem ser iguais', category='error')
        elif 7 <= len(senha) > 24:
            flash('A sua senha deve possuir entre 8 e 24 caracteres', category='error')
        else:
            flash('Conta criada com sucesso!', category='success')

        # if senha == confirma_senha:
        #     # Redirecionar para a rota de sucesso após o processamento do formulário
        #     response = make_response(redirect('/'))
        #
        #     # Definir o cabeçalho de cache-control para evitar armazenamento em cache
        #     response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
        #
        #     return response
        # else:
        #     return "A senha e a confirmação de senha não coincidem."
    return render_template('sign-up.html')
