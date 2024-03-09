import React from "react";

import styles from "./OutlineButton.module.scss";

function OutlineButton({ title, onClick, width, height }) {
  return (
    <div onClick={onClick} className={styles.outlineButton}>
      <button className={styles.button} style={{ width, height }}>
        {title}
      </button>
    </div>
  );
}

export default OutlineButton;
