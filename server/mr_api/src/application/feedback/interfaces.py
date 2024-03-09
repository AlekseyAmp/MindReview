from abc import ABC, abstractmethod

from src.application.feedback import entities


class IFeedbackRepository(ABC):

    @abstractmethod
    async def save_feedback(
        self,
        feedback: entities.FeedbackInput
    ) -> entities.FeedbackReturn:
        pass

    @abstractmethod
    async def update_feedback(
        self,
        feedback: entities.FeedbackUpdate
    ) -> entities.FeedbackReturn:
        pass

    @abstractmethod
    async def get_feedback_by_id(
        self,
        feedback_id
    ) -> entities.FeedbackReturn | None:
        pass

    @abstractmethod
    async def get_all_answered_feedbacks(
        self
    ) -> list[entities.FeedbackReturn | None]:
        pass

    @abstractmethod
    async def get_all_unanswered_feedbacks(
        self
    ) -> list[entities.FeedbackReturn | None]:
        pass


class IMailSender(ABC):

    @abstractmethod
    def send_mail(self, title: str, message: str, to_address: str) -> str:
        pass
