import React, { useState, useEffect } from "react";
import { useNavigate, Link } from "react-router-dom";
import { Helmet } from "react-helmet";

import styles from "./Main.module.scss";
import PurpleButton from "../../components/UI/Buttons/PurpleButton/PurpleButton";
import OrangeButton from "../../components/UI/Buttons/OrangeButton/OrangeButton";
import Textarea from "../../components/UI/Inputs/Textarea/Textarea";
import ErrorBox from "../../components/PopUps/ErrorBox/ErrorBox";
import SuccessBox from "../../components/PopUps/SuccessBox/SuccessBox";
import { analyzeTest } from "../../services/analyze";
import Tooltip from "../../components/PopUps/Tooltip/Tooltip";

function Main() {
  const navigate = useNavigate();
  const [showTooltip, setShowTooltip] = useState(false);
  const [reviews, setReviews] = useState("");
  const [success, setSuccess] = useState(null);
  const [showSuccess, setShowSuccess] = useState(false);
  const [error, setError] = useState(null);
  const [showError, setShowError] = useState(false);
  const [isSubmitting, setIsSubmitting] = useState(false);

  const scrollToTest = () => {
    const TestSection = document.getElementById("testService");
    TestSection.scrollIntoView({ behavior: "smooth" });
  };

  const handleTestSubmit = async (e) => {
    e.preventDefault();
    const hasEmptyLines = reviews
      .split("\n")
      .some((line) => line.trim() === "");
    if (hasEmptyLines) {
      const errorMessage = "Пожалуйста, введите отзывы без пустых строк.";
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
    const reviewsArray = reviews.split("\n").map((review) => review.trim());
    setIsSubmitting(true); 
    const flag = await analyzeTest(
      reviewsArray,
      setError,
      setShowError,
      setSuccess,
      setShowSuccess
    );
    if (flag) {
      navigate("/analyze/test");
    }
    setIsSubmitting(false); 
  };

  return (
    <div className={styles.main}>
      <Helmet>
        <title>MindReview - Главная</title>
      </Helmet>
      <div className={`content`}>
        <div className={styles.title}>
          <h1 className={`bold-text`} style={{ fontSize: 32 }}>
            Повысьте эффективность своего бизнеса
          </h1>
          <h3 className={`dark-text mt50px`} style={{ fontSize: 20 }}>
            MindReview предоставляет возможность <br />
            глубокого анализа потребительских отзывов, <br />
            помогая понимать восприятие продуктов и услуг, <br />
            выявлять тренды <br />
            и оптимизировать стратегии развития бизнеса <br />
          </h3>
          <div className={`mt35px ${styles.testServiceButton}`}>
            <PurpleButton
              title={"Протестировать сервис"}
              onClick={scrollToTest}
              width={300}
              height={37}
            />
          </div>
        </div>
        <div className={styles.howWork}>
          <h2 className={`bold-text`}>Как работает MindReview?</h2>
          <div className={`${styles.cards} mt50px`}>
            <div className={styles.card}>
              <p className={`purple-text`} style={{ fontSize: 20 }}>
                Загрузите отзывы
              </p>
              <img src="../img/howWork/1.png" alt="how-work-one" />
              <p className={`gray-text`}>
                <p>
                  Просто загрузите свои отзывы <br /> в систему, <br /> чтобы
                  начать анализировать их.
                </p>
              </p>
            </div>
            <div className={styles.card}>
              <p className={`purple-text`} style={{ fontSize: 20 }}>
                Алгоритм анализа отзывов
              </p>
              <img src="../img/howWork/2.png" alt="how-work-two" />
              <p className={`gray-text`}>
                Наш алгоритм анализирует <br /> каждый отзыв, <br /> понимая
                мнение ваших клиентов.
              </p>
            </div>
            <div className={styles.card}>
              <p className={`purple-text`} style={{ fontSize: 20 }}>
                Визуализация данных <br />и аналитика
              </p>
              <img src="../img/howWork/3.png" alt="how-work-three" />
              <p className={`gray-text`}>
                Получайте наглядное <br /> представление о данных с помощью{" "}
                <br /> наших инструментов визуализации.
              </p>
            </div>
          </div>
          <div className={`center mt50px`}>
            <Link to="/analyze/preload">
              <OrangeButton
                title={"Перейти к анализу"}
                width={300}
                height={37}
              />
            </Link>
          </div>
        </div>
        <div className={styles.features}>
          <h2 className={`bold-text`}>Особенности MindReview</h2>
          <div className={styles.banner}>Скоро тут будет контент</div>
        </div>
        <div className={styles.test} id="testService">
          <h2 className={`bold-text`}>Протестируйте сервис</h2>
          <div className={styles.content}>
            <img src="../img/testSection/test.png" alt="testService" />
            <div className={styles.input}>
              <div className={styles.label}>
                <span className={`gray-text`}>
                  Введите один или несколько отзывов для проверки качества
                  сервиса.
                </span>
                <Tooltip
                  setShowTooltip={setShowTooltip}
                  showTooltip={showTooltip}
                  title={"Отзывы нужно вводить каждый на новой строке:"}
                  text={
                    <span>
                      Текст1 <br /> Текст2 <br /> Текст3
                    </span>
                  }
                />
              </div>
              <Textarea
                name={"test"}
                width={702}
                height={188}
                onChange={(e) => setReviews(e.target.value)}
              />
              <div className={`mt35px`}>
                <PurpleButton
                  title={"Попробовать"}
                  width={422}
                  height={37}
                  onClick={isSubmitting ? undefined : handleTestSubmit}
                />
              </div>
            </div>
          </div>
        </div>
        {showError && <ErrorBox error={error} />}
        {showSuccess && <SuccessBox success={success} />}
      </div>
    </div>
  );
}

export default Main;
