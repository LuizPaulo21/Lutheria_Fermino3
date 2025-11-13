class GetPedidoUseCase:
    def __init__(self, pedido_repository):
        self.pedido_repository = pedido_repository

    def execute(self, pedido_id):
        return self.pedido_repository.get_pedido(pedido_id)