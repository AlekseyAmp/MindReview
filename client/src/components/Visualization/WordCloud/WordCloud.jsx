import React, { useState, useEffect } from "react";
import ReactWordcloud from "react-wordcloud";
import "tippy.js/dist/tippy.css";
import "tippy.js/animations/scale.css";
import styles from "./WordCloud.module.scss";

function WordCloud({ keywords, title }) {
  const [cloudWidth, setCloudWidth] = useState(1);
  const [cloudHeight, setCloudHeight] = useState(1);

  const numberOfWords = Object.keys(keywords).length;
  const wordCloudData = Object.entries(keywords).map(([word, count]) => ({
    text: word,
    value: count,
  }));

  const handleResize = () => {
    const container = document.getElementById("wordcloud-container");
    if (container) {
      const parentWidth = container.offsetWidth;
      const newWidth = parentWidth < cloudWidth ? parentWidth : cloudWidth;
      setCloudWidth(newWidth);
      setCloudHeight(newWidth);
    }
  };

  useEffect(() => {
    handleResize();
    window.addEventListener("resize", handleResize);

    return () => {
      window.removeEventListener("resize", handleResize);
    };
  }, [cloudWidth]);

  const options = {
    colors: ["#635BFF", "#15966E", "#E56935", "#9C9EA3"],
    enableTooltip: true,
    deterministic: true,
    fontFamily: "Mulish",
    fontSizes: [16, 25],
    fontStyle: "normal",
    fontWeight: "normal",
    padding: 7,
    enableOptimizations: true,
    rotations: 3,
    rotationAngles: [0, 0],
    scale: "linear",
    spiral: "archimedean",
    transitionDuration: 1000,
  };

  return (
    <>
      {wordCloudData.length > 0 ? (
        <div id="wordcloud-container" className={styles.wordcloud}>
          <h3 className={`bold-text`}>
            {title} ({numberOfWords})
          </h3>
          <ReactWordcloud
            words={wordCloudData}
            options={options}
            size={[500, 300]}
          />
        </div>
      ) : (
        <div className={styles.notData}>
          <h3 className={`bold-text`}>
            {title} ({numberOfWords})
          </h3>
          <p className={`dark-text mt35px`} style={{ textAlign: "center" }}>
            Ключевых слов не обнаружено
          </p>
        </div>
      )}
    </>
  );
}

export default WordCloud;
