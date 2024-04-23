from dataclasses import asdict, dataclass

from async_lru import alru_cache

from src.adapters.api.feedback import schemas
from src.adapters.email.settings import settings as email_settings
from src.adapters.logger.settings import logger
from src.application import exceptions
from src.application.constants import TimeConstants, UserRole
from src.application.feedback import entities
from src.application.feedback import interfaces as feedback_interfaces
from src.application.user import interfaces as user_interfaces
from src.application.utils import (
    datetime_to_json,
    get_current_dt,
    validate_non_empty_fields,
)


@dataclass
class FeedbackService:
    """
    Сервис для работы с обратной связью.
    """

    feedback_repo: feedback_interfaces.IFeedbackRepository
    user_repo: user_interfaces.IUserRepository
    mail_sender: feedback_interfaces.IMailSender

    def __hash__(self) -> int:
        return hash(id(self))

    async def send_feedback(
        self,
        send_feedback: schemas.SendFeedback,
        user_id: int
    ) -> dict[str, str]:
        """
        Сохраняет обратную связь от пользователя.

        :param user_id: Идентификатор пользователя.
        :param send_feedback: Объект обратной связи.

        :return: Объект обратной связи.
        """

        empty_field = validate_non_empty_fields(send_feedback.dict())
        if empty_field:
            raise exceptions.EmptyFieldException(empty_field)

        feedback = entities.FeedbackInput(
            user_id=user_id,
            response_dt=None,
            message=send_feedback.message,
            response=None,
            sender_email=send_feedback.email,
            recipient_email=email_settings.EMAIL_USERNAME
        )

        feedback_data = await self.feedback_repo.save_feedback(
            feedback
        )

        logger.info(
            (
                "Письмо от пользователя направлено к службе поддержки. "
                "(feedback_id: %s, "
                "sender_email: %s, "
                "recipient_email: %s, "
                "user_id: %s)"
            ),
            feedback_data.id,
            feedback_data.sender_email,
            feedback_data.recipient_email,
            user_id
        )

        # Конвертация даты обратной связи в строковый формат
        feedback_data.dt = datetime_to_json(feedback_data.dt)

        return {
            "message": (
                "Мы получили ваше письмо! "
                "Оператор скоро ответит вам на указанную почту."
            )
        }

    async def reply_feedback(
        self,
        reply_feedback: schemas.ReplyFeedback,
        user_id: int
    ) -> dict[str, str]:
        """
        Отвечает на обратную связь от пользователя,
        высылает письмо на почту.

        :param reply_feedback: Объект обратной связи.

        :return: Объект обратной связи.
        """

        empty_field = validate_non_empty_fields(reply_feedback.dict())
        if empty_field:
            raise exceptions.EmptyFieldException(empty_field)

        # Проверка на роль администратора
        user = await self.user_repo.get_user_info_by_id(user_id)

        if user.role != UserRole.ADMIN.value:
            raise exceptions.NotAdminRoleException

        # Проверка на наличие обратной связи
        feedback = await self.feedback_repo.get_feedback_by_id(
            reply_feedback.feedback_id
        )

        if not feedback:
            return exceptions.FeedbackNotFound

        if feedback.response:
            raise exceptions.FeedbackAlreadyAnsweredException

        # Обновляем запись в БД
        feedback_data = await self.feedback_repo.update_feedback(
            entities.FeedbackUpdate(
                id=reply_feedback.feedback_id,
                response_dt=get_current_dt(TimeConstants.DEFAULT_TIMEZONE),
                response=reply_feedback.response,
            )
        )

        # В этом случае мы отправляем письмо от службы поддержки пользователю,
        # поэтому роли адресов меняются местами: адрес получателя
        # - адрес отправителя и наоборот.
        recipient_email = feedback_data.sender_email
        sender_email = feedback.recipient_email

        # Отправляем письмо на почту пользователя
        self.mail_sender.send_mail(
            title="MindReview: Получено письмо от службы поддержки",
            message=(
                f"Ваше письмо: {feedback_data.message}.\n"
                f"Ответ от службы поддержки: {reply_feedback.response}"
            ),
            to_address=recipient_email
        )
        logger.info(
            (
                "Письмо от службы поддержки отправлено на почту. "
                "(feedback_id: %s, "
                "sender_email: %s, "
                "recipient_email: %s, "
                "user_id: %s)"
            ),
            feedback_data.id,
            sender_email,
            recipient_email,
            user_id
        ),

        return {"message": f"Письмо отправлено на почту {recipient_email}"}

    @alru_cache
    async def get_all_feedbacks(
        self,
        user_id: int
    ) -> schemas.FeedbacksResponse:
        """
        Получает все обратные связи, как отвеченные, так и неотвеченные,
        и возвращает их в виде словаря с ключами "answered" и "unanswered".

        :param user_id: Идентификатор пользователя.

        :return: FeedbacksResponse.
        """

        user = await self.user_repo.get_user_info_by_id(user_id)

        if user.role != UserRole.ADMIN.value:
            raise exceptions.NotAdminRoleException

        all_answered_feedbacks = await self.feedback_repo.\
            get_all_answered_feedbacks()
        all_unanswered_feedbacks = await self.feedback_repo.\
            get_all_unanswered_feedbacks()

        # Преобразование даты dt
        for feedback in all_answered_feedbacks:
            feedback.dt = datetime_to_json(feedback.dt)
            feedback.response_dt = datetime_to_json(feedback.response_dt)

        for feedback in all_unanswered_feedbacks:
            feedback.dt = datetime_to_json(feedback.dt)

        answered_feedbacks = [
            schemas.FeedbackResponse(**asdict(answered_feedback))
            for answered_feedback in all_answered_feedbacks
        ]

        # Переворачиваем, старые в начале, новые в конце
        unanswered_feedbacks = [
            schemas.FeedbackResponse(**asdict(unanswered_feedback))
            for unanswered_feedback in all_unanswered_feedbacks
        ][::-1]

        return schemas.FeedbacksResponse(
            answered=answered_feedbacks,
            unanswered=unanswered_feedbacks
        )
