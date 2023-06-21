// registro.js
document.addEventListener('DOMContentLoaded', function() {
  const senhaInput = document.getElementById('password');
  const confirmaSenhaInput = document.getElementById('password2');
  const erroSenhaElement = document.getElementById('erro-senha');
  const formulario = document.getElementById('registro-form');
  const camposObrigatorios = Array.from(formulario.querySelectorAll('[required]'));
  const inputRegistrar = document.getElementById('btn_registrar');
  let timeoutMostrarInput;

  function validarSenhas() {
    if (confirmaSenhaInput.value === '') {
      erroSenhaElement.textContent = '';

      inputRegistrar.disabled = true;
    } else if (senhaInput.value !== confirmaSenhaInput.value) {
      erroSenhaElement.textContent = 'As senhas não coincidem.';
      inputRegistrar.disabled = true;
    } else {
      erroSenhaElement.textContent = '';
      inputRegistrar.disabled = false;
    }
  }

  function verificarCamposPreenchidos() {
    const camposPreenchidos = camposObrigatorios.every(function(campo) {
      return campo.value.trim() !== '';
    });

    if (camposPreenchidos && senhaInput.value === confirmaSenhaInput.value) {
      inputRegistrar.disabled = false;
    } else {
      inputRegistrar.disabled = true;
    }
  }

  confirmaSenhaInput.addEventListener('input', function() {
    clearTimeout(timeoutMostrarInput);
    timeoutMostrarInput = setTimeout(function() {
      validarSenhas();
      verificarCamposPreenchidos();
    }, 500); // Atraso de 500ms antes de verificar os campos preenchidos
  });

  camposObrigatorios.forEach(function(campo) {
    campo.addEventListener('input', verificarCamposPreenchidos);
  });
});
