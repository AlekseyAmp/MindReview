import axios from "../utils/axios";

export async function deleteStopword(
  stopword_id,
  setError,
  setShowError,
  setSuccess,
  setShowSuccess
) {
  try {
    const response = await axios.delete(`data/stopwords/${stopword_id}`);
    setSuccess(response.data.message);
    setShowSuccess(true);
    setTimeout(() => {
      setShowSuccess(false);
      setSuccess(null);
    }, 2500);
  } catch (error) {
    setError(error.response.data.detail);
    setShowError(true);
    setTimeout(() => {
      setShowError(false);
    }, 2500);
  }
}

export async function getAllStopwords() {
  try {
    const response = await axios.get("data/stopwords");

    if (response.data) {
      return response.data;
    }
  } catch (error) {
    const errorMessage = error.response.data.detail;
    console.error(errorMessage);
  }
}

export async function updateStopwordUsage(
  stopword_id,
  setError,
  setShowError,
  setSuccess,
  setShowSuccess
) {
  try {
    const response = await axios.patch(`data/stopwords/${stopword_id}`);
    setSuccess(response.data.message);
    setShowSuccess(true);
    setTimeout(() => {
      setShowSuccess(false);
      setSuccess(null);
    }, 2500);
  } catch (error) {
    setError(error.response.data.detail);
    setShowError(true);
    setTimeout(() => {
      setShowError(false);
    }, 2500);
  }
}
