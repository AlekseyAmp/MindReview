import React, { useState } from "react";
import { decodeJWT } from "../../utils/token";
import { access_token } from "../../constants/token";

import styles from "./Admin.module.scss";

function Admin() {
  const token = access_token;
  const decode = decodeJWT(token);
  const isAdmin = decode.header.role === "admin";
  const [activeTab, setActiveTab] = useState("stopwords");

  return (
    <div className={styles.admin}>
      {isAdmin ? (
        <>
          <h3 className={`${styles.title} bold-text`}>
            Выберите способ загрузки отзывов
          </h3>
          <div className={styles.tabs}>
            <div className={styles.tab}>
              <button
                className={`${
                  activeTab === "users" ? styles.active : ""
                } gray-text`}
                onClick={() => setActiveTab("users")}
              >
                Управление пользователями
              </button>
            </div>
            <div className={styles.tab}>
              <button
                className={`${
                  activeTab === "feedbacks" ? styles.active : ""
                } gray-text`}
                onClick={() => setActiveTab("feedbacks")}
              >
                Управление обратной связью
              </button>
            </div>
            <div className={styles.tab}>
              <button
                className={`${
                  activeTab === "stopwords" ? styles.active : ""
                } gray-text`}
                onClick={() => setActiveTab("stopwords")}
              >
                Управление стоп-словами
              </button>
            </div>
          </div>
          {activeTab === "users" && (
            <div className={styles.tabContent}>users</div>
          )}
          {activeTab === "feedbacks" && (
            <div className={styles.tabContent}>feedbacks</div>
          )}
          {activeTab === "stopwords" && (
            <div className={styles.tabContent}>stropwords</div>
          )}
        </>
      ) : (
        <div>Вы не являетесь администратором</div>
      )}
    </div>
  );
}

export default Admin;
