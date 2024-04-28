import React from "react";
import styles from "./LogCard.module.scss";

function LogCard({ log }) {
  const { id, dt, level, message } = log;

  return (
    <div className={styles.card}>
      <div className={styles.header}>
        <p className={`gray-text`}>Номер: {id}</p>
        <p className={`gray-text`}>{dt}</p>
      </div>
      <div className={styles.content}>
        <p className={`dark-text`}>
          <span className={`bold-text`}>Уровень:</span> {level}
        </p>
        <p className={`dark-text`}>
          <span className={`bold-text`}>Сообщение:</span> {message}
        </p>
      </div>
    </div>
  );
}

export default LogCard;
