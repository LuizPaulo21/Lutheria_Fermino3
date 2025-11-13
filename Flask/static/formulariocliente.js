        document.addEventListener('DOMContentLoaded', function () {
            const tipoPessoaFisicaRadio = document.getElementById('tipoPessoaFisica');
            const tipoPessoaJuridicaRadio = document.getElementById('tipoPessoaJuridica');
            const dadosPessoaFisicaDiv = document.getElementById('dadosPessoaFisica');
            const dadosPessoaJuridicaDiv = document.getElementById('dadosPessoaJuridica');

            // Campos Pessoa Física
            const cpfInput = document.getElementById('cpf');
            const nomeCompletoInput = document.getElementById('nomeCompleto');

            // Campos Pessoa Jurídica
            const cnpjInput = document.getElementById('cnpj');
            const razaoSocialInput = document.getElementById('razaoSocial');
            const nomeFantasiaInput = document.getElementById('nomeFantasia');

            // Função para alternar entre os campos de Pessoa Física e Pessoa Jurídica
            function toggleCamposCliente() {
                if (tipoPessoaFisicaRadio.checked) {
                    dadosPessoaFisicaDiv.style.display = 'block';
                    dadosPessoaJuridicaDiv.style.display = 'none';
                    // Limpa e desabilita campos PJ se necessário
                    cnpjInput.value = '';
                    razaoSocialInput.value = '';
                    nomeFantasiaInput.value = '';
                } else {
                    dadosPessoaFisicaDiv.style.display = 'none';
                    dadosPessoaJuridicaDiv.style.display = 'block';
                    // Limpa e desabilita campos PF se necessário
                    cpfInput.value = '';
                    nomeCompletoInput.value = '';
                }
            }

            tipoPessoaFisicaRadio.addEventListener('change', toggleCamposCliente);
            tipoPessoaJuridicaRadio.addEventListener('change', toggleCamposCliente);

            // Inicializa a visibilidade correta
            toggleCamposCliente();
        });