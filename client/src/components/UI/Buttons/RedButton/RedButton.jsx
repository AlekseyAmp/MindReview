import React from 'react';

import styles from './RedButton.module.scss';

function RedButton({ title, onClick, width, height }) {
  return (
    <div onClick={onClick} className={styles.redButton}>
      <button className={styles.button} style={{ width, height }}>{title}</button>
    </div>
  );
}

export default RedButton;
