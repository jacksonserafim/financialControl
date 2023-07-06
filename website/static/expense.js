function formatarMoeda(inputId) {
  const input = document.getElementById(inputId);
  const valor = input.value.replace(/\D/g, '');
  const parsedValor = parseFloat(valor);

  if (!isNaN(parsedValor)) {
    input.value = (parsedValor / 100).toLocaleString('pt-BR', {
      style: 'currency',
      currency: 'BRL',
    });
  } else {
    input.value = '';
  }
}

$(document).ready(function() {
  $("#is_installment").on("change", function() {
    if ($(this).is(":checked")) {
      $("#installment-fields").show();
      $("#value-field").hide();
      $("#date-field").hide();
      calcularValorRestante();
      calcularInformacoesParcelas();
    } else {
      $("#installment-fields").hide();
      $("#value-field").show();
      $("#date-field").show();
      $("#valor_restante").text("");
      $("#parcelas-list").empty();
    }
  });

  $("#installment_value").on("input", function() {
    formatarMoeda("installment_value");
    calcularValorRestante();
    calcularInformacoesParcelas();
  });

  $("#installment_count").on("change", function() {
    calcularValorRestante();
    calcularInformacoesParcelas();
  });

  $("#due_date").on("change", function() {
    calcularInformacoesParcelas();
  });

  // Adicionando evento de alteração ao campo do valor total
  $("#total_value").on("input", function() {
    formatarMoeda("value");
    calcularValorParcela();
    calcularValorRestante();
    calcularInformacoesParcelas();
  });

  // Chamar as funções de cálculo ao terminar de carregar a página
  calcularValorParcela();
  calcularValorRestante();
  calcularInformacoesParcelas();
});

function calcularValorParcela() {
  const valorTotal = document.getElementById("value").value.replace(/\D/g, '');
  const numeroParcelas = parseInt(document.getElementById("installment_count").value);

  const parsedValorTotal = parseFloat(valorTotal);

  if (!isNaN(parsedValorTotal) && numeroParcelas > 0) {
    const valorParcela = (parsedValorTotal / numeroParcelas).toLocaleString('pt-BR', {
      style: 'currency',
      currency: 'BRL',
    });

    $("#installment_value").val(valorParcela);
  } else {
    $("#installment_value").val('');
  }
}

function calcularValorRestante() {
  const valorParcela = document.getElementById("installment_value").value.replace(/\D/g, '');
  const numeroParcelas = parseInt(document.getElementById("installment_count").value);

  const parsedValorParcela = parseFloat(valorParcela);

  if (!isNaN(parsedValorParcela) && numeroParcelas > 0) {
    const valorRestante = ((parsedValorParcela * numeroParcelas) / 100).toLocaleString('pt-BR', {
      style: 'currency',
      currency: 'BRL',
    });

    $("#valor_restante").text(valorRestante);
  } else {
    $("#valor_restante").text("");
  }
}

let isShowingAllInstallments = false;

function calcularInformacoesParcelas() {
  const valorParcela = document.getElementById("installment_value").value.replace(/\D/g, '');
  const numeroParcelas = parseInt(document.getElementById("installment_count").value);
  const dataDespesa = moment(document.getElementById("due_date").value, 'YYYY-MM-DD');

  const parsedValorParcela = parseFloat(valorParcela);

  if (!isNaN(parsedValorParcela) && numeroParcelas > 0 && dataDespesa.isValid()) {
    const parcelasList = $("#parcelas-list");
    parcelasList.empty();

    const maxItems = isShowingAllInstallments ? numeroParcelas : 3;

    for (let i = 1; i <= maxItems; i++) {
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

// Chamar a função de cálculo ao terminar de carregar a página
calcularInformacoesParcelas();
