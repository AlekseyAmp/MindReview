import React, { useState } from "react";
import styles from "./GeoChart.module.scss";

function GeoChart({ data }) {
  const [showModal, setShowModal] = useState(false);
  const [showAllCities, setShowAllCities] = useState(false);

  const topCities = Object.entries(data)
    .sort((a, b) => b[1] - a[1])
    .slice(0, 10);

  const allCities = showAllCities
    ? Object.entries(data).sort((a, b) => b[1] - a[1])
    : topCities;

  const handleShowModal = () => {
    setShowModal(true);
  };

  const handleCloseModal = () => {
    setShowModal(false);
  };

  return (
    <div className={styles.geoChart}>
      <h3 className={`bold-text`}>
        Географическая карта ({Object.keys(data).length})
      </h3>
      {allCities.length > 0 ? (
        <div className={`${styles.cities} mt35px`}>
          {allCities.map(([city, value]) => (
            <p className={`purple-text`} key={city}>
              {city}: <span className={`purple-text`}>{value}</span>
            </p>
          ))}
          {Object.keys(data).length > 10 && !showAllCities && (
            <p
              className={`${styles.showMore} gray-text`}
              onClick={handleShowModal}
            >
              Показать больше ▼
            </p>
          )}
        </div>
      ) : (
        <p className={`${styles.notFound} dark-text`}>Города не обнаружены</p>
      )}

      {showModal && (
        <div className={styles.fullChartOverlay}>
          <div className={styles.fullChartContainer}>
            <div className={styles.modalContent}>
              <h3 className={`bold-text`}>Все города</h3>
              {Object.entries(data)
                .sort((a, b) => b[1] - a[1])
                .map(([city, value]) => (
                  <p className={`purple-text`} key={city}>
                    {city}: <span className={`purple-text`}>{value}</span>
                  </p>
                ))}
            </div>
            <p
              className={`link-text ${styles.closeButton}`}
              onClick={handleCloseModal}
            >
              Закрыть ✖
            </p>
          </div>
        </div>
      )}
    </div>
  );
}

export default GeoChart;
