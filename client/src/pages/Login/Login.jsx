import React, { useState } from "react";
import { useNavigate, Link } from "react-router-dom";
import { Helmet } from "react-helmet";

import { loginUser } from "../../services/auth";
import { access_token } from "../../constants/token";

import ErrorBox from "../../components/PopUps/ErrorBox/ErrorBox";
import SuccessBox from "../../components/PopUps/SuccessBox/SuccessBox";
import AuthForm from "../../components/UI/Forms/AuthForm/AuthForm";
import styles from "./Login.module.scss";

function Login() {
  const navigate = useNavigate();
  const isAuthorize = !!access_token;
  const [error, setError] = useState(null);
  const [showError, setShowError] = useState(false);
  const [success, setSuccess] = useState(null);
  const [showSuccess, setShowSuccess] = useState(false);

  const inputConfigs = [
    {
      title: "Адрес электронной почты",
      type: "email",
      name: "email",
      width: "422px",
      height: "37px",
    },
    {
      title: "Пароль",
      type: "password",
      name: "password",
      width: "422px",
      height: "37px",
    },
  ];

  const handleLoginSubmit = async (e) => {
    e.preventDefault();
    const email = e.target.email.value;
    const password = e.target.password.value;
    await loginUser(
      email,
      password,
      setError,
      setShowError,
      setSuccess,
      setShowSuccess,
      navigate
    );
  };

  return (
    <div className={styles.login}>
      <Helmet>
        <title>MindReview - Вход</title>
      </Helmet>
      {isAuthorize ? null : (
        <div className={`content`}>
          <div className={`${styles.logo} center`}>
            <img src="../img/logo.svg" alt="Logo" />
          </div>
          <h2 className={`bold-text mt35px center`}>Рады видеть вас снова!</h2>
          <div
            className={`gray-text center`}
            style={{ fontSize: "18px", marginTop: "15px" }}
          >
            Выполните вход в аккаунт
          </div>
          <div className={`mt35px center`}>
            <AuthForm
              inputConfigs={inputConfigs}
              buttonTitle="Войти"
              onSubmit={handleLoginSubmit}
            />
          </div>
          <div className={`${styles.help} center mt50px`}>
            <span className={`dark-text`}>Нет аккаунта?</span>
            <Link to="/register" className={`purple-link-text`}>
              Регистрация
            </Link>
          </div>
        </div>
      )}
      {showError && <ErrorBox error={error} />}
      {showSuccess && <SuccessBox success={success} />}
    </div>
  );
}

export default Login;
