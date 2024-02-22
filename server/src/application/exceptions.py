from dataclasses import dataclass

from fastapi import HTTPException


@dataclass
class EmptyFieldException(HTTPException):
    field_name: str

    def __post_init__(self) -> None:
        detail = f"Поле '{self.field_name}' не может быть пустым."
        super().__init__(status_code=422, detail=detail)


@dataclass
class UserExistsException(HTTPException):
    email: str

    def __post_init__(self) -> None:
        detail = f"Пользователь с почтой '{self.email}' уже существует."
        super().__init__(status_code=409, detail=detail)


@dataclass
class UserNotFoundException(HTTPException):
    def __post_init__(self) -> None:
        detail = "Пользователь не найден."
        super().__init__(status_code=404, detail=detail)


@dataclass
class AlreadyAuthenticatedException(HTTPException):
    def __post_init__(self) -> None:
        detail = "Вы уже авторизованы."
        super().__init__(status_code=401, detail=detail)


@dataclass
class InvalidCredentialsException(HTTPException):
    def __post_init__(self) -> None:
        detail = "Неверная почта или пароль."
        super().__init__(status_code=409, detail=detail)
