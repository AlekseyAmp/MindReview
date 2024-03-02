import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';

import { logout_user } from '../../services/auth';

import ErrorBox from '../PopUps/ErrorBox/ErrorBox';
import OrangeButton from '../UI/Buttons/OrangeButton/OrangeButton';

function Logout() {
    const navigate = useNavigate();
    const [error, setError] = useState(null);
    const [showError, setShowError] = useState(false);

    const handleLogoutSubmit = async (e) => {
        e.preventDefault();
        await logout_user(setError, setShowError, navigate);
    };

    return (
        <>
            <OrangeButton
                title="Выйти (Временно)"
                onClick={handleLogoutSubmit}
                width={200}
                height={40}
            />
            {showError && <ErrorBox error={error} />}
        </>

    );
}

export default Logout;