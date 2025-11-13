class GetGrupoUseCase:
    def __init__(self, grupo_repository):
        self.grupo_repository = grupo_repository

    def execute(self, id):
        grupo = self.grupo_repository.get_by_id(id)
        if not grupo:
            raise ValueError("Grupo not found")
        return grupo