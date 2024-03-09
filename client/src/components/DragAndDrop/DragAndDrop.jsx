import React, { useState } from "react";
import { useDropzone } from "react-dropzone";

import { uploadFile } from "../../services/analyze";

import styles from "./DragAndDrop.module.scss";

import ErrorBox from "../../components/PopUps/ErrorBox/ErrorBox";
import SuccessBox from "../../components/PopUps/SuccessBox/SuccessBox";

function DragAndDrop({ user_id, setIsLoadAnalyze }) {
  const [success, setSuccess] = useState(null);
  const [error, setError] = useState(null);
  const [showError, setShowError] = useState(false);
  const [showSuccess, setShowSuccess] = useState(false);

  const onDrop = async (acceptedFiles) => {
    const file = acceptedFiles[0];

    if (file) {
      uploadFile(
        user_id,
        file,
        setError,
        setShowError,
        setSuccess,
        setShowSuccess,
        setIsLoadAnalyze
      );
    }
  };

  const { getRootProps, getInputProps, isDragActive } = useDropzone({ onDrop });

  return (
    <div className={styles.dropzoneContainer}>
      {showSuccess || setShowError ? (
        <>
          {showError && <ErrorBox error={error} />}
          {showSuccess && <SuccessBox success={success} />}
        </>
      ) : null}

      <div {...getRootProps()} className={styles.dropzone}>
        <input {...getInputProps()} />
        {isDragActive ? (
          <p className={`${styles.dropzoneContent} dark-text`}>
            Перетащите файл сюда...
          </p>
        ) : (
          <div className={styles.dropzoneContent}>
            <img src="../img/icons/drag-and-drop.svg" alt="drag-and-drop" />
            <p className={`dark-text mt35px`}>
              Перетащите файл сюда или кликните, чтобы выбрать файл
            </p>
            <p className={`gray-text mt35px`}>Поддерживаемые форматы: .xlsx</p>
          </div>
        )}
      </div>
    </div>
  );
}

export default DragAndDrop;
