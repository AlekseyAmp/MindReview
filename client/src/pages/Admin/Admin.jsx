import React, { useState, useEffect } from "react";
import { Link } from "react-router-dom";
import { decodeJWT } from "../../utils/token";
import { access_token } from "../../constants/token";
import { Helmet } from "react-helmet";

import styles from "./Admin.module.scss";
import { getAllFeedbacks } from "../../services/feedback";
import { getSystemInfo, getAllLogs } from "../../services/system";
import { getAllUsers, editUser, deleteUser } from "../../services/user";
import {
  getAllStopwords,
  updateStopwordUsage,
  deleteStopword,
} from "../../services/data";
import FeedbackCard from "../../components/Cards/FeedbackCard/FeedbackCard";
import StopwordCard from "../../components/Cards/StopwordCard/StopwordCard";
import LogCard from "../../components/Cards/LogCard/LogCard";
import Input from "../../components/UI/Inputs/Input/Input";
import PurpleButton from "../../components/UI/Buttons/PurpleButton/PurpleButton";
import RedButton from "../../components/UI/Buttons/RedButton/RedButton";
import OrangeButton from "../../components/UI/Buttons/OrangeButton/OrangeButton";
import ErrorBox from "../../components/PopUps/ErrorBox/ErrorBox";
import SuccessBox from "../../components/PopUps/SuccessBox/SuccessBox";

