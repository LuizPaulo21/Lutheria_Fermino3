from Flask.repositories import clienteRepository 

class CreateClienteUseCase:
    def __init__(self, cliente_repository: clienteRepository):
        
        self.cliente_repository = cliente_repository

    def execute(self, cliente_data: dict) -> dict:
        return self.cliente_repository.create_cliente(cliente_data)

