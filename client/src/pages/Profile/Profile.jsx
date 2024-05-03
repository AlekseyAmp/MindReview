import React, { useEffect, useState } from "react";
import { Helmet } from "react-helmet";
import { Link, useNavigate } from "react-router-dom";
import styles from "./Profile.module.scss";
import { access_token } from "../../constants/token";
import { deleteUser, getUserById, editUser } from "../../services/user";
import { getAllAnalyzeResults } from "../../services/analyze";
import { logoutUser } from "../../services/auth";
import ErrorBox from "../../components/PopUps/ErrorBox/ErrorBox";
import SuccessBox from "../../components/PopUps/SuccessBox/SuccessBox";
import OrangeButton from "../../components/UI/Buttons/OrangeButton/OrangeButton";
import RedButton from "../../components/UI/Buttons/RedButton/RedButton";
import PurpleButton from "../../components/UI/Buttons/PurpleButton/PurpleButton";
import Input from "../../components/UI/Inputs/Input/Input";
import { decodeJWT } from "../../utils/token";

function Profile() {
  const isAuthorized = !!access_token;
  const [success, setSuccess] = useState(null);
  const [showSuccess, setShowSuccess] = useState(false);
  const [error, setError] = useState(null);
  const [showError, setShowError] = useState(false);
  const [firstName, setFirstName] = useState("");
  const [lastName, setLastName] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [showDeleteModal, setShowDeleteModal] = useState(false);
  const navigate = useNavigate();
  const [analyzeResults, setAnalyzeResults] = useState([]);

  const decode = decodeJWT(access_token);

  if (!isAuthorized) {
    return (
      <div className={styles.notAuth}>
        <Helmet>
          <title>MindReview - Профиль</title>
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

  let userId = null;
  if (isAuthorized) {
    userId = decode.payload.sub;
  }

  let isPremium = false;
  if (isAuthorized) {
    isPremium = decode.header.is_premium;
  }

  const handleEditUser = async () => {
    const edited = await editUser(
      userId,
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

  const toggleDeleteModal = () => {
    setShowDeleteModal(!showDeleteModal);
  };

  const handleDeleteUser = async () => {
    try {
      const deleted = await deleteUser(userId);
      if (deleted) {
        logoutUser(setError, setShowError, navigate);
      } else {
            // Дополнительные действия при неудачном удалении пользователя
      }
    } catch (error) {
      // Обработка ошибок удаления пользователя
      console.error("Error deleting user:", error);
    }
  };

  useEffect(() => {
    const fetchUserData = async () => {
      try {
        const user = await getUserById(userId);
        setFirstName(user.first_name);
        setLastName(user.last_name);
        setEmail(user.email);
      } catch (error) {
        console.error(error);
      }
    };

    fetchUserData();
  }, [userId]);

  useEffect(() => {
    async function fetchAllAnalyzeResults() {
      try {
        const data = await getAllAnalyzeResults();
        if (data) {
          setAnalyzeResults(data);
        }
      } catch (error) {
        console.error(error);
      }
    }

    fetchAllAnalyzeResults();
  }, []);

  const aggregateSentiments = () => {
    const aggregatedSentiments = {
      sentiments: {},
      total: 0,
    };

    analyzeResults.forEach((result) => {
      const sentiments = result.full_analyze.sentiments_data.sentiments;
      Object.entries(sentiments).forEach(([key, value]) => {
        if (!aggregatedSentiments.sentiments[key]) {
          aggregatedSentiments.sentiments[key] = { count: 0, percentage: 0 };
        }
        aggregatedSentiments.sentiments[key].count += value.count;
        aggregatedSentiments.sentiments[key].percentage +=
          value.percentage / 100;
        aggregatedSentiments.total += value.count;
      });
    });
    return aggregatedSentiments;
  };
  const positiveCount =
    aggregateSentiments().sentiments["Позитивный"]?.count || 0;
  const negativeCount =
    aggregateSentiments().sentiments["Негативный"]?.count || 0;
  const neutralCount =
    aggregateSentiments().sentiments["Нейтральный"]?.count || 0;
  return (
    <div className={styles.profile}>
      <Helmet>
        <title>MindReview - Личный кабинет</title>
      </Helmet>
      <h3 className={`bold-text center`}>Личный кабинет</h3>
      <div className={styles.content}>
        <div className={styles.userInfo}>
          <h3 className={`gray-text`}>
            Здесь Вы можете поменять о себе данные.
          </h3>
          <div className={styles.edit}>
            {isPremium && (
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
                value={firstName}
                onChange={(e) => setFirstName(e.target.value)}
                width={"200px"}
                height={"30px"}
              />
              <Input
                title={"Фамилия"}
                type={"text"}
                name={"last_name"}
                value={lastName}
                onChange={(e) => setLastName(e.target.value)}
                width={"200px"}
                height={"30px"}
              />
            </div>
            <div className={styles.twoInputs}>
              <Input
                title={"Email"}
                type={"email"}
                name={"email"}
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                width={"440px"}
                height={"30px"}
              />
              <Input
                title={"Пароль"}
                type={"password"}
                name={"password"}
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                width={"440px"}
                height={"30px"}
              />
            </div>
            <PurpleButton
              title={"Сохранить"}
              onClick={handleEditUser}
              width={460}
              height={40}
            />
          </div>
          <div className={styles.buttons}>
            <div className={styles.buttons}>
              {!isPremium && (
                <div className={styles.premium}>
                  <Link to="/premium">
                    <OrangeButton
                      title="Купить премиум подписку"
                      width={250}
                      height={40}
                    />
                  </Link>
                </div>
              )}
              <div className={styles.delete}>
                <RedButton
                  title={"Удалить аккаунт"}
                  onClick={toggleDeleteModal}
                  width={200}
                  height={40}
                />
              </div>
            </div>
          </div>
        </div>
        <div className={styles.statistic}>
          <h3 className={`purple-text`}>
            За всё время было проанализировано {aggregateSentiments().total}{" "}
            отзывов
          </h3>
          <div className={styles.statisticContent}>
            <p className={`lettuce-text`}>Положительные: {positiveCount}</p>
            <p className={`orange-text`}>Нейтральные: {neutralCount}</p>
            <p className={`red-text`}>Негативные: {negativeCount}</p>
          </div>
          <div className={styles.archive}>
            <Link to="/archive">
              <OrangeButton title="Перейти в архив" width={400} height={40} />
            </Link>
          </div>
        </div>
      </div>
      {showError && <ErrorBox error={error} />}
      {showSuccess && <SuccessBox success={success} />}

      {showDeleteModal && (
        <div className={styles.modal}>
          <div className={styles.modalContent}>
            <h2 className={`dark-text`}>
              Вы точно хотите удалить свой аккаунт?
            </h2>
            <div className={styles.modalButtons}>
              <OrangeButton
                title={"Отмена"}
                onClick={toggleDeleteModal}
                width={100}
                height={40}
              />
              <RedButton
                title={"Удалить"}
                onClick={handleDeleteUser}
                width={100}
                height={40}
              />
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

export default Profile;
