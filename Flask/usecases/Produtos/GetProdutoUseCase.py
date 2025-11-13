from Flask.repositories import produtoRepository

class GetProdutoUseCase:
    def __init__(self, produto_repository):
        self.produto_repository = produto_repository

    def execute(self, produto_id):
        return self.produto_repository.get_by_id(produto_id)