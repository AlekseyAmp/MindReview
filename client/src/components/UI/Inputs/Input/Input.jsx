import React from 'react';

import styles from './Input.module.scss';

function Input({ title, type, name, value, placeholder, onChange, width, height }) {
    return (
        <div className={styles.input}>
            <label htmlFor={name} className={`gray-text`}>{title}</label>
            <input style={{ width, height }}
                type={type}
                name={name}
                value={value}
                onChange={onChange}
                placeholder={placeholder}
            />

        </div>
    )
}

export default Input;
