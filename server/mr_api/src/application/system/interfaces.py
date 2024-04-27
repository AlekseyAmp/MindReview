from abc import ABC, abstractmethod

from src.application.system import entities


class ISystemRepository(ABC):

    @abstractmethod
    async def save_log(
        self,
        feedback: entities.LogInput
    ) -> int:
        pass

    @abstractmethod
    async def get_all_logs(
        self
    ) -> list[entities.LogReturn | None]:
        pass
