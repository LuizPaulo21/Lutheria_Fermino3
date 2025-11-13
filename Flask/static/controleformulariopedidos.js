            // --- Obtendo os elementos HTML para manipulação ---
            const quantidadeInput = document.getElementById('quantidade');
            const valorUnitarioInput = document.getElementById('valorUnitario');
            const valorTotalItemInput = document.getElementById('valorTotalItem');
            const tipoConsertoRadio = document.getElementById('tipoConserto');
            const tipoCompraRadio = document.getElementById('tipoCompra');
            const campoPrazoConsertoDiv = document.getElementById('campoPrazoConserto');
            const prazoConsertoInput = document.getElementById('prazoConserto');
            const nomeClienteInput = document.getElementById('nomeCliente');
            const clienteIdInput = document.getElementById('clienteId');
            const clienteSelecionadoDataInput = document.getElementById('clienteSelecionadoDataInput');   
            

            function calcularValorTotalItem() {
                const quantidade = parseFloat(quantidadeInput.value) || 0;
                const valorUnitario = parseFloat(valorUnitarioInput.value) || 0;
                const total = quantidade * valorUnitario;
                valorTotalItemInput.value = total.toFixed(2).replace('.', ',');
            }
            quantidadeInput.addEventListener('input', calcularValorTotalItem);
            valorUnitarioInput.addEventListener('input', calcularValorTotalItem);
            calcularValorTotalItem(); // Chama na inicialização

            // --- CONTROLE DO CAMPO PRAZO ---
            function togglePrazoConserto() {
                if (tipoConsertoRadio.checked) {
                    campoPrazoConsertoDiv.style.display = 'block';
                    prazoConsertoInput.setAttribute('required', 'required');
                } else {
                    campoPrazoConsertoDiv.style.display = 'none';
                    prazoConsertoInput.removeAttribute('required');
                    prazoConsertoInput.value = ''; // Limpa o valor se não for conserto
                }
            }
            tipoConsertoRadio.addEventListener('change', togglePrazoConserto);
            tipoCompraRadio.addEventListener('change', togglePrazoConserto);
            togglePrazoConserto(); // Chama na inicialização

                        // --- SUBMISSÃO DO FORMULÁRIO ---
            formIncluirPedido.addEventListener('submit', function(event) {
                if (!formIncluirPedido.checkValidity()) {
                    event.preventDefault();
                    event.stopPropagation();
                    // Força a exibição de mensagens de erro do Bootstrap
                    formIncluirPedido.classList.add('was-validated');
                    // Verifica se os campos de busca têm IDs válidos
                    if (!clienteIdInput.value) {
                        nomeClienteInput.setCustomValidity("Por favor, selecione um cliente da lista.");
                        nomeClienteInput.classList.add('is-invalid');
                    } else {
                        nomeClienteInput.setCustomValidity("");
                        nomeClienteInput.classList.remove('is-invalid');
                    }
                    if (!produtoIdInput.value) {
                        nomeProdutoInput.setCustomValidity("Por favor, selecione um produto/serviço da lista.");
                        nomeProdutoInput.classList.add('is-invalid');
                    } else {
                        nomeProdutoInput.setCustomValidity("");
                        nomeProdutoInput.classList.remove('is-invalid');
                    }
                    // Adiciona a classe was-validated para mostrar feedback visual
                    formIncluirPedido.classList.add('was-validated');
                     alert('Por favor, corrija os erros no formulário antes de salvar.');
                    return;
                }
                // Se passou na validação HTML5 e campos de busca estão OK
                nomeClienteInput.setCustomValidity("");
                nomeProdutoInput.setCustomValidity("");
                formIncluirPedido.classList.add('was-validated');

                const formData = new FormData(formIncluirPedido);
                const data = {};
                formData.forEach((value, key) => {
                    data[key] = value;
                });

                // Garante que IDs estão corretos
                data['clienteId'] = clienteIdInput.value.toString();
                data['nomeCliente'] = nomeClienteInput.value;
                data['produtoId'] = produtoIdInput.value;
                data['quantidade'] = quantidadeInput.value;
                data['valorUnitario'] = valorUnitarioInput.value;//.replace(',', '.');
                data['valorTotalItem'] = valorTotalItemInput.value;//.replace(',', '.');
                if (data.tipoPedido !== 'conserto') {
                    delete data.prazoConserto; // Remove prazo se não for conserto
                }
                if(data.clienteSelecionadoDataInput === 'true') {
                    delete data.clienteSelecionadoDataInput; // Remove o campo se não for necessário
                }
                

                fetch(formIncluirPedido.action, { //Chama o Action do formulário
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify(data) // Envia o objeto 'data' como JSON
                })

                //Lógica para a listagem de produtos

                //Resetar o formulário
                formIncluirPedido.reset();
                formIncluirPedido.classList.remove('was-validated');
                document.getElementById('dataPedido').value = today;
                togglePrazoConserto();
                calcularValorTotalItem();
                clienteIdInput.value = '';
                produtoIdInput.value = '';
                valorUnitarioInput.value = '';
            });
