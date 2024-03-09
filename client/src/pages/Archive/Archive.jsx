import React, { useEffect, useState } from "react";
import { Helmet } from "react-helmet";
import { Link } from "react-router-dom";
import { access_token } from "../../constants/token";
import { getAllAnalyzeResults } from "../../services/analyze";
import ArchiveCard from "../../components/Cards/ArchiveCard/ArchiveCard";
import WordCloud from "../../components/Visualization/WordCloud/WordCloud";
import PieChart from "../../components/Visualization/PieChart/PieChart";
import GeoChart from "../../components/Visualization/GeoChart/GeoChart";
import BarChart from "../../components/Visualization/BarChart/BarChart";
import styles from "./Archive.module.scss";

function Archive() {
  const isAuthorized = !!access_token;

  const [analyzeResults, setAnalyzeResults] = useState([]);
  const [selectedSentiments, setSelectedSentiments] = useState([]);
  const [selectedSourceTypes, setSelectedSourceTypes] = useState([]);
  const [selectedSourceUrls, setSelectedSourceUrls] = useState([]);
  const [selectedDates, setSelectedDates] = useState([]);

  const [sourceUrlDropdownOpen, setSourceUrlDropdownOpen] = useState(false);
  const [sourceTypeDropdownOpen, setSourceTypeDropdownOpen] = useState(false);
  const [sentimentDropdownOpen, setSentimentDropdownOpen] = useState(false);
  const [isOtherInfoOpen, setIsOtherInfoOpen] = useState(false);

  useEffect(() => {
    async function fetchAllAnalyzeResults() {
      try {
        const data = await getAllAnalyzeResults();
        if (data) {
          setAnalyzeResults(data);
        }
      } catch (error) {
        console.error(error);
      }
    }

    fetchAllAnalyzeResults();
  }, []);

  const applyFilters = (results) => {
    let filteredResults = [...results];

    if (selectedSentiments.length > 0) {
      filteredResults = filteredResults.filter((result) =>
        selectedSentiments.includes(
          Object.keys(result.full_analyze.sentiments_data.sentiments)[0]
        )
      );
    }

    if (selectedSourceTypes.length > 0) {
      filteredResults = filteredResults.filter((result) =>
        selectedSourceTypes.includes(result.source_type)
      );
    }

    if (selectedSourceUrls.length > 0) {
      filteredResults = filteredResults.filter((result) =>
        selectedSourceUrls.includes(result.source_url)
      );
    }

    if (selectedDates.length > 0) {
      filteredResults = filteredResults.filter((result) =>
        selectedDates.includes(getDateWithoutTime(result.dt))
      );
    }

    return filteredResults;
  };

  const handleSentimentToggle = (sentiment) => {
    const updatedSentiments = selectedSentiments.includes(sentiment)
      ? selectedSentiments.filter((item) => item !== sentiment)
      : [...selectedSentiments, sentiment];
    setSelectedSentiments(updatedSentiments);
  };

  const handleSourceTypeToggle = (type) => {
    const updatedTypes = selectedSourceTypes.includes(type)
      ? selectedSourceTypes.filter((item) => item !== type)
      : [...selectedSourceTypes, type];
    setSelectedSourceTypes(updatedTypes);
  };

  const handleSourceUrlToggle = (url) => {
    const updatedUrls = selectedSourceUrls.includes(url)
      ? selectedSourceUrls.filter((item) => item !== url)
      : [...selectedSourceUrls, url];
    setSelectedSourceUrls(updatedUrls);
  };

  const handleDateToggle = (date) => {
    const updatedDates = selectedDates.includes(date)
      ? selectedDates.filter((item) => item !== date)
      : [...selectedDates, date];
    setSelectedDates(updatedDates);
  };

  const getDateWithoutTime = (dateTimeString) => {
    const date = new Date(dateTimeString);
    const month = date.getDate().toString().padStart(2, "0");
    const day = (date.getMonth() + 1).toString().padStart(2, "0");
    const year = date.getFullYear();
    return `${day}.${month}.${year}`;
  };

  const getUniqueDates = () => {
    const uniqueDates = [];
    analyzeResults.forEach((result) => {
      const date = getDateWithoutTime(result.dt);
      if (!uniqueDates.includes(date)) {
        uniqueDates.push(date);
      }
    });
    return uniqueDates;
  };

  const getUniqueSourceTypes = () => {
    const uniqueSourceTypes = [];
    analyzeResults.forEach((result) => {
      const sourceType = result.source_type;
      if (!uniqueSourceTypes.includes(sourceType)) {
        uniqueSourceTypes.push(sourceType);
      }
    });
    return uniqueSourceTypes;
  };

  const getUniqueSourceUrls = () => {
    const uniqueSourceUrls = [];
    analyzeResults.forEach((result) => {
      const sourceURL = result.source_url;
      if (!uniqueSourceUrls.includes(sourceURL)) {
        uniqueSourceUrls.push(sourceURL);
      }
    });
    return uniqueSourceUrls;
  };

  const getUniqueSentiments = () => {
    const uniqueSentiments = new Set();
    analyzeResults.forEach((result) => {
      const sentiments = result.full_analyze.sentiments_data.sentiments;
      Object.keys(sentiments).forEach((key) => {
        uniqueSentiments.add(key);
      });
    });
    return Array.from(uniqueSentiments);
  };

  const aggregateSentiments = () => {
    const aggregatedSentiments = {
      sentiments: {},
      total: 0,
    };

    analyzeResults.forEach((result) => {
      const sentiments = result.full_analyze.sentiments_data.sentiments;
      Object.entries(sentiments).forEach(([key, value]) => {
        if (!aggregatedSentiments.sentiments[key]) {
          aggregatedSentiments.sentiments[key] = { count: 0, percentage: 0 };
        }
        aggregatedSentiments.sentiments[key].count += value.count;
        aggregatedSentiments.sentiments[key].percentage +=
          value.percentage / 100;
        aggregatedSentiments.total += value.count;
      });
    });

    return aggregatedSentiments;
  };

  const aggregateKeywordCloud = () => {
    const keywordCloud = {};

    analyzeResults.forEach((item) => {
      const currentKeywordCloud = item.full_analyze.keywords_cloud;

      Object.entries(currentKeywordCloud).forEach(([keyword, count]) => {
        if (keywordCloud[keyword]) {
          keywordCloud[keyword] += count;
        } else {
          keywordCloud[keyword] = count;
        }
      });
    });

    const sortedKeywordCloud = Object.entries(keywordCloud)
      .sort((a, b) => b[1] - a[1])
      .slice(0, 20);

    const result = {};
    sortedKeywordCloud.forEach(([keyword, count]) => {
      result[keyword] = count;
    });

    return result;
  };

  const aggregateGeographicalMap = () => {
    const totalGeographicalMap = {};

    analyzeResults.forEach((item) => {
      const geographicalMap = item.full_analyze.geographical_map;

      Object.entries(geographicalMap).forEach(([city, value]) => {
        if (totalGeographicalMap[city]) {
          totalGeographicalMap[city] += value;
        } else {
          totalGeographicalMap[city] = value;
        }
      });
    });

    return totalGeographicalMap;
  };

  const aggregateTopKeywords = () => {
    const keywordCounts = {};

    analyzeResults.forEach((result) => {
      const keywordSentimentCounts =
        result.full_analyze.keyword_sentiment_counts;

      Object.entries(keywordSentimentCounts).forEach(
        ([sentiment, keywords]) => {
          if (!keywordCounts[sentiment]) {
            keywordCounts[sentiment] = {};
          }

          Object.entries(keywords).forEach(([keyword, count]) => {
            if (keywordCounts[sentiment][keyword]) {
              keywordCounts[sentiment][keyword] += count;
            } else {
              keywordCounts[sentiment][keyword] = count;
            }
          });
        }
      );
    });

    const topKeywords = {};
    Object.entries(keywordCounts).forEach(([sentiment, keywords]) => {
      topKeywords[sentiment] = Object.entries(keywords)
        .sort((a, b) => b[1] - a[1])
        .slice(0, 20)
        .reduce((obj, [keyword, count]) => {
          obj[keyword] = count;
          return obj;
        }, {});
    });

    return topKeywords;
  };

  if (!isAuthorized) {
    return (
      <div className={styles.notAuth}>
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

  return (
    <div className={styles.archive}>
      <h3 className={`bold-text center`}>Архив</h3>
      <Helmet>
        <title>MindReview - Архив</title>
      </Helmet>
      <div className={`${styles.visualization} mt50px`}>
        <h3 className={`${styles.visualizationTitle} bold-text`}>
          Визуализация всех проанализированных отзывов
        </h3>
        <div className={styles.up}>
          <BarChart data={aggregateTopKeywords()} />
        </div>
        <div className={styles.bottom}>
          <PieChart data={aggregateSentiments()} />
          <WordCloud
            title={"Топ 20 ключевых слов"}
            keywords={aggregateKeywordCloud()}
          />
          <GeoChart data={aggregateGeographicalMap()} />
        </div>
      </div>
      <h3 className={`${styles.archiveTitle} bold-text`}>
        Архив результатов анализа ({applyFilters(analyzeResults).length})
      </h3>
      <div className={styles.filters}>
        <div className={styles.filterNumber}>
          <h3 className={`bold-text`}>Номер</h3>
        </div>
        <div className={styles.filterDropdown}>
          <div className={styles.customDropdown}>
            <button onClick={() => setIsOtherInfoOpen(!isOtherInfoOpen)}>
              <p className={`bold-text`}>Дата {!isOtherInfoOpen ? "▼" : "▲"}</p>
            </button>
            {isOtherInfoOpen && (
              <div className={styles.dropdownContent}>
                {getUniqueDates().map((date) => (
                  <label className={`dark-text`} key={date}>
                    <input
                      type="checkbox"
                      checked={selectedDates.includes(date)}
                      onChange={() => handleDateToggle(date)}
                    />
                    <p className={styles.text}>{date}</p>
                  </label>
                ))}
              </div>
            )}
          </div>
        </div>
        <div className={styles.filterDropdown}>
          <div className={styles.customDropdown}>
            <button
              onClick={() => setSourceTypeDropdownOpen(!sourceTypeDropdownOpen)}
            >
              <p className={`bold-text`}>
                Тип загрузки {!sourceTypeDropdownOpen ? "▼" : "▲"}
              </p>
            </button>
            {sourceTypeDropdownOpen && (
              <div className={styles.dropdownContent}>
                {getUniqueSourceTypes().map((result) => (
                  <label className={`dark-text`} key={result}>
                    <input
                      type="checkbox"
                      checked={selectedSourceUrls.includes(result)}
                      onChange={() => handleSourceTypeToggle(result)}
                    />
                    <p className={styles.text}>{result}</p>
                  </label>
                ))}
              </div>
            )}
          </div>
        </div>
        <div className={styles.filterDropdown}>
          <div className={styles.customDropdown}>
            <button
              onClick={() => setSourceUrlDropdownOpen(!sourceUrlDropdownOpen)}
            >
              <p className={`bold-text`}>
                Источник загрузки {!sourceUrlDropdownOpen ? "▼" : "▲"}
              </p>
            </button>
            {sourceUrlDropdownOpen && (
              <div className={styles.dropdownContent}>
                {getUniqueSourceUrls().map((result) => (
                  <label className={`dark-text`} key={result}>
                    <input
                      type="checkbox"
                      checked={selectedSourceUrls.includes(result)}
                      onChange={() => handleSourceUrlToggle(result)}
                    />
                    <p className={styles.text}>{result}</p>
                  </label>
                ))}
              </div>
            )}
          </div>
        </div>
        <div className={styles.filterDropdown}>
          <div className={styles.customDropdown}>
            <button
              onClick={() => setSentimentDropdownOpen(!sentimentDropdownOpen)}
            >
              <p className={`bold-text`}>
                Настроение {!sentimentDropdownOpen ? "▼" : "▲"}
              </p>
            </button>
            {sentimentDropdownOpen && (
              <div className={styles.dropdownContent}>
                {getUniqueSentiments().map((result) => (
                  <label className={`dark-text`} key={result}>
                    <input
                      type="checkbox"
                      checked={selectedSentiments.includes(result)}
                      onChange={() => handleSentimentToggle(result)}
                    />
                    <p className={styles.text}>{result}</p>
                  </label>
                ))}
              </div>
            )}
          </div>
        </div>
      </div>
      <div className={styles.results}>
        {applyFilters(analyzeResults).map((analyzeResult, index) => (
          <ArchiveCard
            key={analyzeResult.id}
            cardKey={index + 1}
            analyzeResult={analyzeResult}
          />
        ))}
      </div>
    </div>
  );
}

export default Archive;
