import React from 'react';

import styles from './AuthForm.module.scss';

import Input from '../../Inputs/Input/Input';
import PurpleButton from '../../Buttons/PurpleButton/PurpleButton';

function AuthForm({ inputConfigs, buttonTitle, onSubmit }) {
    return (
        <form className={styles.form} onSubmit={onSubmit}>
            {inputConfigs.map((inputConfig, index) => (
                <Input
                    key={index}
                    title={inputConfig.title}
                    type={inputConfig.type}
                    name={inputConfig.name}
                    width={inputConfig.width}
                    height={inputConfig.height}
                />
            ))}
            <PurpleButton title={buttonTitle} width={441} height={37} />
        </form>
    );
};

export default AuthForm;