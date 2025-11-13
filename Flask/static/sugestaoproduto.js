       document.addEventListener('DOMContentLoaded', function () {

        //DIV de sugestões
        const sugestoesProdutoDiv = document.getElementById('sugestoesProduto');
        const nomeProdutoInput = document.getElementById('nomeProdutoServico');
        const produtoSelecionado = document.getElementById('produtoSelecionadoDataInput');
        const produtoIdInput = document.getElementById('produtoId');

    
        let debounceTimer;
        nomeProdutoInput.addEventListener('input', function() {
        const termo = this.value.trim();

        // Limpa o timer anterior para evitar múltiplas requisições rápidas (debounce)
        clearTimeout(debounceTimer);

        if (termo.length < 2) { // Começa a buscar após 2 caracteres, por exemplo
            sugestoesProdutoDiv.innerHTML = ''; // Limpa sugestões se o termo for muito curto
            return;
        }

        // Define um novo timer
        debounceTimer = setTimeout(() => {
            fetch(`/produto?termo=${encodeURIComponent(termo)}`)
                .then(response => {
                    if (!response.ok) {
                        throw new Error(`Erro HTTP: ${response.status}`);
                    }
                    return response.json();
                })
                .then(produtos => {
                    exibirSugestoes(produtos);
                })
                .catch(error => {
                    console.error('Erro ao buscar produtos:', error);
                    sugestoesProdutoDiv.innerHTML = '<div class="sugestao-item">Erro ao buscar.</div>';
                });
        }, 300); // Epera de 300ms antes de fazer a requisição
    });

    function exibirSugestoes(produtos) {
        sugestoesProdutoDiv.innerHTML = ''; // Limpa sugestões anteriores
        if (produtos.length === 0) {
            sugestoesProdutoDiv.innerHTML = '<div class="sugestao-item">Nenhum produto encontrado.</div>';
            return;
        }

            produtos.forEach(produto => {
            const itemLink = document.createElement('a'); // Usar <a> para estilo Bootstrap
            itemLink.href = "#"; // Para comportamento de link
            itemLink.classList.add('list-group-item', 'list-group-item-action'); // Classes Bootstrap
            
            // Propriedades retornadas pela API
            itemLink.textContent = `${produto.nome} (ID: ${produto._id})`; 
            
            itemLink.dataset.produtoData = JSON.stringify(produto);

            itemLink.addEventListener('click', function(e) {
                e.preventDefault(); // Prevenir navegação do link
                const stringProduto = this.dataset.produtoData;
                const produtoSelecionar = JSON.parse(stringProduto);

                // Preencher o input visível
                nomeProdutoInput.value = produtoSelecionar.nome; 
                
                // Preencher o campo oculto com o ID do cliente
                produtoIdInput.value = produtoSelecionar._id; 
                
                // Preencher o campo oculto com os dados JSON completos do produto
                produtoSelecionado.value = stringProduto; 

                sugestoesProdutoDiv.innerHTML = '';
                sugestoesProdutoDiv.style.display = 'none';
            });
            sugestoesProdutoDiv.appendChild(itemLink);
        });
        sugestoesProdutoDiv.style.display = 'block';
    }
            // Fechar sugestões se clicar fora do campo
            document.addEventListener('click', function(e) {
                if (!sugestoesProdutoDiv.contains(e.target) && e.target !== nomeProdutoInput) {
                    sugestoesProdutoDiv.style.display = 'none';
                }
            });
        });
