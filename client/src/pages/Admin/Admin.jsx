import React, { useState, useEffect } from "react";
import { Link } from "react-router-dom";
import { decodeJWT } from "../../utils/token";
import { access_token } from "../../constants/token";

import styles from "./Admin.module.scss";
import { getAllFeedbacks } from "../../services/feedback";
import { getSystemInfo } from "../../services/system";
import FeedbackCard from "../../components/Cards/FeedbackCard/FeedbackCard";

function Admin() {
  const isAuthorized = !!access_token;
  const [feedbacks, setFeedbacks] = useState({ answered: [], unanswered: [] });
  const [systemInfo, setSystemInfo] = useState();
  const decode = decodeJWT(access_token);
  const [updateTrigger, setUpdateTrigger] = useState(false);

  let isAdmin = false;
  if (isAuthorized) {
    isAdmin = decode?.header?.role === "admin";
  }

  const [activeTab, setActiveTab] = useState("stopwords");

  useEffect(() => {
    async function fetchAllFeedbacks() {
      try {
        const data = await getAllFeedbacks();
        if (data) {
          setFeedbacks(data);
        }
      } catch (error) {
        console.error(error);
      }
    }

    if (activeTab === "feedbacks") {
      fetchAllFeedbacks();
    }
  }, [updateTrigger, activeTab]);

  useEffect(() => {
    async function fetchSystemInfo() {
      try {
        const data = await getSystemInfo();
        if (data) {
          setSystemInfo(data);
        }
      } catch (error) {
        console.error(error);
      }
    }

    if (activeTab === "system") {
      fetchSystemInfo();
    }
  }, [activeTab]);

  const refreshFeedbacks = () => {
    setUpdateTrigger((prev) => !prev);
  };

  if (!isAuthorized) {
    return (
      <div className={styles.notAuth}>
        <div className={styles.notAuthData}>
          <h3 className={`${styles.title} dark-text`}>
            <Link className={`purple-text`} to="/login">
              Войдите{" "}
            </Link>{" "}
            или{" "}
            <Link className={`purple-text`} to="/register">
              зарегистрируйтесь
            </Link>
          </h3>
        </div>
      </div>
    );
  }

  if (!isAdmin) {
    return (
      <div className={styles.notAdmin}>
        <div className={styles.notAdminData}>
          <h3 className={`${styles.title} bold-text`}>
            Вы не являетесь администратором.
          </h3>
        </div>
      </div>
    );
  }

  return (
    <div className={styles.admin}>
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
        <div className={styles.tab}>
          <button
            className={`${activeTab === "logs" ? styles.active : ""} gray-text`}
            onClick={() => setActiveTab("logs")}
          >
            Логи приложения
          </button>
        </div>
        <div className={styles.tab}>
          <button
            className={`${
              activeTab === "system" ? styles.active : ""
            } gray-text`}
            onClick={() => setActiveTab("system")}
          >
            О системе
          </button>
        </div>
      </div>
      {activeTab === "users" && <div className={styles.tabContent}>users</div>}
      {activeTab === "feedbacks" && (
        <div className={styles.tabContent}>
          <h3 className={`${styles.title} bold-text`}>Обратная связь</h3>
          <div className={styles.feedbackSections}>
            <div className={styles.answered}>
              <div className={styles.titlee}>
                <img src="../img/icons/done.svg" alt="done" />
                <h3 className="green-text">Отвеченная:</h3>
              </div>
              {feedbacks.answered.map((feedback) => (
                <FeedbackCard feedback={feedback} />
              ))}
            </div>
            <div className={styles.unanswered}>
              <div className={styles.titlee}>
                <img src="../img/icons/wait.svg" alt="wait" />
                <h3 className="orange-text">Неотвеченная:</h3>
              </div>
              {feedbacks.unanswered.map((feedback) => (
                <div key={feedback.id}>
                  <FeedbackCard
                    feedback={feedback}
                    refreshFeedbacks={refreshFeedbacks}
                  />
                </div>
              ))}
            </div>
          </div>
        </div>
      )}
      {activeTab === "stopwords" && (
        <div className={styles.tabContent}>Stopwords management content</div>
      )}
      {activeTab === "logs" && <div className={styles.tabContent}>logs</div>}
      {activeTab === "system" && (
        <div className={styles.tabContent}>
          <h3 className={`${styles.title} bold-text`}>Информация о системе</h3>
          <div className={styles.systemInfoContent}>
            <div className={styles.card}>
              <p className={`purple-text ${styles.cardtitle}`}>
                Общая информация
              </p>
              <div className={styles.cardinfo}>
                <p className={`dark-text`}>
                  Версия приложения: {systemInfo?.version}
                </p>
              </div>
            </div>
            <div className={styles.card}>
              <p className={`purple-text ${styles.cardtitle}`}>Сервер</p>
              <div className={styles.cardinfo}>
                <p className={`dark-text`}>Хост API: {systemInfo?.api_host}</p>
                <p className={`dark-text`}>
                  Документация API: {systemInfo?.api_docs}
                </p>
                <p className={`dark-text`}>
                  Хост WebSocket: {systemInfo?.ws_host}
                </p>
                <p className={`dark-text`}>
                  Хост RabbitMQ: {systemInfo?.rabbitmq_host}
                </p>
              </div>
            </div>
            <div className={styles.card}>
              <p className={`purple-text ${styles.cardtitle}`}>Клиент</p>
              <div className={styles.cardinfo}>
                <p className={`dark-text`}>
                  Хост веб-интерфейса: {systemInfo?.client_host}
                </p>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

export default Admin;
