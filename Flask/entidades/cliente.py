#Classe cliente com seu construtor e dados necessários
import re

class Cliente:
    
    def __init__(self, nome, cpf, cep, endereco, complemento, email, telefone, celular):
        self.nome = nome,
        self.cpf = cpf,
        self.cep = cep,
        self.endereco = endereco,
        self.complemento = complemento,
        self.email = email,
        self.telefone = telefone,
        self.celular = celular

    def __post_init__(self):
        # Valida o CPF do cliente
        if not self._validar_cpf(self.cpf):
            raise ValueError("CPF inválido")
        if not self.validar_email(self.email):
             raise ValueError("Email inválido")

    def validar_email(self, email: str) -> bool:
        # Validação do email
        pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
        return bool(re.match(pattern, email))
    
    def _validar_cpf(self, cpf: str) -> bool:
        # Implementar lógica de validação de CPF (simplificada aqui)
        cpf_numerico = re.sub(r'[^0-9]', '', cpf)
        return len(cpf_numerico) == 11 # Exemplo muito básico