from abc import ABC, abstractmethod
from typing import List

class iPedidoRepository(ABC):

    @abstractmethod
    def get_pedido(self, id: int) -> dict:
        pass
    
    @abstractmethod
    def create_pedido(self, pedido: dict) -> dict:
        pass

    @abstractmethod
    def update_pedido(self, id: int, pedido: dict) -> dict:
        pass

    @abstractmethod
    def delete_pedido(self, id: int) -> None:
        pass