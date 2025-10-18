from abc import ABC, abstractmethod
from typing import Optional
from models.widget import WidgetRequest

class RequestSource(ABC):
    @abstractmethod
    def get_next_request(self) -> Optional[WidgetRequest]:
        ...
