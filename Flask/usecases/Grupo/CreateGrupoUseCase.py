class CreateGrupoUseCase:
    def __init__(self, grupo_repository):
        self.grupo_repository = grupo_repository

    def execute(self, grupo_data):
        # Validate the input data
        if not grupo_data.get('name'):
            raise ValueError("Group name is required")
        if not grupo_data.get('description'):
            raise ValueError("Group description is required")

        # Create the group using the repository
        grupo = self.grupo_repository.create(grupo_data)
        return grupo