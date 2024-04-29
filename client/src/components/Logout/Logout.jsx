import React, { useState } from "react";
import { useNavigate } from "react-router-dom";

import { logoutUser } from "../../services/auth";

import ErrorBox from "../PopUps/ErrorBox/ErrorBox";
import OrangeButton from "../UI/Buttons/OrangeButton/OrangeButton";

function Logout() {
  const navigate = useNavigate();
  const [error, setError] = useState(null);
  const [showError, setShowError] = useState(false);

  const handleLogoutSubmit = async (e) => {
    e.preventDefault();
    await logoutUser(setError, setShowError, navigate);
  };

  return (
    <>
      <OrangeButton
        title="Выйти"
        onClick={handleLogoutSubmit}
        width={200}
        height={40}
      />
      {showError && <ErrorBox error={error} />}
    </>
  );
}

export default Logout;