function Admin() {
  const isAuthorized = !!access_token;
  const [feedbacks, setFeedbacks] = useState({ answered: [], unanswered: [] });
  const [systemInfo, setSystemInfo] = useState();
  const [stopwords, setStopwords] = useState([]);
  const [logs, setLogs] = useState([]);
  const decode = decodeJWT(access_token);
  const [updateTrigger, setUpdateTrigger] = useState(false);
  const [users, setUsers] = useState([]);
  const [firstName, setFirstName] = useState("");
  const [lastName, setLastName] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [showDeleteModal, setShowDeleteModal] = useState(false);
  const [success, setSuccess] = useState(null);
  const [showSuccess, setShowSuccess] = useState(false);
  const [error, setError] = useState(null);
  const [showError, setShowError] = useState(false);
  const [userStates, setUserStates] = useState([]);
  const [userIdToDelete, setUserIdToDelete] = useState(null);

  let isAdmin = false;
  if (isAuthorized) {
    isAdmin = decode?.header?.role === "admin";
  }

  if (!isAuthorized) {
    return (
      <div className={styles.notAuth}>
        <Helmet>
          <title>MindReview - Админ панель</title>
        </Helmet>
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
        <Helmet>
          <title>MindReview - Админ панель</title>
        </Helmet>
        <div className={styles.notAdminData}>
          <h3 className={`${styles.title} bold-text`}>
            Вы не являетесь администратором.
          </h3>
        </div>
      </div>
    );
  }

  const [activeTab, setActiveTab] = useState("stopwords");

  useEffect(() => {
    async function fetchAllUsers() {
      try {
        const data = await getAllUsers();
        if (data) {
          setUsers(data);
        }
      } catch (error) {
        console.error(error);
      }
    }

    if (activeTab === "users") {
      fetchAllUsers();
    }
  }, [activeTab]);

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
    async function fetchAllStopwords() {
      try {
        const data = await getAllStopwords();
        if (data) {
          setStopwords(data);
        }
      } catch (error) {
        console.error(error);
      }
    }

    if (activeTab === "stopwords") {
      fetchAllStopwords();
    }
  }, [activeTab]);

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

  useEffect(() => {
    async function fetchAllLogs() {
      try {
        const data = await getAllLogs();
        if (data) {
          setLogs(data);
        }
      } catch (error) {
        console.error(error);
      }
    }

    if (activeTab === "logs") {
      fetchAllLogs();
    }
  }, [activeTab]);

  useEffect(() => {
    // Создаем состояние для каждого пользователя при загрузке компонента
    setUserStates(
      users.map((user) => ({
        id: user.id,
        firstName: user.first_name,
        lastName: user.last_name,
        email: user.email,
      }))
    );
  }, [users]);

  const handleInputChange = (userId, field, value) => {
    setUserStates((prevStates) =>
      prevStates.map((state) => {
        if (state.id === userId) {
          // Обновляем только поле, которое изменилось
          return { ...state, [field]: value };
        }
        return state;
      })
    );
  };
  const handleEditUser = async (user_id, userData) => {
    const { firstName, lastName, email } = userData;
    const edited = await editUser(
      user_id,
      firstName,
      lastName,
      email,
      setError,
      setShowError,
      setSuccess,
      setShowSuccess
    );
    if (edited) {
      // Дополнительные действия при успешном изменении пользователя
    } else {
      // Дополнительные действия при неудачном изменении пользователя
    }
  };

  const toggleDeleteModal = (userId) => {
    setUserIdToDelete(userId);
    setShowDeleteModal(!showDeleteModal);
  };

  const handleChangeStopword = (id) => {
    setStopwords((prevStopwords) =>
      prevStopwords.filter((stopword) => stopword.id !== id)
    );
  };

  const refreshFeedbacks = () => {
    setUpdateTrigger((prev) => !prev);
  };

  const handleDeleteUser = async (userId) => {
    try {
      const deleted = await deleteUser(userId);
      if (deleted) {
        setUsers((prevUsers) => prevUsers.filter((user) => user.id !== userId));
        // Дополнительные действия после успешного удаления пользователя
        setShowDeleteModal(false); // Закрыть модальное окно после удаления
        setSuccess(`Вы удалили пользователя с идентификатором ${userId}.`);
        setShowSuccess(true);
        setTimeout(() => {
          setShowSuccess(false);
          setSuccess(null);
        }, 2500);
      } else {
        // Дополнительные действия при неудачном удалении пользователя
      }
    } catch (error) {
      // Обработка ошибок удаления пользователя
      console.error("Error deleting user:", error);
    }
  };

  return (
    <div className={styles.admin}>
      <Helmet>
        <title>MindReview - Админ панель</title>
      </Helmet>
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
      {activeTab === "users" && (
        <div className={styles.tabContent}>
          <h3 className={`${styles.title} bold-text`}>
            Управление пользователями
          </h3>
          <div className={styles.users}>
            {users.length === 0 ? (
              <p className={`dark-text`}>Нет данных</p>
            ) : (
              users.map((user) => (
                <div key={user.id} className={styles.edit}>
                  {user.is_premium && (
                    <div className={styles.premiumStatus}>
                      <img src="../img/icons/done.svg" alt="done" />
                      <p className={`green-text`}>Премиум пользователь.</p>
                    </div>
                  )}
                  <div className={styles.oneInputs}>
                    <Input
                      title={"Имя"}
                      type={"text"}
                      name={"first_name"}
                      value={
                        userStates.find((state) => state.id === user.id)
                          ?.firstName || ""
                      }
                      onChange={(e) =>
                        handleInputChange(user.id, "firstName", e.target.value)
                      }
                      width={"200px"}
                      height={"30px"}
                    />
                    <Input
                      title={"Фамилия"}
                      type={"text"}
                      name={"last_name"}
                      value={
                        userStates.find((state) => state.id === user.id)
                          ?.lastName || ""
                      }
                      onChange={(e) =>
                        handleInputChange(user.id, "lastName", e.target.value)
                      }
                      width={"200px"}
                      height={"30px"}
                    />
                  </div>
                  <div className={styles.twoInputs}>
                    <Input
                      title={"Email"}
                      type={"email"}
                      name={"email"}
                      value={
                        userStates.find((state) => state.id === user.id)
                          ?.email || ""
                      }
                      onChange={(e) =>
                        handleInputChange(user.id, "email", e.target.value)
                      }
                      width={"440px"}
                      height={"30px"}
                    />
                  </div>
                  <div className={styles.buttons}>
                    <PurpleButton
                      title={"Сохранить"}
                      onClick={() =>
                        handleEditUser(user.id, {
                          firstName:
                            userStates.find((state) => state.id === user.id)
                              ?.firstName || "",
                          lastName:
                            userStates.find((state) => state.id === user.id)
                              ?.lastName || "",
                          email:
                            userStates.find((state) => state.id === user.id)
                              ?.email || "",
                        })
                      }
                      width={220}
                      height={40}
                    />
                    <RedButton
                      title={"Удалить аккаунт"}
                      onClick={() => toggleDeleteModal(user.id)}
                      width={220}
                      height={40}
                    />
                  </div>
                </div>
              ))
            )}
          </div>
        </div>
      )}
      {activeTab === "feedbacks" && (
        <div className={styles.tabContent}>
          <h3 className={`${styles.title} bold-text`}>Обратная связь</h3>
          <div className={styles.feedbackSections}>
            <div className={styles.answered}>
              <div className={styles.titlee}>
                <img src="../img/icons/done.svg" alt="done" />
                <h3 className="green-text">Отвеченная:</h3>
              </div>
              {feedbacks.answered.length > 0 ? (
                feedbacks.answered.map((feedback) => (
                  <FeedbackCard key={feedback.id} feedback={feedback} />
                ))
              ) : (
                <p className={`dark-text mt35px`}>Нет данных</p>
              )}
            </div>
            <div className={styles.unanswered}>
              <div className={styles.titlee}>
                <img src="../img/icons/wait.svg" alt="wait" />
                <h3 className="orange-text">Неотвеченная:</h3>
              </div>
              {feedbacks.unanswered.length > 0 ? (
                feedbacks.unanswered.map((feedback) => (
                  <div key={feedback.id}>
                    <FeedbackCard
                      feedback={feedback}
                      refreshFeedbacks={refreshFeedbacks}
                    />
                  </div>
                ))
              ) : (
                <p className={`dark-text mt35px`}>Нет данных</p>
              )}
            </div>
          </div>
        </div>
      )}
      {activeTab === "stopwords" && (
        <div className={styles.tabContent}>
          <h3 className={`${styles.title} bold-text`}>Стоп-слова</h3>
          <div className={styles.stopwordsSection}>
            {stopwords.length > 0 ? (
              stopwords.map((stopword) => (
                <div key={stopword.id}>
                  <StopwordCard
                    stopword={stopword}
                    onChange={handleChangeStopword}
                  />
                </div>
              ))
            ) : (
              <p className={`dark-text mt35px`}>Нет данных</p>
            )}
          </div>
        </div>
      )}
      {activeTab === "logs" && (
        <div className={styles.tabContent}>
          <h3 className={`${styles.title} bold-text`}>Логи приложения</h3>
          {logs.length > 0 ? (
            logs.map((log) => <LogCard key={log.id} log={log} />)
          ) : (
            <p className={`dark-text`}>Нет данных</p>
          )}
        </div>
      )}
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
                  <span className={`bold-text`}>Версия приложения:</span>{" "}
                  {systemInfo?.version}
                </p>
              </div>
            </div>
            <div className={styles.card}>
              <p className={`purple-text ${styles.cardtitle}`}>Сервер</p>
              <div className={styles.cardinfo}>
                <p className={`dark-text`}>
                  <span className={`bold-text`}>Хост API:</span>{" "}
                  {systemInfo?.api_host}
                </p>
                <p className={`dark-text`}>
                  <span className={`bold-text`}>Документация API:</span>{" "}
                  {systemInfo?.api_docs}
                </p>
                <p className={`dark-text`}>
                  <span className={`bold-text`}>Хост WebSocket:</span>{" "}
                  {systemInfo?.ws_host}
                </p>
                <p className={`dark-text`}>
                  <span className={`bold-text`}>Хост RabbitMQ:</span>{" "}
                  {systemInfo?.rabbitmq_host}
                </p>
              </div>
            </div>
            <div className={styles.card}>
              <p className={`purple-text ${styles.cardtitle}`}>Клиент</p>
              <div className={styles.cardinfo}>
                <p className={`dark-text`}>
                  <span className={`bold-text`}>Хост веб-интерфейса:</span>{" "}
                  {systemInfo?.client_host}
                </p>
              </div>
            </div>
          </div>
        </div>
      )}
      {showDeleteModal && (
        <div className={styles.modal}>
          <div className={styles.modalContent}>
            <h2 className={`dark-text`}>Вы точно хотите удалить аккаунт?</h2>
            <div className={styles.modalButtons}>
              <OrangeButton
                title={"Отмена"}
                onClick={toggleDeleteModal}
                width={100}
                height={40}
              />
              <RedButton
                title={"Удалить"}
                onClick={() => handleDeleteUser(userIdToDelete)}
                width={100}
                height={40}
              />
            </div>
          </div>
        </div>
      )}
      {showError && <ErrorBox error={error} />}
      {showSuccess && <SuccessBox success={success} />}
    </div>
  );
}

export default Admin;
