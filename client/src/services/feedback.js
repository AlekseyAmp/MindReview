import axios from "../utils/axios";

export async function sendFeedback(
  email,
  message,
  setError,
  setShowError,
  setSuccess,
  setShowSuccess
) {
  try {
    const response = await axios.post("feedback/send", { email, message });
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
      setError("Неверный формат электронной почты.");
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

export async function getAllFeedbacks() {
  try {
    const response = await axios.get("feedback/get_all");

    if (response.data) {
      return response.data;
    }
  } catch (error) {
    const errorMessage = error.response.data.detail;
    console.error(errorMessage);
  }
}

export async function replyFeedback(
  feedback_id,
  response,
  setError,
  setShowError,
  setSuccess,
  setShowSuccess
) {
  try {
    const resp = await axios.post("/feedback/reply", { feedback_id, response });
    if (resp.data) {
      setSuccess(resp.data.message);
      setShowSuccess(true);
      setTimeout(() => {
        setShowSuccess(false);
        setSuccess(null);
      }, 2500);
    }
    return true;
  } catch (error) {
    const errorMessage = error.response.data.detail;
    setError(errorMessage);
    setShowError(true);
    setTimeout(() => {
      setShowError(false);
      setError(null);
    }, 2500);
    return false;
  }
}
