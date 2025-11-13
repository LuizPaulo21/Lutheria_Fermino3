from Flask.repositories import produtoRepository

class CreateProdutoUseCase:
    def __init__(self, produto_repository):
        self.produto_repository = produto_repository

    def execute(self, produto_data):
        # Validate the input data
        if not produto_data.get('name'):
            raise ValueError("Product name is required")
        if not isinstance(produto_data.get('price'), (int, float)):
            raise ValueError("Product price must be a number")

        # Create the product using the repository
        produto = self.produto_repository.create(produto_data)
        return produto