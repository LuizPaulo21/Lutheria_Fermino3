from abc import ABC, abstractmethod
from typing import List

class IprodutoRepository(ABC):
    @abstractmethod
    def get_produto(self, id: int) -> dict:
        pass
        
    @abstractmethod
    def create_produto(self, produto: dict) -> dict:
        pass

    @abstractmethod
    def update_produto(self, id: int, produto: dict) -> dict:
        pass

    @abstractmethod
    def delete_produto(self, id: str) -> None:
        pass