import React, { useEffect, useState } from "react";
import DragAndDrop from "../../components/DragAndDrop/DragAndDrop";
import { access_token } from "../../constants/token";
import { decodeJWT } from "../../utils/token";
import Input from "../../components/UI/Inputs/Input/Input";
import PurpleButton from "../../components/UI/Buttons/PurpleButton/PurpleButton";
import ErrorBox from "../../components/PopUps/ErrorBox/ErrorBox";
import SuccessBox from "../../components/PopUps/SuccessBox/SuccessBox";
import styles from "./AnalyzePreload.module.scss";
import { analyzeWebsite } from "../../services/analyze";

export default function AnalyzePreload() {
  const token = access_token;
  const [activeTab, setActiveTab] = useState("file");
  const [isLoadAnalyze, setIsLoadAnalyze] = useState(false);
  const [error, setError] = useState(null);
  const [showError, setShowError] = useState(false);
  const [success, setSuccess] = useState(null);
  const [showSuccess, setShowSuccess] = useState(false);
  const [selectedItem, setSelectedItem] = useState(null);
  const [reviewId, setReviewId] = useState(null);
  const [url, setUrl] = useState("");

  const decode = decodeJWT(token);

  const handleChangeUrl = (event) => {
    setUrl(event.target.value);
  };

  const handleClick = (website) => {
    setSelectedItem(website);
  };

  const handleOnClickContinue = async () => {
    if (!selectedItem) {
      setError("Выберите сайт для анализа.");
      setShowError(true);
      setSuccess(null);
      setShowSuccess(false);
      setTimeout(() => {
        setShowError(false);
        setError(null);
      }, 2500);
      return;
    }

    let reviewId = null;
    if (selectedItem === "Wildberries") {
      reviewId = extractReviewIdForWB(url);
      setReviewId(reviewId);
    }

    await analyzeWebsite(
      decode.payload.sub,
      selectedItem,
      reviewId,
      setReviewId,
      setError,
      setShowError,
      setSuccess,
      setShowSuccess,
      setIsLoadAnalyze
    );
  };

  const extractReviewIdForWB = (url) => {
    const wildberriesPattern = /imtId=(\d+)/;
    const match = url.match(wildberriesPattern);
    return match ? match[1] : null;
  };

  const websiteGuides = {
    Wildberries: {
      img: "../img/externalSources/wb.png",
      guideText: (
        <div className={`mt35px ${styles.guide}`}>
          <p className={`dark-text`}>1. Перейдите в карточку товара</p>
          <p className={`dark-text`}>
            2. Нажмите на отзывы
            <img
              src="../img/externalSources/guides/wb_guide1.png"
              alt="wb_guide"
            />
          </p>
          <p className={`dark-text`}>
            3. Скопируйте ссылку
            <img
              src="../img/externalSources/guides/wb_guide2.png"
              alt="wb_guide"
            />
          </p>
          <p className={`dark-text`}>
            4. Вставьте её в поле "Ссылка на источник"
          </p>
        </div>
      ),
    },
  };

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
          {activeTab === "external" && (
            <div className={styles.external}>
              <div className={styles.input}>
                <Input
                  title={"Ссылка на источник"}
                  type={"text"}
                  name={"url"}
                  onChange={handleChangeUrl}
                  width={"530px"}
                  height={"30px"}
                />
                <PurpleButton
                  title={"Продолжить"}
                  width={250}
                  height={37}
                  onClick={handleOnClickContinue}
                />
              </div>
              <div className={styles.websites}>
                {Object.entries(websiteGuides).map(([website, info], index) => (
                  <div
                    key={index}
                    className={styles.gridItem}
                    onClick={() => handleClick(website)}
                  >
                    <a href="#">
                      <img src={info.img} alt="website" />
                    </a>
                    <p
                      className={`dark-text`}
                      style={{
                        color: selectedItem === website ? "#15966E" : "#221F1F",
                      }}
                    >
                      {website}
                    </p>{" "}
                    {selectedItem === website && (
                      <div className={styles.tooltipWrapper}>
                        <div className={styles.tooltip}>{info.guideText}</div>
                      </div>
                    )}
                  </div>
                ))}
              </div>
            </div>
          )}
        </>
      )}
      {showError && <ErrorBox error={error} />}
      {showSuccess && <SuccessBox success={success} />}
    </div>
  );
}
