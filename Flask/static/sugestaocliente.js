       document.addEventListener('DOMContentLoaded', function () {
            // --- VALORES INICIAIS E UTILITÁRIOS ---
            const today = new Date().toISOString().split('T')[0];
            document.getElementById('dataPedido').value = today;

            const nomeClienteInput = document.getElementById('nomeCliente');
            const clienteIdInput = document.getElementById('clienteId');
            const sugestoesClientesDiv = document.getElementById('sugestoesClientesDiv');
            const clienteSelecionadoDataInput = document.getElementById('clienteSelecionadoDataInput');

            let debounceTimer;

        nomeCliente.addEventListener('input', function() {
        const termo = this.value.trim();

        // Limpa o timer anterior para evitar múltiplas requisições rápidas (debounce)
        clearTimeout(debounceTimer);

        if (termo.length < 2) { // Começa a buscar após 2 caracteres, por exemplo
            sugestoesClientesDiv.innerHTML = ''; // Limpa sugestões se o termo for muito curto
            clienteSelecionadoDataInput.value = ''; // Limpa dados do cliente selecionado
            return;
        }

        // Define um novo timer
        debounceTimer = setTimeout(() => {
            fetch(`/cliente?termo=${encodeURIComponent(termo)}`)
                .then(response => {
                    if (!response.ok) {
                        throw new Error(`Erro HTTP: ${response.status}`);
                    }
                    return response.json();
                })
                .then(clientes => {
                    exibirSugestoes(clientes);
                })
                .catch(error => {
                    console.error('Erro ao buscar clientes:', error);
                    sugestoesClientesDiv.innerHTML = '<div class="sugestao-item">Erro ao buscar.</div>';
                });
        }, 300); // Epera de 300ms antes de fazer a requisição
    });

    function exibirSugestoes(clientes) {
        sugestoesClientesDiv.innerHTML = ''; // Limpa sugestões anteriores
        if (clientes.length === 0) {
            sugestoesClienteDiv.innerHTML = '<div class="sugestao-item">Nenhum cliente encontrado.</div>';
            return;
        }

                clientes.forEach(cliente => {
            const itemLink = document.createElement('a'); // Usar <a> para estilo Bootstrap
            itemLink.href = "#"; // Para comportamento de link
            itemLink.classList.add('list-group-item', 'list-group-item-action'); // Classes Bootstrap
            
            // Propriedades retornadas pela API
            itemLink.textContent = `${cliente.nome} (ID: ${cliente._id})`; 
            
            itemLink.dataset.clienteData = JSON.stringify(cliente);

            itemLink.addEventListener('click', function(e) {
                e.preventDefault(); // Prevenir navegação do link
                const clienteDataString = this.dataset.clienteData;
                const clienteSelecionado = JSON.parse(clienteDataString);

                // Preencher o input visível
                nomeClienteInput.value = clienteSelecionado.nome; 
                
                // Preencher o campo oculto com o ID do cliente
                clienteIdInput.value = clienteSelecionado._id; 
                
                // Preencher o campo oculto com os dados JSON completos do cliente
                clienteSelecionadoDataInput.value = clienteDataString; 

                sugestoesClientesDiv.innerHTML = '';
                sugestoesClientesDiv.style.display = 'none';
            });
            sugestoesClientesDiv.appendChild(itemLink);
        });
        sugestoesClientesDiv.style.display = 'block';
    }


            // Fechar sugestões se clicar fora do campo
            document.addEventListener('click', function(e) {
                if (!sugestoesClientesDiv.contains(e.target) && e.target !== nomeClienteInput) {
                    sugestoesClientesDiv.style.display = 'none';
                }
            });});
