class UpdateClienteUseCase:
    def __init__(self, cliente_repository):
        self.cliente_repository = cliente_repository

    def execute(self, cliente_id, updated_data):
        # Faz a validação dos dados de entrada
        if not updated_data.get('name') or not updated_data.get('email'):
            raise ValueError("Name and email are required fields")

        # Atualiza o cliente usando o repositório
        updated_cliente = self.cliente_repository.update(cliente_id, updated_data)

        return updated_cliente