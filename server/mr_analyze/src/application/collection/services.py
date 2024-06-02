from dataclasses import dataclass

from src.application.analyze import entities as analyze_entities
from src.application.analyze import interfaces as analyze_interfaces
from src.application.collection import entities as collection_entities
from src.application.collection import interfaces as collection_interfaces
from src.application.constants import TimeConstants
from src.application.utils import get_current_dt


@dataclass
class CollectionService:
    """
    Сервис для сбора различных данных с проанализированных отзывов.
    """

    analyze_repo: analyze_interfaces.IAnalyzeRepository
    data_repo: collection_interfaces.IDataRepository

    def _extract_keywords(
        self,
        analyze_results: list[analyze_entities.AnalyzeReturn]
    ) -> list[dict]:
        """
        Извлекает ключевые слова из результатов анализа.

        :param analyze_results: Список результатов анализа.
        :return: Список ключевых слов.
        """

        stopwords = []
        for result in analyze_results:
            for entry_analyze in result.entries_analyze:
                keywords = entry_analyze.get("keywords", [])
                for keyword in keywords:
                    stopwords.append(
                        collection_entities.StopwordInput(
                            dt=get_current_dt(TimeConstants.DEFAULT_TIMEZONE),
                            word=keyword,
                        )
                    )
        return stopwords

    async def save_stopwords(self) -> None:
        """
        Сохраняет стоп-слова в базу данных раз в час.

        :return: Список стоп-слов.
        """

        analyze_results = await self.analyze_repo.\
            get_hour_ago_analyze_results()

        # Извлечение ключевых слов из результатов анализа
        stopwords = self._extract_keywords(analyze_results)

        if stopwords:
            await self.data_repo.save_stopwords(stopwords)
            print("Сохранение стоп-слов завершено")
