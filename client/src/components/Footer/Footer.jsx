import React from "react";
import { Link } from "react-router-dom";

import styles from "./Footer.module.scss";

function Footer() {
  return (
    <footer>
      <div className={styles.footer}>
        <div className={styles.menu}>
          <ul>
            <li>
              <Link to="/analyze" className={`link-text`}>
                Анализ
              </Link>
            </li>
            <li>
              <Link to="/archive" className={`link-text`}>
                Архив
              </Link>
            </li>
            <li>
              <Link to="/profile" className={`link-text`}>
                Личный кабинет
              </Link>
            </li>
            <li>
              <Link to="/feedback" className={`link-text`}>
                Обратная связь
              </Link>
            </li>
          </ul>
        </div>
        <div className={styles.menu}>
          <ul>
            <li>
              <p className={`gray-text`}>info@mindreview.ru</p>
            </li>
            <li>
              <p className={`gray-text`}>+7(999)-999-99-99</p>
            </li>
          </ul>
        </div>
      </div>
    </footer>
  );
}

export default Footer;
