import React from 'react';
import styles from './Tooltip.module.scss';

function Tooltip({ setShowTooltip, showTooltip, title, text }) {
    return (
        <div className={styles.tooltip} onMouseEnter={() => setShowTooltip(true)} onMouseLeave={() => setShowTooltip(false)}>
            <img src="../img/icons/purple-issue.svg" alt="issue" />
            {showTooltip && (
                <div className={styles.tooltipContent}>
                    <p className={`dark-text`}>
                        {title}
                    </p>
                    <p className={`gray-text`}>
                        {text}
                    </p>
                </div>
            )}
        </div>
    );
};

export default Tooltip;
