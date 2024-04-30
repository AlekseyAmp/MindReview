from dataclasses import asdict

import requests

from src.application.constants import ReviewsURLConstants
from src.application.review import entities, interfaces


class ReviewsParser(interfaces.IReviewsParser):
    """Класс для получения данных о продукте из API Wildberries."""

    def fetch_wildberries_reviews(
        self,
        reviews_id: int
    ) -> list[entities.ReviewTemplate]:
        """
        Метод для получения отзывов Wildberries.

        :param reviews_id: Идентификатор отзывов.

        :return: Список отзывов.
        """

        response = requests.get(
            ReviewsURLConstants.WB_FEEDBACK_URL + str(reviews_id)
        )

        if response.status_code == 200:
            data = response.json()
            reviews_data = data.get('feedbacks')

            if reviews_data:
                # Создаем пустой список для хранения отзывов
                reviews = []

                for review_info in reviews_data:
                    review = {
                        "text": review_info.get("text").strip(),
                        "rating": review_info.get("productValuation"),
                    }

                    # Добавляем текущий отзыв в список
                    reviews.append(review)

                # Подготовка отзывов для анализа
                prepared_reviews = [
                    asdict(
                        entities.ReviewTemplate(
                            number=index,
                            message=review.get("text"),
                            raiting=review.get("rating"),
                        )
                    )
                    for index, review in enumerate(reviews, start=1)
                ]

                return prepared_reviews

        return None
