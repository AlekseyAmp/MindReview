import React from "react";

import styles from "./ErrorBox.module.scss";

function ErrorBox({ error }) {
  return (
    <div className={styles.errorBox}>
      <span className={`white-text`} style={{ fontWeight: "bold" }}>
        {error}
      </span>
    </div>
  );
}

export default ErrorBox;
