import React, { useEffect, useState } from "react";

import DragAndDrop from "../../components/DragAndDrop/DragAndDrop";
import { access_token } from "../../constants/token";
import { decodeJWT } from "../../utils/token";

import styles from "./AnalyzePreload.module.scss";

export default function AnalyzePreload() {
  const token = access_token;
  const [activeTab, setActiveTab] = useState("file");

  const [isLoadAnalyze, setIsLoadAnalyze] = useState(false);

  const decode = decodeJWT(token);

  // useEffect(() => {
  // }, [isLoadAnalyze]);

  return (
    <div className={styles.analyzePreload}>
      {isLoadAnalyze ? (
        <div className={styles.notData}>
          <img src="../img/logo.svg" alt="logo" />
          <h3 className={`bold-text`}>Отзывы анализируются...</h3>
        </div>
      ) : (
        <>
          <h3 className={`${styles.title} bold-text`}>
            Выберите способ загрузки отзывов
          </h3>
          <div className={styles.tabs}>
            <div className={styles.tab}>
              <img src="../img/icons/file-upload.svg" alt="upload-file" />
              <button
                className={`${
                  activeTab === "file" ? styles.active : ""
                } gray-text`}
                onClick={() => setActiveTab("file")}
              >
                Загрузить Excel файл с отзывами
              </button>
            </div>
            <div className={styles.tab}>
              <img
                src="../img/icons/external-service.svg"
                alt="external-service"
              />
              <button
                className={`${
                  activeTab === "external" ? styles.active : ""
                } gray-text`}
                onClick={() => setActiveTab("external")}
              >
                Загрузить отзывы со сторонних сервисов
              </button>
            </div>
          </div>
          {activeTab === "file" && (
            <DragAndDrop
              user_id={decode.payload.sub}
              setIsLoadAnalyze={setIsLoadAnalyze}
            />
          )}
        </>
      )}
    </div>
  );
}
