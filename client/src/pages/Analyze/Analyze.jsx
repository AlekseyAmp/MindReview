import React, { useEffect, useState } from "react";
import { Helmet } from "react-helmet";
import { Link, useNavigate, useParams } from "react-router-dom";

import { access_token } from "../../constants/token";
import { decodeJWT } from "../../utils/token";
import {
  downloadAnalyzeResult,
  getAnalyzeById,
  getLastAnalyze,
} from "../../services/analyze";
import { getSentimentInfo } from "../../utils/review";

import styles from "./Analyze.module.scss";

import AnalyzeCard from "../../components/Cards/AnalyzeCard/AnalyzeCard";
import WordCloud from "../../components/Visualization/WordCloud/WordCloud";
import PieChart from "../../components/Visualization/PieChart/PieChart";
import GeoChart from "../../components/Visualization/GeoChart/GeoChart";
import BarChart from "../../components/Visualization/BarChart/BarChart";
import PurpleButton from "../../components/UI/Buttons/PurpleButton/PurpleButton";
import ErrorBox from "../../components/PopUps/ErrorBox/ErrorBox";
import SuccessBox from "../../components/PopUps/SuccessBox/SuccessBox";
import AnalyzePreload from "../AnalyzePreload/AnalyzePreload";

function Analyze() {
  const navigate = useNavigate();
  const isAuthorized = !!access_token;
  const token = access_token;
  const [title, setTitle] = useState("");

  const [analyzeData, setAnalyzeData] = useState(null);
  const [filteredEntries, setFilteredEntries] = useState(null);
  const [selectedSentiments, setSelectedSentiments] = useState([]);
  const [selectedKeywords, setSelectedKeywords] = useState([]);
  const [selectedLocations, setSelectedLocations] = useState([]);
  
  const [showMoreKeywords, setShowMoreKeywords] = useState(false);
  const [showMoreLocations, setShowMoreLocations] = useState(false);
  
  const [success, setSuccess] = useState(null);
  const [showSuccess, setShowSuccess] = useState(false);
  const [error, setError] = useState(null);
  const [showError, setShowError] = useState(false);
  
  const [showPreload, setShowPreload] = useState(false);
  
  const { analyze_id } = useParams();
  
    if (!isAuthorized && !analyzeData && analyze_id != "test") {
      return (
        <div className={styles.notAuth}>
          <Helmet>
            <title>MindReview - Анализ отзывов</title>
          </Helmet>
          <div className={styles.notAuthData}>
            <h3 className={`${styles.title} dark-text`}>
              <Link className={`purple-text`} to="/login">
                Войдите{" "}
              </Link>{" "}
              или{" "}
              <Link className={`purple-text`} to="/register">
                зарегистрируйтесь
              </Link>
            </h3>
          </div>
        </div>
      );
    }

  useEffect(() => {
    const fetchData = async () => {
      try {
        if (analyze_id == null) {
          setShowPreload(true);
        } else if (analyze_id == "test") {
          const testData = localStorage.getItem("testAnalyzeData");
          setAnalyzeData(JSON.parse(testData));
          setTitle("Краткий результат анализа тестовых отзывов");
          setShowPreload(false);
        } else if (analyze_id == "last") {
          const analyzeData = await getLastAnalyze();
          setAnalyzeData(analyzeData);
          setTitle("Краткий результат последнего анализа");
          setShowPreload(false);
        } else if (analyze_id == "preload") {
          setShowPreload(true);
        } else {
          const analyzeData = await getAnalyzeById(analyze_id);
          setTitle("Краткий результат анализа");
          setAnalyzeData(analyzeData);
          setShowPreload(false);
        }
      } catch (error) {
        console.error(error);
      }
    };
    fetchData();
    return () => {
      if (analyze_id === "test") {
        localStorage.removeItem("testAnalyzeData");
      }
    };
  }, [analyze_id]);

  useEffect(() => {
    if (analyzeData) {
      let filtered = analyzeData.entries_analyze;

      if (selectedSentiments.length > 0) {
        filtered = filtered.filter((entry) =>
          selectedSentiments.includes(entry.sentiment[0])
        );
      }

      if (selectedKeywords.length > 0) {
        filtered = filtered.filter((entry) => {
          const entryKeywords = entry.keywords;
          return selectedKeywords.some((keyword) =>
            entryKeywords.includes(keyword)
          );
        });
      }

      if (selectedLocations.length > 0) {
        filtered = filtered.filter((entry) => {
          const entryCities = entry.other_info.cities;
          return selectedLocations.some((location) =>
            entryCities.includes(location)
          );
        });
      }

      setFilteredEntries(filtered);
    }
  }, [selectedSentiments, selectedKeywords, selectedLocations, analyzeData]);

  const mostPopularSentiment = analyzeData
    ? Object.keys(analyzeData.full_analyze.sentiments_data.sentiments).reduce(
        (maxSentiment, currentSentiment) =>
          analyzeData.full_analyze.sentiments_data.sentiments[currentSentiment]
            .count >
          analyzeData.full_analyze.sentiments_data.sentiments[maxSentiment]
            .count
            ? currentSentiment
            : maxSentiment,
        Object.keys(analyzeData.full_analyze.sentiments_data.sentiments)[0]
      )
    : null;

  const topKeywords = analyzeData
    ? Object.keys(analyzeData.full_analyze.keywords_cloud || {})
        .sort(
          (a, b) =>
            analyzeData.full_analyze.keywords_cloud[b] -
            analyzeData.full_analyze.keywords_cloud[a]
        )
        .slice(0, 5)
    : [];

  const topCities = analyzeData
    ? Object.keys(analyzeData.full_analyze.geographical_map || {})
        .sort((a, b) => a.localeCompare(b))
        .slice(0, 5)
    : [];

  const filterBySentiment = (sentiment) => {
    const index = selectedSentiments.indexOf(sentiment);
    if (index === -1) {
      setSelectedSentiments([...selectedSentiments, sentiment]);
    } else {
      setSelectedSentiments(
        selectedSentiments.filter((item) => item !== sentiment)
      );
    }
  };

  const filterByKeyword = (keyword) => {
    if (selectedKeywords.includes(keyword)) {
      setSelectedKeywords(selectedKeywords.filter((item) => item !== keyword));
    } else {
      setSelectedKeywords([...selectedKeywords, keyword]);
    }
  };

  const filterByLocation = (location) => {
    if (selectedLocations.includes(location)) {
      setSelectedLocations(
        selectedLocations.filter((item) => item !== location)
      );
    } else {
      setSelectedLocations([...selectedLocations, location]);
    }
  };

  const handleDownloadSubmit = (e) => {
    e.preventDefault();

    const decode = decodeJWT(token);
    if (
      decode.header.is_premium === null ||
      decode.header.is_premium === false
    ) {
      const errorMessage =
        'Нужна подписка "Премиум", чтобы скачать результат анализа.';
      setError(errorMessage);
      setShowSuccess(false);
      setShowError(true);
      setTimeout(() => {
        setShowError(false);
        setError(null);
      }, 2500);
      return;
    } else if (analyzeData.source_type === "test") {
      const errorMessage =
        "Результат анализа тестовых отзывов скачивать нельзя.";
      setError(errorMessage);
      setShowSuccess(false);
      setShowError(true);
      setTimeout(() => {
        setShowError(false);
        setError(null);
      }, 2500);
      return;
    }

    downloadAnalyzeResult(
      analyzeData.id,
      analyzeData.dt,
      setError,
      setShowError,
      setSuccess,
      setShowSuccess
    );
  };

  const handleBackSubmit = () => {
    navigate("/analyze/preload");
  };

  const sentimentInfo = getSentimentInfo(mostPopularSentiment);

  return (
    <div className={styles.analyze}>
      {showPreload && isAuthorized && <AnalyzePreload />}
      <Helmet>
        <title>MindReview - Анализ отзывов</title>
      </Helmet>
      {analyzeData && !showPreload && (
        <>
          {isAuthorized && (
            <div className={styles.backLoading}>
              <p className={`link-text`} onClick={handleBackSubmit}>
                ◄ Вернуться к способам загрузки
              </p>
            </div>
          )}
          <div className={styles.shortAnalyzeResults}>
            <h3 className={`bold-text`}>{title}</h3>
            <div className={styles.shortAnalyzeData}>
              <div className={styles.row}>
                <div className={styles.rowBlock}>
                  <div className={`${styles.label} dark-text`}>
                    Номер анализа:{" "}
                    {analyzeData.id ? (
                      <span className={`dark-text`}>{analyzeData.id}</span>
                    ) : (
                      <span className={`dark-text`}> Нет</span>
                    )}
                  </div>
                </div>
                <div className={styles.rowBlock}>
                  <div className={`${styles.label} dark-text`}>
                    Дата проведения анализа:{" "}
                    <span className={`dark-text`}>{analyzeData.dt}</span>
                  </div>
                </div>
                <div className={styles.rowBlock}>
                  <div className={`${styles.label} dark-text`}>
                    Источник загрузки:{" "}
                    <span className={`purple-text`}>
                      {analyzeData.source_type}
                    </span>
                  </div>
                </div>
                <div className={styles.rowBlock}>
                  <div
                    className={`${styles.label} dark-text`}
                    style={{ maxWidth: 370, wordBreak: "break-all" }}
                  >
                    Ссылка на источник:{" "}
                    <span className={`gray-text`}>
                      {analyzeData.source_url ? analyzeData.source_url : "Нет"}
                    </span>
                  </div>
                </div>
              </div>
              <div className={styles.row}>
                <div className={styles.rowBlock}>
                  <div className={`${styles.label} dark-text`}>
                    Количество отзывов:{" "}
                    <span className={`dark-text`}>
                      {analyzeData.entries_analyze.length}
                    </span>
                  </div>
                </div>
                <div className={styles.rowBlock}>
                  <div className={`${styles.label} dark-text`}>
                    Наиболее популярное настроение:
                  </div>
                  <span
                    className={`${styles.sentimentBlock} white-text`}
                    style={{
                      color: sentimentInfo.color,
                    }}
                  >
                    {mostPopularSentiment} (
                    {
                      analyzeData.full_analyze.sentiments_data.sentiments[
                        mostPopularSentiment
                      ].percentage
                    }
                    %)
                  </span>
                </div>
              </div>
              <div className={styles.row}>
                <div className={`${styles.label} dark-text`}>
                  Топ 5 ключевых слов:
                </div>
                <div>
                  <ul>
                    {topKeywords.map((keyword, index) => (
                      <li className={`gray-text`} key={index}>
                        {keyword}(
                        {analyzeData.full_analyze.keywords_cloud[keyword]})
                      </li>
                    ))}
                    {topKeywords.length === 0 && (
                      <li className={`gray-text`}>Нет данных</li>
                    )}
                  </ul>
                </div>
              </div>
              <div className={styles.row}>
                <div className={`${styles.label} dark-text`}>
                  Топ 5 городов:
                </div>
                <div>
                  <ul>
                    {topCities.map((city, index) => (
                      <li className={`gray-text`} key={index}>
                        {city}({analyzeData.full_analyze.geographical_map[city]}
                        )
                      </li>
                    ))}
                    {topCities.length === 0 && (
                      <li className={`gray-text`}>Нет данных</li>
                    )}
                  </ul>
                </div>
              </div>
            </div>
          </div>
          {isAuthorized ? (
            <>
              <div className={styles.downloadAnalyze}>
                <div className={"center mt50px"}>
                  <PurpleButton
                    title={"Скачать результат анализа"}
                    onClick={handleDownloadSubmit}
                  />
                </div>
              </div>
              <div className={`${styles.visualization} mt50px`}>
                <h3 className={`${styles.visualizationTitle} bold-text`}>
                  Визуализация результатов анализа
                </h3>
                <div className={styles.top}>
                  <div className={styles.topLeft}>
                    <BarChart
                      data={analyzeData.full_analyze.keyword_sentiment_counts}
                    />
                    <GeoChart
                      data={analyzeData.full_analyze.geographical_map}
                    />
                  </div>
                  <div className={styles.topRight}>
                    <WordCloud
                      title={"Облако ключевых слов"}
                      keywords={analyzeData.full_analyze.keywords_cloud}
                    />
                    <PieChart data={analyzeData.full_analyze.sentiments_data} />
                  </div>
                </div>
              </div>
            </>
          ) : (
            <div className={styles.nonAuthorized}>
              <h3 className={`${styles.title} bold-text`}>
                Для визуализации данных и скачивания отчёта нужно <br />
                <Link className={`link-text`} to="/login">
                  войти
                </Link>{" "}
                или{" "}
                <Link className={`link-text`} to="/register">
                  зарегистрироваться
                </Link>
              </h3>
            </div>
          )}
          <div className={`${styles.analyzeBlock}`}>
            <h3 className={`${styles.analyzeTitle} dark-text`}>
              Анализ отзывов {filteredEntries && `(${filteredEntries.length})`}:
            </h3>
            <div className={styles.analyzeContent}>
              <div className={styles.analyzeCards}>
                {filteredEntries &&
                  filteredEntries.map((entry, index) => (
                    <AnalyzeCard key={index} review={entry} />
                  ))}
              </div>
              <div className={styles.analyzeFilters}>
                <div className={styles.sentimentFilters}>
                  <h3 className={`${styles.filterSubtitle} bold-text`}>
                    По настроениям:
                  </h3>
                  <div className={styles.filterOptions}>
                    <label className={`dark-text`}>
                      <input
                        type="checkbox"
                        value="Позитивный"
                        checked={selectedSentiments.includes("Позитивный")}
                        onChange={() => filterBySentiment("Позитивный")}
                      />{" "}
                      Позитивный
                    </label>
                    <label className={`dark-text`}>
                      <input
                        type="checkbox"
                        value="Нейтральный"
                        checked={selectedSentiments.includes("Нейтральный")}
                        onChange={() => filterBySentiment("Нейтральный")}
                      />{" "}
                      Нейтральный
                    </label>
                    <label className={`dark-text`}>
                      <input
                        type="checkbox"
                        value="Негативный"
                        checked={selectedSentiments.includes("Негативный")}
                        onChange={() => filterBySentiment("Негативный")}
                      />{" "}
                      Негативный
                    </label>
                  </div>
                </div>
                <div className={styles.keywordFilters}>
                  <h3 className={`${styles.filterSubtitle} bold-text`}>
                    По ключевым словам:
                  </h3>
                  <div className={styles.filterOptions}>
                    {analyzeData &&
                      analyzeData.full_analyze.keywords_cloud &&
                      Object.keys(analyzeData.full_analyze.keywords_cloud)
                        .sort(
                          (a, b) =>
                            analyzeData.full_analyze.keywords_cloud[b] -
                            analyzeData.full_analyze.keywords_cloud[a]
                        )
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
                  {analyzeData &&
                    analyzeData.full_analyze.keywords_cloud &&
                    Object.keys(analyzeData.full_analyze.keywords_cloud)
                      .length > 15 && (
                      <h3
                        className={`${styles.title} gray-text`}
                        onClick={() => setShowMoreKeywords(!showMoreKeywords)}
                      >
                        {showMoreKeywords ? "Скрыть ▲" : "Показать ещё ▼"}
                      </h3>
                    )}
                </div>
                <div className={styles.locationFilters}>
                  <h3 className={`${styles.filterSubtitle} bold-text`}>
                    По локации:
                  </h3>
                  <div className={styles.filterOptions}>
                    {analyzeData &&
                      analyzeData.full_analyze.geographical_map &&
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
                  {analyzeData &&
                    analyzeData.full_analyze.geographical_map &&
                    Object.keys(analyzeData.full_analyze.geographical_map)
                      .length > 15 && (
                      <h3
                        className={`${styles.title} gray-text`}
                        onClick={() => setShowMoreLocations(!showMoreLocations)}
                      >
                        {showMoreLocations ? "Скрыть ▲" : "Показать ещё ▼"}
                      </h3>
                    )}
                </div>
              </div>
            </div>
          </div>
        </>
      )}
      {!analyzeData && !showPreload && isAuthorized && (
        <div className={styles.notData}>
          <h3 className={`bold-text`}>Нет данных для отображения.</h3>
        </div>
      )}
      {showError && <ErrorBox error={error} />}
      {showSuccess && <SuccessBox success={success} />}
    </div>
  );
}

export default Analyze;
