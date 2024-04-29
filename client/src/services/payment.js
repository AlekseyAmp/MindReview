import axios from "../utils/axios";


export async function setPremium(
  setError,
  setShowError,
  setSuccess,
  setShowSuccess
) {
  try {
    const response = await axios.patch("payment/premium");
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
    setError(errorMessage);
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
