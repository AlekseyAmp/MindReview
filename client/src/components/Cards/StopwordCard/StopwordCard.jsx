import React, { useState } from "react";
import styles from "./FeedbackCard.module.scss";
import OrangeButton from "../../UI/Buttons/OrangeButton/OrangeButton";
import Textarea from "../../UI/Inputs/Textarea/Textarea";
import { set } from "../../../services/data";
import ErrorBox from "../../PopUps/ErrorBox/ErrorBox";
import SuccessBox from "../../PopUps/SuccessBox/SuccessBox";

function StopwordCard({ stopword, refreshStopwords }) {
  const {
    id,
    dt,
    response_dt,
    message,
    response,
    sender_email,
    recipient_email,
  } = feedback;

  const [responseMessage, setResponseMessage] = useState("");
  const [showTextarea, setShowTextarea] = useState(false);
  const [error, setError] = useState(null);
  const [showError, setShowError] = useState(false);
  const [success, setSuccess] = useState(null);
  const [showSuccess, setShowSuccess] = useState(false);

  const toggleTextarea = () => {
    setShowTextarea(!showTextarea);
  };

  const handleReply = async () => {
    if (responseMessage.trim()) {
      const result = await replyFeedback(
        id,
        responseMessage,
        setError,
        setShowError,
        setSuccess,
        setShowSuccess
      );
      if (result) {
        setResponseMessage("");
        setShowTextarea(false);
        refreshFeedbacks();
      }
    } else {
      const errorMessage = "Пожалуйста, напишите ответ.";
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
  };

  return (
    <div className={styles.card}>
      <div className={styles.header}>
        <p className={`gray-text`}>Номер: {id}</p>
        <div className={styles.divider}>
          <div className={styles.from}>
            <p className={`gray-text`}>От: {sender_email}</p>
            <p className={`gray-text`}>{dt}</p>
          </div>
          <div className={styles.to}>
            <p className={`gray-text`}>СП: {recipient_email}</p>
            {response_dt && <p className={`gray-text`}>{response_dt}</p>}
          </div>
        </div>
      </div>
      <div className={styles.content}>
        <p className={`dark-text`}>
          <span className={`bold-text`}>Сообщение:</span> {message}
        </p>
        {response && (
          <p className={`dark-text`}>
            <span className={`bold-text`}>Ответ:</span> {response}
          </p>
        )}
      </div>
      <div className={styles.footer}>
        {!response && (
          <>
            <p className={`purple-link-text`} onClick={toggleTextarea}>
              {showTextarea ? "Скрыть" : "Ответить"}
            </p>
            {showTextarea && (
              <>
                <Textarea
                  value={responseMessage}
                  onChange={(e) => setResponseMessage(e.target.value)}
                  placeholder="Введите ответ..."
                />
                <OrangeButton
                  title={showTextarea ? "Отправить ответ" : "Ответить"}
                  onClick={handleReply}
                />
              </>
            )}
          </>
        )}
      </div>
      {showError && <ErrorBox error={error} />}
      {showSuccess && <SuccessBox success={success} />}
    </div>
  );
}

export default FeedbackCard;
