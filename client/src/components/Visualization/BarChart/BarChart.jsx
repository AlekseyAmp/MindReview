import React, { useState, useEffect } from "react";
import { Chart } from "react-google-charts";

import styles from "./BarChart.module.scss";

function BarChart({ data }) {
  const colorsMap = [
    { sentiment: "Позитивный", color: "#90BE6D" },
    { sentiment: "Нейтральный", color: "#E56935" },
    { sentiment: "Негативный", color: "#df1916" },
  ];

  const [showFullChart, setShowFullChart] = useState(false);
  const [showLimitedChart, setShowLimitedChart] = useState(true);
  const [fullChartHeight, setFullChartHeight] = useState("auto");
  const [chartTitle, setChartTitle] = useState(
    "Анализ настроений по ключевым словам (10 самых популярных)"
  );

  const allWords = Object.values(data).flatMap((sentiment) =>
    Object.keys(sentiment)
  );
  const uniqueWords = [...new Set(allWords)].sort((a, b) => {
    const totalOccurrencesA = colorsMap.reduce(
      (acc, { sentiment }) => acc + (data[sentiment]?.[a] || 0),
      0
    );
    const totalOccurrencesB = colorsMap.reduce(
      (acc, { sentiment }) => acc + (data[sentiment]?.[b] || 0),
      0
    );
    return totalOccurrencesB - totalOccurrencesA;
  });

  const limitedWords = uniqueWords.slice(0, 10);
  const topWords = limitedWords;

  const chartData = topWords.map((word) => {
    const values = colorsMap.map(
      ({ sentiment }) => data[sentiment]?.[word] || 0
    );
    return [word, ...values];
  });

  useEffect(() => {
    if (showFullChart) {
      setFullChartHeight(`${uniqueWords.length * 30}px`);
    }
  }, [showFullChart, uniqueWords]);

  const options = {
    title: chartTitle,
    titleTextStyle: {
      color: "#221F1F",
      fontName: "Mulish, sans-serif",
      fontSize: 17,
      bold: true,
    },
    hAxis: {
      textStyle: {
        fontSize: 14,
        bold: false,
        fontFace: "Mulish",
        color: "#221F1F",
      },
    },
    vAxis: {
      title: "Ключевые слова",
      titleTextStyle: {
        color: "#221F1F",
        fontName: "Mulish, sans-serif",
        fontSize: 15,
        bold: true,
        italic: false,
      },
      textStyle: {
        fontSize: 12,
        bold: true,
        fontFace: "Mulish",
        color: "#9C9EA3",
      },
    },
    colors: colorsMap.map((item) => item.color),
    bar: { groupWidth: "50%" },
    chartArea: {
      left: "15%",
      top: "10%",
      bottom: "10%",
      width: "auto",
      height: fullChartHeight,
    },
    tooltip: {
      textStyle: {
        color: "#635BFF",
        fontName: "Mulish",
        fontSize: 14,
        bold: false,
      },
    },
    legend: {
      textStyle: {
        color: "#221F1F",
        fontName: "Mulish",
        fontSize: 14,
      },
      position: "right",
    },
  };

  const handleToggleChart = () => {
    setShowFullChart(!showFullChart);
    setChartTitle("Анализ настроений по ключевым словам");
  };

  const handleCloseFullChart = () => {
    setShowFullChart(false);
    setShowLimitedChart(true);
    setChartTitle("Анализ настроений по ключевым словам (10 самых популярных)");
  };

  return (
    <div
      className={styles.barChart}
      style={{ width: "fit-content", height: "fit-content" }}
    >
      {Object.keys(data).every((key) => Object.keys(data[key]).length === 0) ? (
        <div className={styles.notData}>
          <h3 className={`bold-text`}>{chartTitle}</h3>
          <p className={`${styles.notFound} dark-text`}>
            Нет данных для отображения
          </p>
        </div>
      ) : (
        <>
          {showLimitedChart && (
            <Chart
              chartType="BarChart"
              width="970px"
              height="650px"
              data={[
                ["Слово", "Позитивный", "Нейтральный", "Негативный"],
                ...chartData,
              ]}
              options={options}
            />
          )}
          {showFullChart && uniqueWords.length > 10 && (
            <div className={styles.fullChartOverlay}>
              <div className={styles.fullChartContainer}>
                <Chart
                  chartType="BarChart"
                  width="100%"
                  height={fullChartHeight}
                  data={[
                    ["Слово", "Позитивный", "Нейтральный", "Негативный"],
                    ...uniqueWords.map((word) => [
                      word,
                      ...colorsMap.map(
                        ({ sentiment }) => data[sentiment]?.[word] || 0
                      ),
                    ]),
                  ]}
                  options={options}
                />
                <p className={`link-text`} onClick={handleCloseFullChart}>
                  Закрыть ✖
                </p>
              </div>
            </div>
          )}
          <div style={{ textAlign: "center", marginTop: "10px" }}>
            {showLimitedChart && uniqueWords.length > 10 && (
              <h3
                className={`${styles.title} gray-text`}
                onClick={handleToggleChart}
              >
                Показать весь график ▼
              </h3>
            )}
          </div>
        </>
      )}
    </div>
  );
}

export default BarChart;
