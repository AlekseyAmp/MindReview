import React, { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';

import { access_token } from '../../constants/token';

import styles from './Analyze.module.scss';

import AnalyzeCard from '../../components/Cards/AnalyzeCard/AnalyzeCard';
import WordCloud from '../../components/Visualization/WordCloud/WordCloud';
import PieChart from '../../components/Visualization/PieChart/PieChart';
import GeoChart from '../../components/Visualization/GeoChart/GeoChart';
import BarChart from '../../components/Visualization/BarChart/BarChart';
import PurpleButton from '../../components/UI/Buttons/PurpleButton/PurpleButton';

function Analyze() {
  const isAuthorized = !!access_token;
  const [analyzeData, setAnalyzeData] = useState(null);
  const [filteredEntries, setFilteredEntries] = useState(null);
  const [selectedSentiments, setSelectedSentiments] = useState([]);
  const [selectedKeywords, setSelectedKeywords] = useState([]);
  const [selectedLocations, setSelectedLocations] = useState([]);
  const [showMoreKeywords, setShowMoreKeywords] = useState(false);
  const [showMoreLocations, setShowMoreLocations] = useState(false);

  useEffect(() => {
    const data = localStorage.getItem('lastTestAnalyzeData');
    if (data) {
      setAnalyzeData(JSON.parse(data));
    }
  }, []);

  const filterBySentiment = (sentiment) => {
    const index = selectedSentiments.indexOf(sentiment);
    if (index === -1) {
      setSelectedSentiments([...selectedSentiments, sentiment]);
    } else {
      setSelectedSentiments(selectedSentiments.filter((item) => item !== sentiment));
    }
  }

  const filterByKeyword = (keyword) => {
    if (selectedKeywords.includes(keyword)) {
      setSelectedKeywords(selectedKeywords.filter((item) => item !== keyword));
    } else {
      setSelectedKeywords([...selectedKeywords, keyword]);
    }
  }

  const filterByLocation = (location) => {
    if (selectedLocations.includes(location)) {
      setSelectedLocations(selectedLocations.filter((item) => item !== location));
    } else {
      setSelectedLocations([...selectedLocations, location]);
    }
  }

  useEffect(() => {
    if (analyzeData) {
      let filtered = analyzeData.entries_analyze;

      if (selectedSentiments.length > 0) {
        filtered = filtered.filter(entry => selectedSentiments.includes(entry.sentiment[0]));
      }

      if (selectedKeywords.length > 0) {
        filtered = filtered.filter(entry => {
          const entryKeywords = entry.keywords;
          return selectedKeywords.some(keyword => entryKeywords.includes(keyword));
        });
      }

      if (selectedLocations.length > 0) {
        filtered = filtered.filter(entry => {
          const entryCities = entry.other_info.cities;
          return selectedLocations.some(location => entryCities.includes(location));
        });
      }

      setFilteredEntries(filtered);
    }
  }, [selectedSentiments, selectedKeywords, selectedLocations, analyzeData]);

  return (
    <div className={styles.analyze}>
      {analyzeData && (
        <>
          <div className={styles.shortAnalyzeResults}>
            <h3 className={`bold-text`}>Краткий результат анализа</h3>
            <table className={styles.shortAnalyzeTable}>
              <tbody>
                <tr>
                  <td className={`dark-text`}>Дата проведения анализа</td>
                  <td className={`dark-text`}>{analyzeData.dt}</td>
                </tr>
                <tr>
                  <td className={`dark-text`}>Источник загрузки</td>
                  <td className={`dark-text`}>{analyzeData.source_type}</td>
                </tr>
                <tr>
                  <td className={`dark-text`}>Ссылка на источник</td>
                  <td className={`dark-text`}>{analyzeData.source_url ? analyzeData.source_url : "Нет"}</td>
                </tr>
                <tr>
                  <td className={`dark-text`}>Количество отзывов</td>
                  <td className={`dark-text`}>{analyzeData.entries_analyze.length}</td>
                </tr>
                <tr>
                  <td className={`dark-text`}>Наиболее популярное настроение</td>
                  <td className={`dark-text`}>
                    {Object.keys(analyzeData.full_analyze.sentiments_data.sentiments).reduce((maxSentiment, currentSentiment) => (
                      analyzeData.full_analyze.sentiments_data.sentiments[currentSentiment].count > analyzeData.full_analyze.sentiments_data.sentiments[maxSentiment].count ? currentSentiment : maxSentiment
                    ), Object.keys(analyzeData.full_analyze.sentiments_data.sentiments)[0])}{" "}
                    ({analyzeData.full_analyze.sentiments_data.sentiments[Object.keys(analyzeData.full_analyze.sentiments_data.sentiments).reduce((maxSentiment, currentSentiment) => (
                      analyzeData.full_analyze.sentiments_data.sentiments[currentSentiment].count > analyzeData.full_analyze.sentiments_data.sentiments[maxSentiment].count ? currentSentiment : maxSentiment
                    ), Object.keys(analyzeData.full_analyze.sentiments_data.sentiments)[0])].percentage}%)
                  </td>
                </tr>
                <tr>
                  <td className={`dark-text`}>Топ 5 ключевых слов</td>
                  <td>
                    <ul>
                      {analyzeData.full_analyze.keywords_cloud &&
                        Object.keys(analyzeData.full_analyze.keywords_cloud)
                          .sort((a, b) => analyzeData.full_analyze.keywords_cloud[b] - analyzeData.full_analyze.keywords_cloud[a])
                          .slice(0, 5)
                          .map((keyword, index) => (
                            <li className={`dark-text`} key={index}>{keyword}({analyzeData.full_analyze.keywords_cloud[keyword]})</li>
                          ))}
                    </ul>
                  </td>
                </tr>
                <tr>
                  <td className={`dark-text`}>Топ 5 городов</td>
                  <td>
                    <ul>
                      {analyzeData.full_analyze.geographical_map &&
                        Object.keys(analyzeData.full_analyze.geographical_map)
                          .sort((a, b) => a.localeCompare(b))
                          .slice(0, 5)
                          .map((city, index) => (
                            <li className={`dark-text`} key={index}>{city}({analyzeData.full_analyze.geographical_map[city]})</li>
                          ))}
                    </ul>

                  </td>
                </tr>
              </tbody>
            </table>
          </div>
          {isAuthorized ? (
            <>
              <div className={styles.downloadAnalyze}>
                <div className={'center mt35px'}>
                  <PurpleButton
                    title={"Скачать результат анализа"}
                  />
                </div>
              </div>
              <div className={`${styles.visualization} mt50px`}>
                <h3 className={`${styles.visualizationTitle} bold-text`}>Визуализация результатов анализа</h3>
                <div className={styles.top}>
                  <div className={styles.topLeft}>
                    <BarChart data={analyzeData.full_analyze.keyword_sentiment_counts} />
                    <GeoChart data={analyzeData.full_analyze.geographical_map} />
                  </div>
                  <div className={styles.topRight}>
                    <WordCloud keywords={analyzeData.full_analyze.keywords_cloud} />
                    <PieChart data={analyzeData.full_analyze.sentiments_data} />
                  </div>
                </div>
                {/* <div className={styles.bottom}></div> */}
              </div>
            </>
          ) : (
            <div className={styles.nonAuthorized}>
              <h3 className={`${styles.title} bold-text`}>
                Для визуализации данных и скачивания отчёта нужно <br />
                <Link className={`link-text`} to="/login">
                  войти
                </Link>{' '}
                или{' '}
                <Link className={`link-text`} to="/register">
                  зарегистрироваться
                </Link>
              </h3>
            </div>
          )}
          <div className={`${styles.analyzeBlock}`}>
            <h3 className={`${styles.analyzeTitle} dark-text`}>Анализ отзывов {filteredEntries && `(${filteredEntries.length})`}:</h3>
            <div className={styles.analyzeContent}>
              <div className={styles.analyzeCards}>
                {filteredEntries && filteredEntries.map((entry, index) => (
                  <AnalyzeCard key={index} review={entry} />
                ))}
              </div>
              <div className={styles.analyzeFilters}>
                <div className={styles.sentimentFilters}>
                  <h3 className={`${styles.filterSubtitle} bold-text`}>По настроениям:</h3>
                  {/* Sentiment filters */}
                  <div className={styles.filterOptions}>
                  <label className={`dark-text`}>
                    <input type="checkbox" value="Позитивный" checked={selectedSentiments.includes("Позитивный")} onChange={() => filterBySentiment("Позитивный")} /> Позитивный
                  </label>
                  <label className={`dark-text`}>
                    <input type="checkbox" value="Нейтральный" checked={selectedSentiments.includes("Нейтральный")} onChange={() => filterBySentiment("Нейтральный")} /> Нейтральный
                  </label>
                  <label className={`dark-text`}>
                    <input type="checkbox" value="Негативный" checked={selectedSentiments.includes("Негативный")} onChange={() => filterBySentiment("Негативный")} /> Негативный
                  </label>
                  </div>
                </div>
                <div className={styles.keywordFilters}>
                  <h3 className={`${styles.filterSubtitle} bold-text`}>По ключевым словам:</h3>
                  <div className={styles.filterOptions}>
                    {analyzeData && analyzeData.full_analyze.keywords_cloud &&
                      Object.keys(analyzeData.full_analyze.keywords_cloud)
                        .sort((a, b) => analyzeData.full_analyze.keywords_cloud[b] - analyzeData.full_analyze.keywords_cloud[a])
                        .slice(0, showMoreKeywords ? undefined : 15)
                        .map((keyword, index) => (
                          <label className={`dark-text`} key={index}>
                            <input
                              type="checkbox"
                              value={keyword}
                              checked={selectedKeywords.includes(keyword)}
                              onChange={() => filterByKeyword(keyword)}
                            />
                            {keyword}
                          </label>
                        ))}
                  </div>
                  {/* Show more/less button */}
                  {analyzeData && analyzeData.full_analyze.keywords_cloud && Object.keys(analyzeData.full_analyze.keywords_cloud).length > 15 && (
                    <h3 className={`${styles.title} gray-text`} onClick={() => setShowMoreKeywords(!showMoreKeywords)}>
                      {showMoreKeywords ? 'Скрыть ▲' : 'Показать ещё ▼'}
                    </h3>
                  )}
                </div>
                <div className={styles.locationFilters}>
                  <h3 className={`${styles.filterSubtitle} bold-text`}>По локации:</h3>
                  <div className={styles.filterOptions}>
                    {analyzeData && analyzeData.full_analyze.geographical_map &&
                      Object.keys(analyzeData.full_analyze.geographical_map)
                        .sort((a, b) => a.localeCompare(b))
                        .slice(0, showMoreLocations ? undefined : 15)
                        .map((city, index) => (
                          <label className={`dark-text`} key={index}>
                            <input
                              type="checkbox"
                              value={city}
                              checked={selectedLocations.includes(city)}
                              onChange={() => filterByLocation(city)}
                            />
                            {city}
                          </label>
                        ))}
                  </div>
                  {/* Show more/less button */}
                  {analyzeData && analyzeData.full_analyze.geographical_map && Object.keys(analyzeData.full_analyze.geographical_map).length > 15 && (
                    <h3 className={`${styles.title} gray-text`} onClick={() => setShowMoreLocations(!showMoreLocations)}>
                      {showMoreLocations ? 'Скрыть ▲' : 'Показать ещё ▼'}
                    </h3>
                  )}
                </div>
              </div>
            </div>
          </div>
        </>
      )}
      <div className={styles.notData}>{!analyzeData && <h3 className={`bold-text`}>Нет данных для отображения.</h3>}</div>
    </div>
  );
}

export default Analyze;
