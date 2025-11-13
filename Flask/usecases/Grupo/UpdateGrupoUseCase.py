class UpdateGrupoUseCase:
    def __init__(self, grupo_repository):
        self.grupo_repository = grupo_repository

    def execute(self, id, nome, descricao):
        # Validate input
        if not id or not nome or not descricao:
            raise ValueError("ID, Nome and Descricao are required")

        # Update the group in the repository
        grupo = self.grupo_repository.update(id, nome, descricao)
        return grupo