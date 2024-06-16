import React, { useState } from "react";
import styles from "./StopwordCard.module.scss";
import RedButton from "../../UI/Buttons/RedButton/RedButton";
import OrangeButton from "../../UI/Buttons/OrangeButton/OrangeButton";
import ErrorBox from "../../PopUps/ErrorBox/ErrorBox";
import SuccessBox from "../../PopUps/SuccessBox/SuccessBox";
import { deleteStopword, updateStopwordUsage } from "../../../services/data"; // Ensure these services are defined

function StopwordCard({ stopword, onChange }) {
  const { id, dt, word, use } = stopword;

  const [error, setError] = useState(null);
  const [showError, setShowError] = useState(false);
  const [success, setSuccess] = useState(null);
  const [showSuccess, setShowSuccess] = useState(false);

  const handleDelete = async () => {
    try {
      await deleteStopword(
        id,
        setError,
        setShowError,
        setSuccess,
        setShowSuccess
      );
      onChange(id);
      setShowSuccess(true);
    } catch (err) {
      setShowError(true);
    } finally {
      setTimeout(() => {
        setShowError(false);
        setShowSuccess(false);
      }, 2500);
    }
  };

  const handleChange = async () => {
    try {
      await updateStopwordUsage(
        id,
        setError,
        setShowError,
        setSuccess,
        setShowSuccess
      );
      onChange(id);
    } catch (err) {
      setShowError(true);
    } finally {
      setTimeout(() => {
        setShowError(false);
        setShowSuccess(false);
      }, 2500);
    }
  };

  return (
    <div className={styles.card}>
      <div className={styles.header}>
        <p className={`gray-text`}>Номер: {id}</p>
        <p className={`gray-text`}>{dt}</p>
      </div>
      <div className={styles.content}>
        <p className={`dark-text`}>
          <span className={`bold-text`}>Слово: </span> {word}
        </p>
      </div>
      <div className={styles.footer}>
        <RedButton
          title="Удалить"
          onClick={handleDelete}
          width="150px"
          height="40px"
        />
        <OrangeButton title="Использовать" onClick={handleChange} />
      </div>
      {showError && <ErrorBox error={error} />}
      {showSuccess && <SuccessBox success={success} />}
    </div>
  );
}

export default StopwordCard;
