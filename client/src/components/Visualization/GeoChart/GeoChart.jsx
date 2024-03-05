import React, { useState } from 'react';
import styles from './GeoChart.module.scss';

function GeoChart({ data }) {
    // Состояние для отображения модального окна
    const [showModal, setShowModal] = useState(false);
    // Состояние для определения, показывать ли все города или только топ-10
    const [showAllCities, setShowAllCities] = useState(false);

    // Получение топ-10 городов из данных
    const topCities = Object.entries(data)
        .sort((a, b) => b[1] - a[1])
        .slice(0, 10);

    // Определение, какие города показывать
    const allCities = showAllCities
        ? Object.entries(data).sort((a, b) => b[1] - a[1])
        : topCities;

    // Обработчик для открытия модального окна
    const handleShowModal = () => {
        setShowModal(true);
    };

    // Обработчик для закрытия модального окна
    const handleCloseModal = () => {
        setShowModal(false);
    };

    return (
        <div className={styles.geoChart}>
            <h3 className={`bold-text`}>Географическая карта ({Object.keys(data).length})</h3>
            {/* Проверка наличия данных для отображения */}
            {allCities.length > 0 ? (
                <div className={`${styles.cities} mt35px`}>
                    {/* Отображение городов */}
                    {allCities.map(([city, value]) => (
                        <p className={`purple-text`} key={city}>{city}: <span className={`purple-text`}>{value}</span></p>
                    ))}
                    {/* Показать ссылку на показ остальных городов, если их больше 10 */}
                    {Object.keys(data).length > 10 && !showAllCities && (
                        <p className={`${styles.showMore} gray-text`} onClick={handleShowModal}>Показать больше ▼</p>
                    )}
                </div>
            ) : (
                // Если города не найдены
                <p className={`${styles.notFound} dark-text`}>Города не обнаружены</p>
            )}

            {/* Модальное окно */}
            {showModal && (
                <div className={styles.fullChartOverlay}>
                    <div className={styles.fullChartContainer}>
                        <div className={styles.modalContent}>
                            <h3 className={`bold-text`}>Все города</h3>
                            {/* Показ всех городов */}
                            {Object.entries(data).sort((a, b) => b[1] - a[1]).map(([city, value]) => (
                                <p className={`purple-text`} key={city}>{city}: <span className={`purple-text`}>{value}</span></p>
                            ))}
                        </div>
                        {/* Кнопка закрытия модального окна */}
                        <p className={`link-text ${styles.closeButton}`} onClick={handleCloseModal}>Закрыть ✖</p>
                    </div>
                </div>
            )}
        </div>
    );
}

export default GeoChart;
