// Espera até que o DOM (Document Object Model) tenha sido completamente carregado
document.addEventListener('DOMContentLoaded', function() {
  const emailInput = document.getElementById('email');
  const passwordInput = document.getElementById('password');
  const loginButton = document.querySelector('input[type="submit"]');

  // Função para validar os campos de e-mail e senha
  function validarCampos() {
    const email = emailInput.value.trim(); // Remove espaços em branco no início e no final do valor do campo
    const password = passwordInput.value.trim(); // Remove espaços em branco no início e no final do valor do campo

    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/; // Expressão regular para validar o formato do e-mail
    const senhaMinima = 8; // Tamanho mínimo da senha
    const senhaMaxima = 24; // Tamanho máximo da senha

    const emailValido = emailRegex.test(email); // Verifica se o e-mail corresponde ao formato válido
    const senhaValida = password.length >= senhaMinima && password.length <= senhaMaxima; // Verifica se a senha tem o tamanho adequado

    // Desabilita o botão de login se o e-mail ou a senha forem inválidos
    loginButton.disabled = !(emailValido && senhaValida);
  }

  // Adiciona um ouvinte de eventos para o evento "input" no campo de e-mail
  emailInput.addEventListener('input', validarCampos);

  // Adiciona um ouvinte de eventos para o evento "input" no campo de senha
  passwordInput.addEventListener('input', validarCampos);
});
