import React from 'react';
import styles from './ReviewCard.module.scss';
import { getSentimentInfo, formatAge } from '../../../../utils/review';

function ReviewCard({ review }) {
    // Проверяем, если review равно null, заменяем на "Не определено"
    const number = review.number;
    const rating = review.rating || "Нет";
    const sentiment = review.sentiment;
    const message = review.message;
    const keywords = review.keywords && review.keywords.length > 0 ? review.keywords : null;
    const authorGender = review.author_gender || null;
    const authorAge = review.author_age || null;

    // Получаем цвет для настроения
    const sentimentInfo = getSentimentInfo(sentiment);

    return (
        <div className={styles.card}>
            <div className={styles.left}>
                <div className={styles.header}>
                    <p className={`gray-text`}>Номер: {number}</p>
                </div>
                <div className={styles.messageBlock}>
                    <p className={`dark-text`}>{message}</p>
                </div>
                <div className={styles.keywordsBlock}>
                    {keywords && keywords.length > 0 ? (
                        <>
                            <h3 className={`bold-text`}>Ключевые слова:</h3>
                            <div className={styles.keywords}>
                                {keywords.map((word, index) => (
                                    <span key={index} className={`${styles.keyword} white-text`}>{word}</span>
                                ))}
                            </div>
                        </>
                    ) : (
                        <h3 className={`bold-text`}>Ключевые слова не обнаружены</h3>
                    )}
                </div>
                {authorGender || authorAge ? (
                    <div className={styles.authorInfoBlock}>
                        <h3 className={`bold-text`}>Информация об авторе:</h3>
                        <div className={styles.author}>
                            <p className={`dark-text`}>
                                {authorGender && `${authorGender}`}
                                {authorGender && authorAge && " "}
                                {authorAge && `${authorAge} ${formatAge(authorAge)}`}
                            </p>
                        </div>
                    </div>
                ) : (
                    <div className={styles.authorInfoBlock}>
                        <h3 className={`bold-text`}>Информация об авторе не найдена</h3>
                    </div>
                )}
            </div>
            <div className={styles.right}>
                <div className={`${styles.sentimentBlock} white-text`} style={
                    {
                        backgroundColor: sentimentInfo.color,
                    }
                }>
                    {sentiment}
                </div>
                <div className={styles.raiting}>
                    <div className={styles.raitingInfo}>
                        <img src="img/icons/raiting.svg" alt="raiting" />
                        <span className={`purple-text`}>{rating}</span>
                    </div>
                </div>
            </div>
        </div>


    );
};

export default ReviewCard;
