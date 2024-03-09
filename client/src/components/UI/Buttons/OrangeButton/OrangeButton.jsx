import React from "react";

import styles from "./OrangeButton.module.scss";

function OrangeButton({ title, onClick, width, height }) {
  return (
    <div onClick={onClick} className={styles.orangeButton}>
      <button className={styles.button} style={{ width, height }}>
        {title}
      </button>
    </div>
  );
}

export default OrangeButton;
