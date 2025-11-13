class GetClienteUseCase:
    def __init__(self, cliente_repository):
        self.cliente_repository = cliente_repository

    def execute(self, cliente_id):
        return self.cliente_repository.get(cliente_id)