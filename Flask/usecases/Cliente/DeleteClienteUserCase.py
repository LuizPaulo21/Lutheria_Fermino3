class DeleteClienteUserCase:
    def __init__(self, cliente_repository):
        self.cliente_repository = cliente_repository

    def execute(self, cliente_id):
        # Validate the input
        if not cliente_id:
            raise ValueError("Cliente ID is required")

        # Call the repository to delete the cliente
        self.cliente_repository.delete(cliente_id)