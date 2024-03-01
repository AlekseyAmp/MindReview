import asyncio
from typing import Generator

import nltk
from googletrans import Translator
from nltk.corpus import stopwords
from pymorphy3 import MorphAnalyzer
from sqlalchemy.orm import Session
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

from src.adapters.database import repositories
from src.adapters.database.sa_session import get_session
from src.adapters.nlp.nlp import NLPService
from src.adapters.rpc import AnalyzeProducer, RabbitMQManager, ReviewConsumer
from src.application.analyze.services import AnalyzeService


class DB:
    session: Session = get_session()

    analyze_repo = repositories.AnalyzeRepository(session)


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
    translator = Translator()

    nltk.download('stopwords')
    nltk.download('averaged_perceptron_tagger_ru')
    stop_words = set(stopwords.words('russian'))
    stop_words.update(['что', 'нея', 'норма', 'йорк', 'деньга', 'часть', 'день', 'это', 'так', 'вот', 'быть', 'как', 'в', 'к', 'на', 'руб', 'мой', 'твой', 'его', 'её', 'наш', 'ваш', 'их', 'свой', 'еще', 'очень', 'поэтому', 'однако', 'конечно'])

    nlp_service = NLPService(
        sentiment_analyzer,
        morph_analyzer,
        translator,
        stop_words
    )


if __name__ == '__main__':
    async def main() -> None:
        async for analyze_producer in Producer().get_analyze_producer():
            async for review_consumer in Consumer().get_review_consumer():
                analyze_service = AnalyzeService(
                    DB.analyze_repo,
                    review_consumer,
                    analyze_producer,
                    NLP.nlp_service
                )
                await analyze_service.start_review_processing()

    asyncio.run(main())
