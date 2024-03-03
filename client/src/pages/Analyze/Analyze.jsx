import React, { useEffect, useState } from 'react';
import styles from './Analyze.module.scss';
import ReviewCard from '../../components/Cards/ReviewCard/ReviewCard';

function Analyze() {
  const [analyzeData, setAnalyzeData] = useState(null);

  useEffect(() => {
    const data = localStorage.getItem('lastTestAnalyzeData');
    if (data) {
      setAnalyzeData(JSON.parse(data));
    }
  }, []);

  return (
    <div className={styles.analyzeContainer}>
      <h2 className={styles.analyzeTitle}>Результаты анализа: (Временный вариант оформления)</h2>
      {analyzeData ? (
        <div>
          <p>Дата анализа: {analyzeData.dt}</p>
          <p>Тип источника: {analyzeData.source_type}</p>
          <p>Статус: {analyzeData.status}</p>
          <h3 className={styles.analyzeSubtitle}>Анализ записей:</h3>
          {analyzeData.entries_analyze.map((entry, index) => (
            <ReviewCard key={index} review={entry} />
          ))}
        </div>
      ) : (
        <p>Нет данных для отображения.</p>
      )}
    </div>
  );
}

export default Analyze;
