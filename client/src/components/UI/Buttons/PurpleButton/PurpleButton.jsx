import React from 'react';

import styles from './PurpleButton.module.scss';

function PurpleButton({ title, onClick, width, height }) {
  return (
    <div onClick={onClick} className={styles.purpleButton}>
      <button className={styles.button} style={{ width, height }}>{title}</button>
    </div>
  );
}

export default PurpleButton;
