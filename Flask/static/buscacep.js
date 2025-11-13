//Busca de endereço por CEP
            const cepInput = document.getElementById('cep');
            if (cepInput) {
                cepInput.addEventListener('blur', function() {
                    const cep = this.value.replace(/\D/g, ''); // Remove não numéricos
                    if (cep.length === 8) {
                        fetch(`https://viacep.com.br/ws/${cep}/json/`)
                         .then(response => response.json())
                         .then(data => {
                             if (!data.erro) {
                                 document.getElementById('logradouro').value = data.logradouro;
                                 document.getElementById('bairro').value = data.bairro;
                                 document.getElementById('cidade').value = data.localidade;
                                 document.getElementById('uf').value = data.uf;
                             } else {
                                 alert('CEP não encontrado.');
                             }
                         })
                         .catch(error => console.error('Erro ao buscar CEP:', error));
                    }
                });
            }