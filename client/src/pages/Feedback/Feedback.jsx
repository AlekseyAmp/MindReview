import React, { useState } from "react";
import { Helmet } from "react-helmet";
import { Link } from "react-router-dom";
import { sendFeedback } from "../../services/feedback";
import { access_token } from "../../constants/token";
import styles from "./Feedback.module.scss";
import Textarea from "../../components/UI/Inputs/Textarea/Textarea";
import Input from "../../components/UI/Inputs/Input/Input";
import PurpleButton from "../../components/UI/Buttons/PurpleButton/PurpleButton";
import ErrorBox from "../../components/PopUps/ErrorBox/ErrorBox";
import SuccessBox from "../../components/PopUps/SuccessBox/SuccessBox";

function Feedback() {
  const isAuthorized = !!access_token;

  const [email, setEmail] = useState("");
  const [message, setMessage] = useState("");
  const [error, setError] = useState(null);
  const [showError, setShowError] = useState(false);
  const [success, setSuccess] = useState(null);
  const [showSuccess, setShowSuccess] = useState(false);
  const [isSubmitting, setIsSubmitting] = useState(false);

  if (!isAuthorized) {
    return (
      <div className={styles.notAuth}>
        <Helmet>
          <title>MindReview - Обратная связь</title>
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

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!email || !message) {
      const errorMessage = "Пожалуйста, заполните все поля.";
      setError(errorMessage);
      setShowError(true);
      setSuccess(null);
      setShowSuccess(false);
      setTimeout(() => {
        setShowError(false);
        setError(null);
      }, 2500);
      return;
    }
    const data = await sendFeedback(
      email,
      message,
      setError,
      setShowError,
      setSuccess,
      setShowSuccess
    );
    if (data) {
      setEmail("");
      setMessage("");
      setSuccess("Письмо отправлено на почту " + email);
      setShowSuccess(true);
      setTimeout(() => {
        setShowSuccess(false);
        setSuccess(null);
        setIsSubmitting(false);
      }, 2500);
    }
  };

  return (
    <div className={styles.feedback}>
      <Helmet>
        <title>MindReview - Обратная связь</title>
      </Helmet>
      <div className={styles.feedbackContent}>
        <img src="../img/feedback/feedback.png" alt="feedback" />
        <div className={styles.feedbackRight}>
          <h3 className={`bold-text`}>Обратная связь</h3>
          <p className={`gray-text mt35px`}>
            Мы ценим ваше мнение! Если у вас есть предложения по улучшению
            сервиса, <br />
            замечания по поводу работы или вы обнаружили какие-то технические
            неполадки, <br />
            не стесняйтесь сообщить нам. Ваши отзывы помогут нам сделать
            MindReview еще лучше. <br />
          </p>
          <form onSubmit={handleSubmit}>
            <div className={`${styles.inputBox} mt35px`}>
              <Input
                title={"Адрес электронной почты"}
                type={"email"}
                name={"email"}
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                width={"250px"}
                height={"30px"}
              />
              <Textarea
                title={"Что бы хотели улучшить/исправить?"}
                name={"message"}
                value={message}
                onChange={(e) => setMessage(e.target.value)}
                width={702}
                height={188}
              />
              <PurpleButton
                title={"Отправить"}
                width={383}
                height={37}
                onClick={isSubmitting ? undefined : handleSubmit}
              />
            </div>
          </form>
        </div>
      </div>
      {showError && <ErrorBox error={error} />}
      {showSuccess && <SuccessBox success={success} />}
    </div>
  );
}

export default Feedback;
