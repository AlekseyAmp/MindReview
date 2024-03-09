import smtplib
from dataclasses import dataclass
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from src.adapters.email.settings import settings
from src.application.feedback import interfaces


@dataclass
class MailSender(interfaces.IMailSender):
    """
    Класс для работы с электронной почтой.
    """

    def send_mail(
        self,
        title: str,
        message: str,
        to_address: str
    ) -> str:
        """
        Отправляет письмо на указанный адрес.

        :param title: Заголовок письма.
        :param message: Текст письма.
        :param from_address: Адрес отправителя.
        :param to_address: Адрес получателя.

        :return: Строка с информацией о результате отправки письма.
        """

        try:
            msg = MIMEMultipart()
            msg['From'] = settings.EMAIL_USERNAME
            msg['To'] = to_address
            msg['Subject'] = title

            msg.attach(MIMEText(message, 'plain'))

            with smtplib.SMTP(
                settings.SMTP_SERVER,
                settings.SMTP_PORT
            ) as server:
                server.starttls()
                server.login(
                    settings.EMAIL_USERNAME,
                    settings.EMAIL_PASSWORD
                )
                server.send_message(msg)

            return "Письмо успешно отправлено"
        except Exception as e:
            return f"Ошибка при отправке письма: {str(e)}"
