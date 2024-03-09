import React, { useState } from "react";
import { Link } from "react-router-dom";

import { access_token } from "../../constants/token";
import PurpleButton from "../UI/Buttons/PurpleButton/PurpleButton";
import OutlineButton from "../UI/Buttons/OutlineButton/OutlineButton";
import Logout from "../Logout/Logout";
import styles from "./Header.module.scss";

function Header() {
  const isAuthorized = !!access_token;
  const [analyzeDropdownOpen, setAnalyzeDropdownOpen] = useState(false);

  return (
    <header>
      <div className={`${styles.header} container`}>
        <div className={styles.logo}>
          <Link to="/">
            <img src="../img/logo.svg" alt="Logo" />
          </Link>
        </div>
        <div className={styles.menu}>
          <ul>
            <li>
              <img src="../img/icons/diagram.svg" alt="analyze" />
              <div
                className={styles.dropDown}
                onMouseEnter={() => setAnalyzeDropdownOpen(true)}
                onMouseLeave={() => setAnalyzeDropdownOpen(false)}
              >
                <div className={styles.customDropdown}>
                  <button>
                    <a className={`link-text`}>
                      Анализ {!analyzeDropdownOpen ? "▼" : "▲"}
                    </a>
                  </button>
                  {analyzeDropdownOpen && (
                    <div className={styles.dropdownContent}>
                      <Link className={`link-text`} to="/analyze/preload">
                        Загрузка отзывов
                      </Link>
                      <Link className={`link-text`} to="/analyze/last">
                        Последний результат анализа
                      </Link>
                    </div>
                  )}
                </div>
              </div>
            </li>
            <li>
              <img src="../img/icons/folder.svg" alt="archive" />
              <Link to="/archive" className={`link-text`}>
                Архив
              </Link>
            </li>
            <li>
              <img src="../img/icons/issue.svg" alt="feedback" />
              <Link to="/feedback" className={`link-text`}>
                Обратная связь
              </Link>
            </li>
          </ul>
        </div>
        <div className={styles.right}>
          <ul>
            {isAuthorized ? (
              <>
                <li>
                  <Link to="/profile">
                    <OutlineButton
                      title="Личный кабинет"
                      width={200}
                      height={40}
                    />
                  </Link>
                </li>
                <li>
                  <Logout />
                </li>
              </>
            ) : (
              <>
                <li>
                  <Link to="/login">
                    <OutlineButton title="Вход" width={200} height={40} />
                  </Link>
                </li>
                <li>
                  <Link to="/register">
                    <PurpleButton title="Регистрация" width={200} height={40} />
                  </Link>
                </li>
              </>
            )}
          </ul>
        </div>
      </div>
    </header>
  );
}

export default Header;
