// Função para formatar um campo de moeda
function formatarMoeda(inputId) {
  const input = document.getElementById(inputId);
  const valor = input.value.replace(/\D/g, ''); // Remove todos os caracteres não numéricos
  const parsedValor = parseFloat(valor); // Converte para um número float

  if (!isNaN(parsedValor)) {
    // Se o número for válido, formata-o como uma string de moeda e atualiza o valor do campo
    input.value = (parsedValor / 100).toLocaleString('pt-BR', {
      style: 'currency',
      currency: 'BRL',
    });
  } else {
    // Caso contrário, limpa o valor do campo
    input.value = '';
  }
}

// Evento que é acionado quando a opção "is_installment" é alterada
$("#is_installment").on("change", function() {
  if ($(this).is(":checked")) {
    // Se a opção for marcada, mostra os campos relacionados às parcelas e esconde outros campos
    $("#installment-fields").show();
    $("#value-field").hide();
    $("#date-field").hide();
    calcularValorRestante();
    calcularInformacoesParcelas();
  } else {
    // Caso contrário, mostra os campos padrão e limpa as informações relacionadas às parcelas
    $("#installment-fields").hide();
    $("#value-field").show();
    $("#date-field").show();
    $("#valor_restante").text("");
    $("#parcelas-list").empty();
  }
});

// Evento que é acionado quando o campo "installment_value" é alterado
$("#installment_value").on("input", function() {
  formatarMoeda("installment_value");
  calcularValorRestante();
  calcularInformacoesParcelas();
});

// Evento que é acionado quando o campo "installment_count" é alterado
$("#installment_count").on("change", function() {
  calcularValorRestante();
  calcularInformacoesParcelas();
});

// Evento que é acionado quando o campo "due_date" é alterado
$("#due_date").on("change", function() {
  calcularInformacoesParcelas();
});

// Evento que é acionado quando o campo "total_value" é alterado
$("#total_value").on("input", function() {
  formatarMoeda("value");
  calcularValorParcela();
  calcularValorRestante();
  calcularInformacoesParcelas();
});

// Função para calcular o valor da parcela com base no valor total e no número de parcelas
function calcularValorParcela() {
  const valorTotal = document.getElementById("value").value.replace(/\D/g, ''); // Remove todos os caracteres não numéricos
  const numeroParcelas = parseInt(document.getElementById("installment_count").value); // Converte para um número inteiro

  const parsedValorTotal = parseFloat(valorTotal); // Converte para um número float

  if (!isNaN(parsedValorTotal) && numeroParcelas > 0) {
    // Se o valor total e o número de parcelas forem válidos, calcula o valor da parcela e atualiza o campo "installment_value"
    const valorParcela = (parsedValorTotal / numeroParcelas).toLocaleString('pt-BR', {
      style: 'currency',
      currency: 'BRL',
    });

    $("#installment_value").val(valorParcela);
  } else {
    // Caso contrário, limpa o valor do campo
    $("#installment_value").val('');
  }
}

// Função para calcular o valor restante com base no valor da parcela e no número de parcelas
function calcularValorRestante() {
  const valorParcela = document.getElementById("installment_value").value.replace(/\D/g, ''); // Remove todos os caracteres não numéricos
  const numeroParcelas = parseInt(document.getElementById("installment_count").value); // Converte para um número inteiro

  const parsedValorParcela = parseFloat(valorParcela); // Converte para um número float

  if (!isNaN(parsedValorParcela) && numeroParcelas > 0) {
    // Se o valor da parcela e o número de parcelas forem válidos, calcula o valor restante e atualiza o campo "valor_restante"
    const valorRestante = ((parsedValorParcela * numeroParcelas) / 100).toLocaleString('pt-BR', {
      style: 'currency',
      currency: 'BRL',
    });

    $("#valor_restante").text(valorRestante);
  } else {
    // Caso contrário, limpa o campo "valor_restante"
    $("#valor_restante").text("");
  }
}

let isShowingAllInstallments = false;

// Função para calcular e exibir as informações das parcelas
function calcularInformacoesParcelas() {
  const valorParcela = document.getElementById("installment_value").value.replace(/\D/g, ''); // Remove todos os caracteres não numéricos
  const numeroParcelas = parseInt(document.getElementById("installment_count").value); // Converte para um número inteiro
  const dataDespesa = moment(document.getElementById("due_date").value, 'YYYY-MM-DD'); // Converte para um objeto Moment.js

  const parsedValorParcela = parseFloat(valorParcela); // Converte para um número float

  if (!isNaN(parsedValorParcela) && numeroParcelas > 0 && dataDespesa.isValid()) {
    // Se o valor da parcela, o número de parcelas e a data da despesa forem válidos
    const parcelasList = $("#parcelas-list");
    parcelasList.empty();

    const maxItems = isShowingAllInstallments ? numeroParcelas : 3; // Define o número máximo de parcelas a serem exibidas

    for (let i = 1; i <= maxItems; i++) {
      // Loop para exibir as informações de cada parcela
      const valorParcelaFormatado = (parsedValorParcela / 100).toLocaleString('pt-BR', {
        style: 'currency',
        currency: 'BRL',
      });

      const dataParcela = dataDespesa.clone().add(i - 1, 'months');
      const dataParcelaFormatada = dataParcela.format('DD/MM/YYYY');

      const listItem = $("<li>").text(`Parcela ${i}: Valor ${valorParcelaFormatado} - Vencimento ${dataParcelaFormatada}`);

      parcelasList.append(listItem);
    }

    if (numeroParcelas > 3) {
      // Se houver mais de 3 parcelas, exibe um link para mostrar todas as parcelas
      const showAllSpan = $("<span>")
        .attr("id", "show-installments-span")
        .addClass("link-span")
        .text("Ver todas as parcelas")
        .on("click", function () {
          isShowingAllInstallments = !isShowingAllInstallments;
          calcularInformacoesParcelas();
        });

      const showAllDiv = $("<div>").attr("id", "show-all-installments").append(showAllSpan);

      parcelasList.after(showAllDiv);
    }
  }
}

// Chama a função de cálculo das informações das parcelas ao terminar de carregar a página
calcularInformacoesParcelas();
