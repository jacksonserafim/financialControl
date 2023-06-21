document.addEventListener('DOMContentLoaded', function() {
  const emailInput = document.getElementById('email');
  const passwordInput = document.getElementById('password');
  const loginButton = document.querySelector('input[type="submit"]');

  function validarCampos() {
    const email = emailInput.value.trim();
    const password = passwordInput.value.trim();

    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/; // Expressão regular para validar o formato do e-mail
    const senhaMinima = 8; // Tamanho mínimo da senha
    const senhaMaxima = 24; // Tamanho máximo da senha

    const emailValido = emailRegex.test(email);
    const senhaValida = password.length >= senhaMinima && password.length <= senhaMaxima;

    loginButton.disabled = !(emailValido && senhaValida);
  }

  emailInput.addEventListener('input', validarCampos);
  passwordInput.addEventListener('input', validarCampos);
});
