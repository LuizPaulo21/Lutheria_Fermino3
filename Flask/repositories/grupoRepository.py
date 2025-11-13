from abc import ABC, abstractmethod
from typing import List


class IgrupoRepository(ABC):

    @abstractmethod
    def get_grupo(self, id: int) -> dict:
        pass
        
    @abstractmethod
    def create_grupo(self, grupo: dict) -> dict:
        pass

    @abstractmethod
    def update_grupo(self, id: int, grupo: dict) -> dict:
        pass

    @abstractmethod
    def delete_grupo(self, id: int) -> None:
        pass