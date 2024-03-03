import React, { useState } from 'react';
import styles from './ReviewCard.module.scss';
import { getSentimentInfo } from '../../../utils/review';

function ReviewCard({ review }) {
    const [isOtherInfoOpen, setIsOtherInfoOpen] = useState(false);

    const toggleOtherInfo = () => {
        setIsOtherInfoOpen(!isOtherInfoOpen);
    };

    const number = review.number;
    const rating = review.rating || "Нет";
    const sentiment = review.sentiment;
    const message = review.message;
    const keywords = review.keywords && review.keywords.length > 0 ? review.keywords : null;
    const otherInfo = review.other_info;
    const cities = otherInfo.cities || [];
    const years = otherInfo.years || [];

    const sentimentInfo = getSentimentInfo(sentiment[0]);

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
                            <h3 className={`bold-text`}>Ключевые слова ({keywords.length}):</h3>
                            <div className={styles.tags}>
                                {keywords.map((word, index) => (
                                    <span key={index} className={`${styles.tag} white-text`}>{word}</span>
                                ))}
                            </div>
                        </>
                    ) : (
                        <h3 className={`bold-text`}>Ключевые слова не обнаружены</h3>
                    )}
                </div>
                <div className={styles.otherInfoBlock}>
                    <div className={styles.otherToggle} onClick={toggleOtherInfo}>
                        <h3 className={`${styles.title} bold-text`}>
                            {isOtherInfoOpen ? 'Скрыть' : 'Прочая информация'}
                        </h3>
                    </div>
                    {isOtherInfoOpen && (
                        <div className={styles.otherInfo}>
                            {cities.length > 0 && (
                                <>
                                    <h3 className={`dark-text`}>Упоминания городов ({cities.length}):</h3>
                                    <div className={styles.tags}>
                                        {cities.map((city, index) => (
                                            <span key={index} className={`${styles.tag} white-text`}>{city}</span>
                                        ))}
                                    </div>
                                </>
                            )}
                            {years.length > 0 && (
                                <>
                                    <h3 className={`dark-text`}>Упоминания годов, возрастов ({years.length}):</h3>
                                    <div className={styles.tags}>
                                        {years.map((year, index) => (
                                            <span key={index} className={`${styles.tag} white-text`}>{year}</span>
                                        ))}
                                    </div>
                                </>
                            )}
                        </div>
                    )}
                </div>
            </div>
            <div className={styles.right}>
                <div className={`${styles.sentimentBlock} white-text`} style={
                    {
                        backgroundColor: sentimentInfo.color,
                    }
                }>
                    {sentiment[0]} ({sentiment[1]})
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
