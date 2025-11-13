class DeleteGrupoUseCase:
    def __init__(self, grupo_repository):
        self.grupo_repository = grupo_repository

    def execute(self, grupo_id):
        # Validate the input
        if not isinstance(grupo_id, int) or grupo_id <= 0:
            raise ValueError("Invalid Grupo ID")

        # Call the repository to delete the Grupo
        self.grupo_repository.delete(grupo_id)