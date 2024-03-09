import React from "react";
import { Chart } from "react-google-charts";

import styles from "./PieChart.module.scss";

function PieChart({ data }) {
  const colorsMap = [
    { sentiment: "Позитивный", color: "#90BE6D" },
    { sentiment: "Нейтральный", color: "#E56935" },
    { sentiment: "Негативный", color: "#df1916" },
  ];

  const totalSentiments = data.total;

  // Формирование данных для графика
  const chartData = [
    [
      "Настроение",
      "Количество",
      { role: "tooltip", type: "string", p: { html: true } },
    ],
  ];
  colorsMap.forEach((colorItem) => {
    const sentiment = colorItem.sentiment;
    const sentimentData = data.sentiments[sentiment];
    if (sentimentData) {
      const { count, percentage } = sentimentData;
      const tooltip = `<div style="padding: 5px; border-radius: 7px; font-size: 14px; font-family: 'Mulish'; color: #635BFF"><b>${sentiment}</b><br/>Количество: ${count}<br/>Процент: ${percentage}%</div>`;
      chartData.push([sentiment, count, tooltip]);
    }
  });

  // Опции для графика
  const options = {
    title: `Круговая диаграмма настроений (${totalSentiments})`,
    titleTextStyle: {
      color: "#221F1F",
      fontName: "Mulish, sans-serif",
      fontSize: 17,
      textAlign: "center",
      bold: true,
    },
    colors: colorsMap
      .map((colorItem) =>
        data.sentiments[colorItem.sentiment] ? colorItem.color : "#000"
      )
      .filter((color) => color !== "#000"),
    pieSliceText: "value-and-percentage",
    pieSliceTextStyle: {
      color: "#221F1F",
      fontName: "Mulish",
      fontSize: 14,
      bold: true,
    },
    legend: {
      textStyle: {
        color: "#221F1F",
        fontName: "Mulish",
        fontSize: 13,
      },
      position: "bottom",
    },
    tooltip: {
      isHtml: true,
    },
  };

  // Стиль графика
  const chartStyle = {
    width: "570px",
    height: "450px",
    padding: "-50px",
  };

  return (
    <div className={styles.pieChart}>
      <Chart
        chartType="PieChart"
        data={chartData}
        options={options}
        style={chartStyle}
      />
    </div>
  );
}

export default PieChart;
