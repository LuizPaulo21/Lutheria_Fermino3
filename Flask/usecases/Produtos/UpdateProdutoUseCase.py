from Flask.repositories import produtoRepository

class UpdateProdutoUseCase:
    def __init__(self, produto_repository):
        self.produto_repository = produto_repository

    def execute(self, produto_id, nome, descricao, preco):
        # Validate input
        if not nome or not descricao or preco <= 0:
            raise ValueError("Invalid input data")

        # Update product in the repository
        produto = self.produto_repository.get_by_id(produto_id)
        if not produto:
            raise ValueError("Product not found")

        produto.nome = nome
        produto.descricao = descricao
        produto.preco = preco

        self.produto_repository.update(produto)