import React from 'react';

import styles from './Textarea.module.scss';

function Textarea({ title, name, value, placeholder, onChange, onBlur, width, height }) {
    return (
        <div className={styles.textarea}>
            <label htmlFor={name} className={`gray-text`}>{title}</label>
            <textarea style={{ width, height }}
                name={name}
                value={value}
                onChange={onChange}
                placeholder={placeholder}
            />

        </div>
    )
}

export default Textarea;
