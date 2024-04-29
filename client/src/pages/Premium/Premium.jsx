import React, { useState } from "react";
import { Helmet } from "react-helmet";
import styles from "./Premium.module.scss";
import { Link, useNavigate } from "react-router-dom";
import { access_token } from "../../constants/token";
import { setPremium } from "../../services/payment";
import ErrorBox from "../../components/PopUps/ErrorBox/ErrorBox";
import SuccessBox from "../../components/PopUps/SuccessBox/SuccessBox";
import { decodeJWT } from "../../utils/token";
import Input from "../../components/UI/Inputs/Input/Input";
import OutlineButton from "../../components/UI/Buttons/OutlineButton/OutlineButton";

function Premium() {
  const navigate = useNavigate();
  const isAuthorized = !!access_token;
  const [success, setSuccess] = useState(null);
  const [showSuccess, setShowSuccess] = useState(false);
  const [error, setError] = useState(null);
  const [showError, setShowError] = useState(false);
  const decode = decodeJWT(access_token);

  let isPremium = false;
  if (isAuthorized) {
    isPremium = decode.header.is_premium;
  }

  const handleSetPremium = async (e) => {
    e.preventDefault();
    const prem = await setPremium(
      setError,
      setShowError,
      setSuccess,
      setShowSuccess
    );
    if (prem) {
      setSuccess("Вы стали премиум пользователем.");
      setShowSuccess(true);
      setTimeout(() => {
        setShowSuccess(false);
        setSuccess(null);
        navigate("/profile");
      }, 2500);
    }
  };

  if (isPremium) {
    return (
      <div className={styles.isPremium}>
        <Helmet>
          <title>MindReview - Покупка премиума</title>
        </Helmet>
        <div className={styles.isPremiumData}>
          <h3 className={`${styles.title} bold-text`}>
            Вы уже являетесь премиум пользователем.
          </h3>
        </div>
      </div>
    );
  }

  if (!isAuthorized) {
    return (
      <div className={styles.notAuth}>
        <Helmet>
          <title>MindReview - Покупка премиума</title>
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

  return (
    <div className={styles.premium}>
      <Helmet>
        <title>MindReview - Покупка премиума</title>
      </Helmet>
      <h3 className={`bold-text center`}>Покупка премиум подписки</h3>
      <div className={styles.cardForm}>
        <div className={styles.cardFormInfo}>
          <div className={styles.money}>
            <p className={`dark-text`}>К оплате:</p>
            <p className={`green-text`}>500 рублей</p>
          </div>
          <div className={styles.cardInfo}>
            <Input
              title={"Введите номер карты"}
              type={"text"}
              name={"card_number"}
              width={"400px"}
              onChange={(e) => {
                e.target.value = e.target.value
                  .replace(/\D/g, "")
                  .replace(/(.{4})/g, "$1 ")
                  .trim();
              }}
              height={"30px"}
            />
            <div className={styles.date}>
              <Input
                title={"Срок действия"}
                type={"text"}
                name={"expire_date"}
                onChange={(e) => {
                  e.target.value = e.target.value
                    .replace(/\D/g, "")
                    .replace(/(.{2})/, "$1/")
                    .trim();
                }}
                width={"100px"}
                height={"30px"}
              />
              <Input
                title={"CVC"}
                type={"password"}
                name={"cvc"}
                width={"100px"}
                height={"30px"}
              />
            </div>
          </div>
          <OutlineButton
            title={"Купить подписку"}
            onClick={handleSetPremium}
            width={200}
            height={40}
          />
        </div>
      </div>
      {showError && <ErrorBox error={error} />}
      {showSuccess && <SuccessBox success={success} />}
    </div>
  );
}

export default Premium;
