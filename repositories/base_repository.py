"""Interface abstraite commune à tous les repositories.

Toute future implémentation (SQLiteRepository, ApiRepository pour la
version SaaS) doit respecter ce contrat. Les services et les écrans ne
dépendent jamais de SQLite directement : ils dépendent de cette interface.
"""

from abc import ABC, abstractmethod
from typing import Any, List, Optional


class BaseRepository(ABC):
    @abstractmethod
    def create(self, entity: Any) -> Any:
        ...

    @abstractmethod
    def get_by_id(self, entity_id: str) -> Optional[Any]:
        ...

    @abstractmethod
    def list_all(self) -> List[Any]:
        ...

    @abstractmethod
    def update(self, entity: Any) -> Any:
        ...

    @abstractmethod
    def delete(self, entity_id: str) -> bool:
        ...
