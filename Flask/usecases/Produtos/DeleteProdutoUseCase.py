from Flask.repositories import produtoRepository 

class DeleteProdutoUseCase:
    def __init__(self, produto_repository):
        self.produto_repository = produto_repository

    def execute(self, id):
        return self.produto_Repository.delete_produto(id)