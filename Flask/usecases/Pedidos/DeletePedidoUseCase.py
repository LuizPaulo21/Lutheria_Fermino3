class DeletePedidoUserCase:
    def __init__(self, pedido_repository):
        self.pedido_repository = pedido_repository

    def execute(self, pedido_id):
        # Validate the pedido_id
        if not pedido_id:
            raise ValueError("Pedido ID is required")

        # Delete the pedido
        deleted_pedido = self.pedido_repository.delete(pedido_id)

        # Check if the pedido was deleted successfully
        if not deleted_pedido:
            raise Exception("Pedido not found or could not be deleted")

        return deleted_pedido