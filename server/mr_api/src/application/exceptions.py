from dataclasses import dataclass

from fastapi import HTTPException

from src.application.constants import PremiumSubscriptionRequiredTypes


# Различные ошибки, связанные с валидацией данных
@dataclass
class EmptyFieldException(HTTPException):
    field_name: str
    status_code: int = 422
    detail: str | None = None

    def __post_init__(self) -> None:
        self.detail = f"Поле '{self.field_name}' не может быть пустым."


@dataclass
class InvalidFileFormatException(HTTPException):
    status_code: int = 422
    detail: str = "Формат не допустим."


@dataclass
class FileEmptyException(HTTPException):
    status_code: int = 422
    detail: str = "Файл пустой."


@dataclass
class PremiumSubscriptionRequiredException(HTTPException):
    type: str
    allowed_num_rows: int | None = None
    status_code: int = 403
    detail: str | None = None

    def __post_init__(self) -> None:
        if self.type == PremiumSubscriptionRequiredTypes.MAX_ROWS.value:
            self.detail = (
                "Нужна \"Премиум\" подписка аккаунт, "
                f"чтобы загрузить более {self.allowed_num_rows} строк отзывов."
            )
        elif self.type == PremiumSubscriptionRequiredTypes.DOWNLOAD.value:
            self.detail = (
                "Нужна \"Премиум\" подписка аккаунт, "
                "чтобы скачать результат анализа."
            )
        else:
            return None


# Ошибки, связанные с пользователем
@dataclass
class UserExistsException(HTTPException):
    email: str
    status_code: int = 409
    detail: str | None = None

    def __post_init__(self) -> None:
        self.detail = f"Пользователь с почтой '{self.email}' уже существует."


@dataclass
class InvalidCredentialsException(HTTPException):
    detail: str = "Неверная почта или пароль."
    status_code: int = 409


@dataclass
class UserNotFoundException(HTTPException):
    detail: str = "Пользователь не найден."
    status_code: int = 404


@dataclass
class NotAuthenticatedException(HTTPException):
    detail: str = "Вы не аутентифицированы."
    status_code: int = 401


@dataclass
class AlreadyAuthenticatedException(HTTPException):
    detail: str = "Вы уже авторизованы."
    status_code: int = 401


@dataclass
class NotAdminRoleException(HTTPException):
    detail: str = "Нет прав администратора"
    status_code: int = 403


# Ошибки связанные с отзывами и анализом
@dataclass
class TooManyTestReviewsException(HTTPException):
    detail: str = (
        "Превышено максимальное количество "
        "тестовых отзывов (максимум 10 штук)."
    )
    status_code: int = 403


@dataclass
class ReviewsProcessingException(HTTPException):
    detail: str = "Ошибка при обработке отзывов."
    status_code: int = 500


@dataclass
class AnalyzeServiceException(HTTPException):
    detail: str = "Произошла ошибка в сервисе анализа."
    status_code: int = 500


@dataclass
class AnalyzeNotFoundException(HTTPException):
    status_code: int = 404
    detail: str = "Результат анализа не найден."


# Ошибки связанные с обратной связью
@dataclass
class FeedbackNotFound(HTTPException):
    status_code: int = 404
    detail: str = "Запись обратной связи не найдена."


@dataclass
class FeedbackAlreadyAnsweredException(HTTPException):
    status_code: int = 409
    detail: str = "Запись обратной связи уже отвечена."
