from dataclasses import asdict, dataclass

from async_lru import alru_cache

from src.adapters.api.data import schemas
from src.application import exceptions
from src.application.constants import UserRole
from src.application.data import interfaces as data_interfaces
from src.application.user import interfaces as user_interfaces


@dataclass
class DataService:
    """
    Сервис для сбора различных данных с проанализированных отзывов.
    """

    data_repo: data_interfaces.IDataRepository
    user_repo: user_interfaces.IUserRepository

    def __hash__(self) -> int:
        return hash(id(self))

    @alru_cache
    async def get_all_stopwords(
        self,
        user_id: int
    ) -> list[schemas.StopwordResponse]:
        """
        Возвращает список стоп-слов.

        :param user_id: id пользователя.

        :return: Список стоп-слов.
        """

        # Проверка на роль администратора
        user = await self.user_repo.get_user_info_by_id(user_id)

        if user.role != UserRole.ADMIN.value:
            raise exceptions.NotAdminRoleException

        stopwords = await self.data_repo.get_all_stopwords()

        return [
            schemas.StopwordResponse(**asdict(stopword))
            for stopword in stopwords
        ]

    async def set_stopword_is_use(
        self,
        stopword_id: int,
        user_id: int
    ) -> dict[str, str]:
        """
        Обновляет стоп-слово.

        :param stopword_id: id стоп-слова.
        :param user_id: id пользователя.

        :return: Сообщение.
        """

        # Проверка на роль администратора
        user = await self.user_repo.get_user_info_by_id(user_id)

        if user.role != UserRole.ADMIN.value:
            raise exceptions.NotAdminRoleException

        await self.data_repo.update_stopword_is_use(stopword_id)

        return {"message": "Стоп-слово обновлено"}

    async def delete_stopword(
        self,
        stopword_id: int,
        user_id: int
    ) -> dict[str, str]:
        """
        Удаляет стоп-слово.

        :param stopword_id: id стоп-слова.
        :param user_id: id пользователя.

        :return: Сообщение.
        """

        # Проверка на роль администратора
        user = await self.user_repo.get_user_info_by_id(user_id)

        if user.role != UserRole.ADMIN.value:
            raise exceptions.NotAdminRoleException

        await self.data_repo.delete_stopword(stopword_id)

        return {"message": "Стоп-слово удалено"}
