class UpdatePedidoUseCase:
    def __init__(self, pedido_repository):
        self.pedido_repository = pedido_repository

    def execute(self, pedido_id, pedido_data):
        # Validate the input data
        if not pedido_id or not pedido_data:
            raise ValueError("Pedido ID and data are required")

        # Update the pedido in the repository
        updated_pedido = self.pedido_repository.update(pedido_id, pedido_data)

        return updated_pedido