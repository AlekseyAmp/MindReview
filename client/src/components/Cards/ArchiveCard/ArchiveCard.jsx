import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import styles from './ArchiveCard.module.scss';
import { access_token } from '../../../constants/token';
import { decodeJWT } from '../../../utils/token';
import { downloadAnalyzeResult, getAnalyzeById } from '../../../services/analyze';
import { getSentimentInfo } from '../../../utils/review';
import OrangeButton from '../../UI/Buttons/OrangeButton/OrangeButton';
import PurpleButton from '../../UI/Buttons/PurpleButton/PurpleButton';
import ErrorBox from '../../PopUps/ErrorBox/ErrorBox';
import SuccessBox from '../../PopUps/SuccessBox/SuccessBox';

function ArchiveCard({ cardKey, analyzeResult }) {
    const navigate = useNavigate();

    const isAuthorized = !!access_token;
    const token = access_token

    const [success, setSuccess] = useState(null);
    const [showSuccess, setShowSuccess] = useState(false);
    const [error, setError] = useState(null);
    const [showError, setShowError] = useState(false);
    const [expanded, setExpanded] = useState(false);

    const { id, dt, source_type, source_url, full_analyze } = analyzeResult;
    const { keywords_cloud, sentiments_data, geographical_map } = full_analyze;

    const toggleExpand = () => {
        setExpanded(!expanded);
    };

    const truncatedSourceUrl = source_url.length > 15 ? source_url.substring(0, 15) : source_url;

    const maxSentiment = Object.keys(sentiments_data.sentiments).reduce((maxSentiment, currentSentiment) =>
        sentiments_data.sentiments[currentSentiment].count > sentiments_data.sentiments[maxSentiment].count ? currentSentiment : maxSentiment
        , Object.keys(sentiments_data.sentiments)[0]);
    const maxSentimentPercentage = sentiments_data.sentiments[maxSentiment].percentage;

    const topKeywords = Object.keys(keywords_cloud)
        .sort((a, b) => keywords_cloud[b] - keywords_cloud[a])
        .slice(0, 5);

    const topCities = Object.keys(geographical_map)
        .sort((a, b) => geographical_map[b] - geographical_map[a])
        .slice(0, 5);

    const handleDownloadSubmit = (e) => {
        e.preventDefault();

        const decode = decodeJWT(token)
        if (decode.header.is_premium === null || decode.header.is_premium === false) {
            const errorMessage = "Нужна подписка \"Премиум\", чтобы скачать результат анализа.";
            setError(errorMessage);
            setShowSuccess(false);
            setShowError(true);
            setTimeout(() => {
                setShowError(false);
                setError(null);
            }, 2500);
            return;
        } else if (source_type === "test") {
            const errorMessage = "Результат анализа тестовых отзывов скачивать нельзя."
            setError(errorMessage);
            setShowSuccess(false);
            setShowError(true);
            setTimeout(() => {
                setShowError(false);
                setError(null);
            }, 2500);
            return;
        }

        downloadAnalyzeResult(id, dt, setError, setShowError, setSuccess, setShowSuccess);

    }

    const sentimentInfo = getSentimentInfo(maxSentiment);

    const handleOpenAnalyze = async (e) => {
        e.preventDefault();
        navigate(`/analyze/${id}`)
    };

    return (
        <div className={styles.card}>
            <div className={styles.cardContent}>
                <div className={styles.cardNumber}>
                    <p className={`gray-text`}>{id}</p>
                </div>
                <div className={styles.dt}>
                    <p className={`gray-text`}>{dt}</p>
                </div>
                <div className={styles.sourceType}>
                    <p className={`purple-text`}>
                        {source_type}
                        <span className={`${styles.sourceURL} gray-text`}>
                            ({expanded ? source_url : truncatedSourceUrl})
                            {source_url.length > 40 && (
                                <span className={`link-text`} onClick={toggleExpand}>
                                    {expanded ? ' (Свернуть)' : ' (Показать полностью)'}
                                </span>
                            )}
                        </span>
                    </p>
                </div>
                <div className={`${styles.sentimentBlock} white-text`} style={
                    {
                        color: sentimentInfo.color,
                    }
                }>
                    {maxSentiment} ({maxSentimentPercentage}%)
                </div>
                <div className={styles.keywords}>
                    <ul>
                        {topKeywords.map((keyword, index) => (
                            <li className={`dark-text`} key={index}>
                                {keyword} ({keywords_cloud[keyword]})
                                {index !== topKeywords.length - 1 && ','}
                            </li>
                        ))}
                        {topKeywords.length === 0 && <li className={`dark-text`}>Нет данных</li>}
                    </ul>
                </div>
                <div className={styles.cities}>
                    <ul>
                        {topCities.map((city, index) => (
                            <li className={`dark-text`} key={index}>
                                {city} ({geographical_map[city]})
                                {index !== topCities.length - 1 && ','}
                            </li>
                        ))}
                        {topCities.length === 0 && <li className={`dark-text`}>Нет данных</li>}
                    </ul>
                </div>
                <div className={styles.buttons}>
                    <OrangeButton
                        title={"Открыть анализ"}
                        width={70}
                        onClick={handleOpenAnalyze}
                    />
                    <PurpleButton
                        title={"Скачать анализ"}
                        width={70}
                        onClick={handleDownloadSubmit}
                    />
                </div>
            </div>
            {showError && <ErrorBox error={error} />}
            {showSuccess && <SuccessBox success={success} />}
        </div>

    );
}

export default ArchiveCard;
