import asyncio
from typing import Generator

import argostranslate.package
import nltk
from nltk.corpus import stopwords
from pymorphy3 import MorphAnalyzer
from sqlalchemy.orm import Session
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

from src.adapters.database import repositories
from src.adapters.database.sa_session import get_session
from src.adapters.nlp.nlp import NLPService
from src.adapters.rpc import AnalyzeProducer, RabbitMQManager, ReviewConsumer
from src.application.analyze.services import AnalyzeService
from src.application.collection.services import CollectionService


class DB:
    session: Session = get_session()

    analyze_repo = repositories.AnalyzeRepository(session)
    data_repo = repositories.DataRepository(session)


class RabbitMQManager:
    io_manager = RabbitMQManager()


class Consumer:
    async def get_review_consumer(self) -> Generator:
        async with ReviewConsumer(
            RabbitMQManager.io_manager
        ) as review_consumer:
            yield review_consumer


class Producer:
    async def get_analyze_producer(self) -> Generator:
        async with AnalyzeProducer(
            RabbitMQManager.io_manager
        ) as analyze_producer:
            yield analyze_producer


class NLP:
    sentiment_analyzer = SentimentIntensityAnalyzer()
    morph_analyzer = MorphAnalyzer()

    nlp_service = NLPService(
        sentiment_analyzer,
        morph_analyzer
    )


if __name__ == '__main__':
    nltk.download('stopwords')
    nltk.download('averaged_perceptron_tagger_ru')
    keywords_stopwords = set(stopwords.words('russian'))

    # Download and install Argos Translate package
    from_code = "ru"
    to_code = "en"
    argostranslate.package.update_package_index()
    available_packages = argostranslate.package.get_available_packages()
    package_to_install = next(
        filter(
            lambda x: x.from_code == from_code and x.to_code == to_code, available_packages # noqa
        )
    )
    argostranslate.package.install_from_path(package_to_install.download())

    async def job(collection_service: CollectionService):
        """
        Функция для планировщика, вызывающая сохранение стоп-слов.
        """
        while True:
            await collection_service.save_stopwords()
            # Спим 1 час перед следующим вызовом
            await asyncio.sleep(3600)

    async def start_review_processing():
        """
        Основная логика анализа данных.
        """
        async for analyze_producer in Producer().get_analyze_producer():
            async for review_consumer in Consumer().get_review_consumer():
                analyze_service = AnalyzeService(
                    DB.data_repo,
                    review_consumer,
                    analyze_producer,
                    NLP.nlp_service,
                    keywords_stopwords
                )
                await analyze_service.start_review_processing()

    async def main() -> None:
        # Создаем экземпляры необходимых зависимостей
        collection_service = CollectionService(
            DB.analyze_repo,
            DB.data_repo
        )

        # Запускаем планировщик и основную логику анализа данных параллельно
        scheduler_task = asyncio.create_task(job(collection_service))
        processing_task = asyncio.create_task(start_review_processing())

        await asyncio.gather(scheduler_task, processing_task)

    # Запуск основного кода
    asyncio.run(main())
