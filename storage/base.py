from abc import ABC, abstractmethod
from models.widget import WidgetRequest

class WidgetStore(ABC):
    @abstractmethod
    def create(self, req: WidgetRequest) -> None:
        ...
