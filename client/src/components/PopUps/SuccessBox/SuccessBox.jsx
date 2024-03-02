import React from 'react';

import styles from './SuccessBox.module.scss';

function SuccessBox({ success }) {
    return (
      <div className={styles.successBox}>
        <span className={`white-text`} style={{fontWeight: 'bold'}}>{success}</span>
      </div>
    );
  }
  

export default SuccessBox