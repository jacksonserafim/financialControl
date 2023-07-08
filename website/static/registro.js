// Espera até que o DOM (Document Object Model) tenha sido completamente carregado
document.addEventListener('DOMContentLoaded', function() {
  const nomeInput = document.getElementById('nome');
  const sobrenomeInput = document.getElementById('sobrenome');
  const senhaInput = document.getElementById('password');
  const confirmaSenhaInput = document.getElementById('password2');
  const erroSenhaElement = document.getElementById('erro-senha');
  const formulario = document.getElementById('registro-form');
  const camposObrigatorios = Array.from(formulario.querySelectorAll('[required]'));
  const inputRegistrar = document.getElementById('btn_registrar');
  let timeoutMostrarInput;

  // Função para capitalizar a primeira letra de cada palavra, exceto palavras específicas
  function capitalizeFirstLetter(value) {
    const exceptions = ['da', 'do', 'de', 'dos', 'das', 'e']; // Palavras que devem ser ignoradas

    return value
      .toLowerCase()
      .split(' ')
      .map(function(word) {
        if (!exceptions.includes(word)) {
          return word.charAt(0).toUpperCase() + word.slice(1);
        } else {
          return word;
        }
      })
      .join(' ');
  }

  // Função para validar se as senhas coincidem
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

  // Função para verificar se todos os campos obrigatórios foram preenchidos
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

  // Evento acionado quando o campo de confirmação de senha é alterado
  confirmaSenhaInput.addEventListener('input', function() {
    clearTimeout(timeoutMostrarInput);
    timeoutMostrarInput = setTimeout(function() {
      validarSenhas();
      verificarCamposPreenchidos();
    }, 500); // Atraso de 500ms antes de verificar os campos preenchidos
  });

  // Adiciona um ouvinte de eventos para o evento "input" em cada campo obrigatório
  camposObrigatorios.forEach(function(campo) {
    campo.addEventListener('input', verificarCamposPreenchidos);
  });

  // Evento que é acionado quando o campo "nome" perde o foco (blur)
  nomeInput.addEventListener('blur', function() {
    this.value = capitalizeFirstLetter(this.value);
  });

  // Evento que é acionado quando o campo "sobrenome" perde o foco (blur)
  sobrenomeInput.addEventListener('blur', function() {
    this.value = capitalizeFirstLetter(this.value);
  });
});
