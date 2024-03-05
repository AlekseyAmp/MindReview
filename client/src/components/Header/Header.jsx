import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';

import { access_token } from '../../constants/token';
// import { getUserInfo } from '../../services/user';

import styles from './Header.module.scss';

// import Logout from '../Buttons/Logout/Logout';
import PurpleButton from '../UI/Buttons/PurpleButton/PurpleButton';
import OutlineButton from '../UI/Buttons/OutlineButton/OutlineButton';
import Logout from '../Logout/Logout';

function Header() {
    const isAuthorized = !!access_token;
    // const [name, setName] = useState('');
    // const [surname, setSurname] = useState('');
    // const [login, setLogin] = useState('');
    // const [role, setRole] = useState('');

    // useEffect(() => {
    //     if (isAuthorized) {
    //         getUserInfo()
    //             .then((data) => {
    //                 setName(data.name);
    //                 setSurname(data.surname);
    //                 setLogin(data.login);
    //                 setRole(data.role);
    //             })
    //             .catch((error) => console.log(error));
    //     }
    // }, [isAuthorized]);

    return (
        <header>

            <div className={`${styles.header} container`}>
                <div className={styles.logo}>
                    <Link to='/'>
                        <img src="img/logo.svg" alt="Logo" />
                    </Link>
                </div>
                <div className={styles.menu}>
                    <ul>
                        <li>
                            <img src="img/icons/diagram.svg" alt="analyze" />
                            <Link to='/analyze' className={`link-text`}>Анализ</Link>
                        </li>
                        <li>
                            <img src="img/icons/folder.svg" alt="archive" />
                            <Link to='/archive' className={`link-text`}>Архив</Link>
                        </li>
                        <li>
                            <img src="img/icons/issue.svg" alt="feedback" />
                            <Link to='/feedback' className={`link-text`}>Обратная связь</Link>
                        </li>
                    </ul>

                </div>
                <div className={styles.right}>
                    <ul>
                        {isAuthorized ? (
                            <>
                                <li>
                                    <Link to="/profile">
                                        <OutlineButton
                                            title='Личный кабинет'
                                            width={200}
                                            height={40}
                                        />
                                    </Link>
                                </li>
                                <li>
                                    <Logout />
                                </li>
                            </>
                        ) : (
                            <>
                                <li>
                                    <Link to="/login">
                                        <OutlineButton
                                            title='Вход'
                                            width={200}
                                            height={40}
                                        />
                                    </Link>
                                </li>
                                <li>
                                    <Link to="/register">
                                        <PurpleButton
                                            title='Регистрация'
                                            width={200}
                                            height={40}
                                        />
                                    </Link>
                                </li>
                            </>
                        )}
                    </ul>
                </div>
            </div>

        </header>

    );
}

export default Header;
