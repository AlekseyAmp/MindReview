import re
from dataclasses import dataclass

# from fuzzywuzzy import fuzz - пока что не используем
from googletrans import Translator
from pymorphy3 import MorphAnalyzer
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

from src.application.analyze import interfaces as analyze_interfaces
from src.application.collection import interfaces as collection_interfaces
from src.application.constants import GENDERS, PartOfSpeech, SentimentCategory
from src.application.utils import round_float
from src.application.collection import entities


@dataclass
class NLPService(analyze_interfaces.INLPService):
    """
    Сервис обработки естественного языка (Natural Language Processing).

    :param sentiment_analyzer: Анализатор настроений.
    :param morph_analyzer: Морфологический анализатор.
    :param translator: Переводчик.
    """

    sentiment_analyzer: SentimentIntensityAnalyzer
    morph_analyzer: MorphAnalyzer
    translator: Translator

    def _translate_text(
        self,
        text: str,
        src_lang: str = 'ru',
        dest_lang: str = 'en'
    ) -> str:
        """
        Производит перевод текста с одного языка на другой.

        :param text: Текст для перевода.
        :param src_lang: Исходный язык текста (по умолчанию 'ru' - русский).
        :param dest_lang: Целевой язык текста (по умолчанию 'en' - английский).

        :return: Переведенный текст.
        """

        translated_text = self.translator.translate(
            text,
            src=src_lang,
            dest=dest_lang
        ).text

        return translated_text

    def _categorize_sentiment(self, score: float) -> tuple[str, float]:
        """
        Категоризирует числовую оценку настроения
        в текстовую категорию.

        :param score: Числовая оценка настроения.

        :return: Кортеж с текстовой категорией
        настроения и числовым значением оценки.
        """
        sentiment_categories = {
            score > 0.05: (SentimentCategory.POSITIVE, score),
            score < -0.05: (SentimentCategory.NEGATIVE, score),
        }

        # Если ни одно условие не выполнено,
        #   значит оценка находится в пределах от -0.05 до 0.05
        #   и считается нейтральной
        return sentiment_categories.get(
            True,
            (SentimentCategory.NEUTRAL, score)
        )

    def analyze_sentiment(
        self,
        reviews: list[dict]
    ) -> dict[int, tuple[str, float]]:
        """
        Анализирует настроения отзывов.

        :param reviews: Список текстов отзывов.

        :return: Словарь с индексами отзывов
        и их оценками настроения в виде кортежа
        (текстовая категория, числовое значение).
        """
        sentiment_categories = {}

        for review in reviews:
            # Перевод текста отзыва на английский
            #   (с русским работает плохо)

            translated_review = self._translate_text(
                self._clean_text(review["message"])
            )

            # Анализ настроения текста и получение компаунд-оценки.
            sentiment_score = self.sentiment_analyzer.polarity_scores(
                translated_review
            )["compound"]

            # Категоризация оценки настроения.
            sentiment_category, score = self._categorize_sentiment(
                sentiment_score
            )

            # Сохранение индекса отзыва
            #   и его оценки настроения в словаре sentiment_categories.
            sentiment_categories[review["number"]] = (
                sentiment_category.value,
                round_float(score)
            )

        # Возврат словаря с индексами отзывов и их оценками настроения.
        return sentiment_categories

    def _clean_text(self, text: str) -> str:
        """
        Очищает текст от лишних символов и цифр.

        :param text: Исходный текст для очистки.

        :return: Очищенный текст или слово-заглушка,
        если текст становится пустым после очистки.
        """

        # Очистка текста от лишних символов:
        #   оставляем только буквы, пробелы
        #   и символы национального алфавита, включая букву "ё"
        cleaned_text = re.sub(r'[^\w\sёЁ]', '', text)

        # Заменяем все последовательности пробелов
        #   на одиночные пробелы и удаляем лишние символы и цифры.
        cleaned_text = re.sub(
            r'\s+', ' ', re.sub(r'[\d\W]', ' ', cleaned_text)
        )

        # Если текст пустой после очистки, вернуть слово-заглушку
        if not cleaned_text.strip():
            return "И"

        return cleaned_text

    def _extract_nouns(
        self,
        text: str,
        keywords_stopwords: set[str]
    ) -> set[str]:
        """
        Извлекает существительные из текста.

        :param text: Текст для извлечения существительных.
        :return: Множество существительных.
        """

        nouns = set()

        # Разделение текста на отдельные слова.
        words = text.split()

        for word in words:
            # Анализ морфологии слова.
            parsed_word = self.morph_analyzer.parse(word)[0]

            # Нормализация слова.
            normalized_word = parsed_word.normal_form

            # Проверка, не является ли слово стоп-словом.
            if normalized_word not in keywords_stopwords:
                # Получение части речи, падежа и одушевлённости слова.
                pos = parsed_word.tag.POS
                case = parsed_word.tag.case
                anim = parsed_word.tag.animacy

                # Добавление существительного в список,
                #   если это существительное не в именительном падеже
                #   и не одушевлённое.
                if pos == PartOfSpeech.NOUN.value and not (
                    case == "nomn" and anim == "anim"
                ):
                    nouns.add(normalized_word)
        return nouns

    def extract_keywords(
        self,
        reviews: list[dict],
        keywords_stopwords: set[str]
    ) -> dict[int, list[str | None]]:
        """
        Извлекает ключевые слова из отзывов.

        :param reviews: Список отзывов.
        :return: Словарь с индексами отзывов и списками ключевых слов.
        """
        keywords_dict = {}

        for review in reviews:
            # Извлечение ключевых слов из текста отзыва.
            keywords = self._extract_nouns(
                self._clean_text(review["message"]),
                keywords_stopwords
            )

            # Сохранение ключевых слов в словаре,
            #   где ключ - индекс отзыва, значение - список ключевых слов.
            keywords_dict[review["number"]] = list(keywords)

        return keywords_dict

    def _extract_verbs(self, text: str) -> list[str | None]:
        """
        Извлекает глаголы из текста.

        :param text: Текст для извлечения глаголов.

        :return: Список глаголов.
        """

        verbs = []

        # Очищаем текст от лишних символов
        clean_text = self._clean_text(text)

        # Разбиваем текст на слова
        words = clean_text.split()

        for word in words:
            # Анализируем каждое слово морфологически
            parsed_word = self.morph_analyzer.parse(word)[0]

            # Проверяем, является ли слово глаголом
            if parsed_word.tag.POS == PartOfSpeech.VERB.value:
                verbs.append(parsed_word.word)

        return verbs

    # Не используется
    def extract_gender_author(
        self,
        reviews: list[dict]
    ) -> dict[int, str | None]:
        """
        Извлекает пол авторов отзывов на основе использованных глаголов.

        :param reviews: Список отзывов.

        :return: Словарь с индексами отзывов и определением пола авторов.
        """
        genders = {"masc": 0, "femn": 0}

        for review in reviews:
            # Извлекаем глаголы из текста отзыва
            verbs = self._extract_verbs(review["message"])

            if verbs:
                # Определяем пол по глаголам
                for verb in verbs:
                    gender = self.morph_analyzer.parse(verb)[0].tag.gender
                    if gender in GENDERS.keys():
                        genders[gender] += 1

        if genders["masc"] > genders["femn"]:
            dominant_gender = GENDERS.get("masc")
        elif genders["femn"] > genders["masc"]:
            dominant_gender = GENDERS.get("femn")
        else:
            dominant_gender = None

        gender_results = {
            review["number"]: dominant_gender
            for review in reviews
        }

        return gender_results

    def extract_years(
        self,
        reviews: list[dict]
    ) -> dict[int, list[int | None]]:
        """
        Определяет возраст авторов отзывов
        на основе текстов сообщений отзывов.

        :param reviews: Список отзывов.

        :return: Словарь с индексами отзывов и возрастами авторов.
        """

        years_dict = {}

        # Задаем шаблон регулярного выражения
        # для поиска упоминаний года в тексте отзыва
        year_pattern = r'\b(\d{1,10})\s*(?:год(?:а|ов|у|ом)?|лет|годи(?:к(?:а|ов|у|ом)?)?)\b'

        # Перебираем каждый отзыв из предоставленного списка
        for review in reviews:
            # Ищем все совпадения с шаблоном года в тексте отзыва
            matches = re.findall(
                year_pattern,
                review["message"],
                re.IGNORECASE
            )

            # Если совпадения найдены
            if matches:
                # Преобразуем найденные года из строкового формата
                # в целые числа
                years = set(int(match) for match in matches)

                # Сохраняем список годов в словаре,
                # где ключ - индекс отзыва, значение - список годов
                years_dict[review["number"]] = list(years)

        return years_dict

    def extract_cities(
        self,
        reviews: list[dict],
        all_cities: list[entities.City],
        cities_stopwords: set[str]
    ) -> dict[int, set[str | None]]:
        """
        Извлекает города из текста отзыва.

        :param reviews: Список отзывов.

        :return: Словарь с индексами отзывов
            и найденными городами (в виде множества).
        """
        cities_dict = {}

        # Создаем словарь из названий городов в нижнем регистре
        cities = {
            city.raw_name: city.original_name
            for city in all_cities
        }
        
        for review in reviews:
            # Токенизируем текст отзыва и проводим морфологический анализ
            tokens = self._clean_text(review["message"]).split()

            nouns = set()
            for token in tokens:
                parsed_token = self.morph_analyzer.parse(token)[0]
                if (
                    (parsed_token.normal_form not in cities_stopwords) and
                    (
                        parsed_token.tag.POS == PartOfSpeech.NOUN.value or \
                            PartOfSpeech.UNKNOWN.value in parsed_token.tag
                    )
                ):
                    nouns.add(parsed_token.normal_form)

            # Создаем пустое множество
            #   для хранения найденных городов в текущем отзыве
            found_cities = set()

            # Проверяем каждое существительное
            #   отзыва на вхождение в названия городов
            for review_noun_word in nouns:
                for raw_city in cities.keys():
                    if raw_city.startswith(review_noun_word):
                        found_cities.add(cities[raw_city])

            cities_dict[review["number"]] = list(found_cities)

        return cities_dict
