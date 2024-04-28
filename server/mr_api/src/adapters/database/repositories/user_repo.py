from dataclasses import dataclass

import sqlalchemy as sqla

from src.adapters.api.auth import schemas as auth_schemas
from src.adapters.database import tables
from src.adapters.database.repositories.base_repo import SABaseRepository
from src.application.user import entities, interfaces


@dataclass
class UserRepository(SABaseRepository, interfaces.IUserRepository):
    """
    Репозиторий для работы с пользователями в базе данных.
    """

    async def create_user(
        self,
        user: auth_schemas.CreateUser
    ) -> entities.User:
        """
        Создает нового пользователя в базе данных.

        :param user: Данные нового пользователя для создания.

        :return: Созданный пользователь.
        """
        table: sqla.Table = tables.users

        query: sqla.Insert = (
            sqla.insert(
                table
            )
            .values(
                **user.dict()
            )
            .returning(
                table
            )
        )

        user = self.session.execute(query).mappings().one()
        self.session.commit()
        return entities.User(**user)

    async def get_user_by_email(self, email: str) -> entities.User | None:
        """
        Получает пользователя из базы данных по электронной почте.

        :param email: Адрес электронной почты пользователя.

        :return: Пользователь с указанным адресом электронной почты,
        если найден, в противном случае None.
        """
        table: sqla.Table = tables.users

        query: sqla.Select = (
            sqla.select(
                table
            )
            .filter(
                table.c.email == email
            )
        )

        user = self.session.execute(query).mappings().one_or_none()

        if user:
            return entities.User(**user)
        return None

    async def get_user_info_by_id(
        self,
        user_id: int
    ) -> entities.UserInfo | None:
        """
        Получает информцию (роль, премиум)
        о пользователе из базы данных по его id.

        :param user_id: ID пользователя.

        :return: UserInfo | None.
        """
        table: sqla.Table = tables.users

        query: sqla.Select = (
            sqla.select(
                table.c.role,
                table.c.is_premium
            )
            .filter(
                table.c.id == user_id
            )
        )

        user = self.session.execute(query).mappings().one_or_none()

        if user:
            return entities.UserInfo(**user)
        return None

    async def get_user_by_id(self, user_id: int) -> entities.User | None:
        """
        Получает пользователя из базы данных по его id.

        :param user_id: ID пользователя.

        :return: Пользователь с указанным id,
        если найден, в противном случае None.
        """

        table: sqla.Table = tables.users

        query: sqla.Select = (
            sqla.select(
                table
            )
            .filter(
                table.c.id == user_id
            )
        )

        user = self.session.execute(query).mappings().one_or_none()

        if user:
            return entities.User(**user)
        return None

    async def get_all_users(self) -> list[entities.User | None]:
        """
        Получает список всех пользователей.

        :return: Список объектов пользователей или пустой список,
        если пользователей нет.
        """

        table: sqla.Table = tables.users

        query: sqla.Select = (
            sqla.select(
                table
            ).order_by(table.c.id.desc())
        )

        users = self.session.execute(query).mappings().all()

        if users:
            return [entities.User(**row) for row in users]
        return []

    async def update_user_by_id(
        self,
        user: entities.UserUpdate
    ) -> entities.User:
        """
        Обновляет информацию о пользователе в базе данных.

        :param user: Объект,
        содержащий обновленные данные пользователя.

        return: Обновленный объект пользователя.
        """

        table: sqla.Table = tables.users

        update_fields = {}

        # Проверяем каждое поле объекта user и,
        # если оно не пустое,
        # добавляем его в словарь update_fields
        if user.first_name:
            update_fields[table.c.first_name] = user.first_name
        if user.last_name:
            update_fields[table.c.last_name] = user.last_name
        if user.email:
            update_fields[table.c.email] = user.email
        if user.password:
            update_fields[table.c.password] = user.password

        query: sqla.Update = (
            sqla.update(
                table
            )
            .filter(
                table.c.id == user.id
            )
            .values(
                update_fields
            )
            .returning(
                table.c.id,
                table.c.dt,
                table.c.first_name,
                table.c.last_name,
                table.c.email,
                table.c.password,
                table.c.role,
                table.c.is_premium
            )
        )

        user = self.session.execute(query).mappings().one()
        self.session.commit()
        return entities.User(**user)

    async def delete_user_by_id(
        self,
        user_id: int
    ) -> int:
        """
        Удаляет пользователя из базы данных.

        :param user_id: int: Идентификатор пользователя,
        :return: int: Идентификатор удаленного пользователя.
        """

        table: sqla.Table = tables.users

        query: sqla.Delete = (
            sqla.delete(
                table
            )
            .filter(
                table.c.id == user_id
            )
        )

        self.session.execute(query)
        self.session.commit()
        return user_id
