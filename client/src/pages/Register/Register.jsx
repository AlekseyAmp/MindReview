import React, { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { Helmet } from 'react-helmet';

import { register_user } from '../../services/auth'
import { access_token } from '../../constants/token'

import ErrorBox from '../../components/PopUps/ErrorBox/ErrorBox';
import SuccessBox from '../../components/PopUps/SuccessBox/SuccessBox';
import AuthForm from '../../components/UI/Forms/AuthForm/AuthForm';
import styles from './Register.module.scss';

function Register() {
    const navigate = useNavigate();
    const isAuthorize = !!access_token
    const [error, setError] = useState(null);
    const [showError, setShowError] = useState(false);
    const [success, setSuccess] = useState(null);
    const [showSuccess, setShowSuccess] = useState(false);

    const inputConfigs = [
        { title: "Имя", type: 'text', name: 'first_name', width: '422px', height: '37px' },
        { title: "Фамилия", type: 'text', name: 'last_name', width: '422px', height: '37px' },
        { title: "Адрес электронной почты", type: 'email', name: 'email', width: '422px', height: '37px' },
        { title: "Пароль", type: 'password', name: 'password', width: '422px', height: '37px' },
    ]

    const handleRegisterSubmit = async (e) => {
        e.preventDefault();
        const first_name = e.target.first_name.value;
        const last_name = e.target.last_name.value;
        const email = e.target.email.value;
        const password = e.target.password.value;
        await register_user(first_name, last_name, email, password, setError, setShowError, setSuccess, setShowSuccess, navigate)
    };

    return (
        <div className={styles.register}>
                  <Helmet>
        <title>MindReview - Регистрация</title>
      </Helmet>
            {isAuthorize ? (
                null
            ) : (
                <div className={`content`}>
                    <div className={`${styles.logo} center`}>
                        <img src="../img/logo.svg" alt="Logo" />
                    </div>
                    <h2 className={`bold-text mt35px center`}>Добро пожаловать!</h2>
                    <div className={`gray-text center`} style={{ fontSize: '18px', marginTop: '15px' }}>Создайте аккаунт</div>
                    <div className={`mt35px center`}>
                        <AuthForm
                            inputConfigs={inputConfigs}
                            buttonTitle='Зарегестрироваться'
                            onSubmit={handleRegisterSubmit}
                        />
                    </div>
                    <div className={`${styles.help} center mt50px`}>
                        <span className={`dark-text`}>
                            Есть аккаунт?
                        </span>
                        <Link to='/login' className={`purple-link-text`}>Вход</Link>
                    </div>
                </div>
            )}
            {showError && <ErrorBox error={error} />}
            {showSuccess && <SuccessBox success={success} />}
        </div>
    )
}

export default Register;