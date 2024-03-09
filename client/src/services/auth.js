import axios from "../utils/axios";
import Cookies from "js-cookie";

export async function registerUser(
  first_name,
  last_name,
  email,
  password,
  setError,
  setShowError,
  setSuccess,
  setShowSuccess,
  navigate
) {
  try {
    const response = await axios.post("auth/register", {
      first_name,
      last_name,
      email,
      password,
    });
    if (response.data) {
      Cookies.set("access_token", response.data.access_token);
      Cookies.set("refresh_token", response.data.refresh_token);
      setSuccess("Добро пожаловать!");
      setShowSuccess(true);
      setTimeout(() => {
        setShowSuccess(false);
        setSuccess(null);
        navigate("/");
        window.location.reload();
      }, 500);
    }
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
  }
}

export async function loginUser(
  email,
  password,
  setError,
  setShowError,
  setSuccess,
  setShowSuccess,
  navigate
) {
  try {
    const response = await axios.post("auth/login", { email, password });

    if (response.data) {
      Cookies.set("access_token", response.data.access_token);
      Cookies.set("refresh_token", response.data.refresh_token);
      setSuccess("Рады видеть вас снова!");
      setShowSuccess(true);
      setTimeout(() => {
        setShowSuccess(false);
        setSuccess(null);
        navigate("/");
        window.location.reload();
      }, 500);
      return true;
    }
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
  }
}

export async function logoutUser(setError, setShowError, navigate) {
  try {
    const response = await axios.post("auth/logout");

    if (response.data) {
      const cookies = Object.keys(Cookies.get());
      cookies.forEach((cookie) => {
        Cookies.remove(cookie);
      });
      navigate("/login");
      window.location.reload();
    }
  } catch (error) {
    const errorMessage = error.response.data.detail;
    setError(errorMessage);
    setShowError(true);
    setTimeout(() => {
      setShowError(false);
      setError(null);
    }, 2500);
  }
}

// export async function refresh_token() {
//   try {
//     const response = await axios.post('/refresh_token');

//     if (response.data && response.data.access_token) {
//       const access_token = response.data.access_token;
//       const expirationTimeInMinutes = 60;
//       const expirationDate = new Date(new Date().getTime() + expirationTimeInMinutes * 60000);
//       Cookies.set('access_token', access_token, { expires: expirationDate });
//     }
//   } catch (error) {
//     console.log(error.response.data.detail);
//   }
// }
