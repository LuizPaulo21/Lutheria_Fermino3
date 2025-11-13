from flask import render_template

class CreatePedidoUseCase:
    def __init__(self, pedido_repository):
        self.pedido_repository = pedido_repository

    def execute(self, pedido_data):
        if pedido_data is None:
            mensagem = "Erro: Dados do pedido não podem ser nulos."
            return render_template('cadastro_pedido.html', msg=mensagem)
        # Se for um pedido de conserto, chama o método create do pedido_repository
        elif pedido_data:
            self.pedido_repository.create_pedido(pedido_data)
        # Se for um pedido de venda, chama o método create do pedido_repository, sem passar o prazo de conserto
        else:
            dados_pedido = {
                "data_pedido": pedido_data.data_pedido,
                "tipo_pedido": pedido_data.tipo_pedido,
                "cliente_id": pedido_data.cliente_id,
                "produto_id": pedido_data.produto_id,
                "quantidade": pedido_data.quantidade,
                "valor_total": pedido_data.valor_total
            }
            self.pedido_repository.create_pedido(dados_pedido)
            return render_template('cadastro_pedido.html', msg="Pedido cadastrado com sucesso!")