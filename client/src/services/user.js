import axios from "../utils/axios";

export async function getUserById(user_id) {
  try {
    const response = await axios.get(`user/get/${user_id}`);

    if (response.data) {
      return response.data;
    }
  } catch (error) {
    const errorMessage = error.response.data.detail;
    console.error(errorMessage);
  }
}

export async function getAllUsers() {
  try {
    const response = await axios.get("user/get_all");

    if (response.data) {
      return response.data;
    }
  } catch (error) {
    const errorMessage = error.response.data.detail;
    console.error(errorMessage);
  }
}

export async function editUser(
  user_id,
  first_name,
  last_name,
  email,
  setError,
  setShowError,
  setSuccess,
  setShowSuccess
) {
  try {
    const response = await axios.patch(`user/edit/${user_id}`, {
      first_name,
      last_name,
      email,
    });
    if (response.data) {
      setSuccess(response.data.message);
      setShowSuccess(true);
      setTimeout(() => {
        setShowSuccess(false);
        setSuccess(null);
      }, 2500);
    }
    return true;
  } catch (error) {
    const errorMessage = error.response.data.detail;
    if (errorMessage[0].msg === "value is not a valid email address") {
      setError("Неверный формат электронной почты");
    } else {
      setError(errorMessage);
    }
    setShowError(true);
    setSuccess(null);
    setShowSuccess(false);
    setTimeout(() => {
      setShowError(false);
      setError(null);
    }, 2500);
    return false;
  }
}

export async function deleteUser(
  user_id
) {
  try {
    const response = await axios.delete(`user/delete/${user_id}`);

    if (response.data) {
        return response.data
    }
  } catch (error) {
    const errorMessage = error.response.data.detail;
    console.error(errorMessage);
  }
}
