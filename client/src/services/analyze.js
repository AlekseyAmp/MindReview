import axios from "../utils/axios";
import { getNotifyMessage } from "../utils/ws";

export async function analyzeTest(
  reviews,
  setError,
  setShowError,
  setSuccess,
  setShowSuccess
) {
  try {
    setSuccess("Проводим анализ. Подождите несколько секунд.");
    setShowSuccess(true);
    setTimeout(() => {
      setShowSuccess(false);
      setSuccess(null);
    }, 2500);
    const response = await axios.post("analyze/test", { reviews });

    if (response.data) {
      localStorage.setItem("testAnalyzeData", JSON.stringify(response.data));
      return true;
    }
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
  }
}

export async function getAnalyzeById(analyze_id) {
  try {
    const response = await axios.get(`analyze/get/${analyze_id}`);

    if (response.data) {
      return response.data;
    }
  } catch (error) {
    const errorMessage = error.response.data.detail;
    console.error(errorMessage);
  }
}

export async function getLastAnalyze() {
  try {
    const response = await axios.get(`analyze/get_last`);

    if (response.data) {
      return response.data;
    }
  } catch (error) {
    const errorMessage = error.response.data.detail;
    console.error(errorMessage);
  }
}

export async function getAllAnalyzeResults() {
  try {
    const response = await axios.get("analyze/get_all");

    if (response.data) {
      return response.data;
    }
  } catch (error) {
    const errorMessage = error.response.data.detail;
    console.error(errorMessage);
  }
}

export async function uploadFile(
  user_id,
  file,
  setError,
  setShowError,
  setSuccess,
  setShowSuccess,
  setIsLoadAnalyze
) {
  try {
    const formData = new FormData();
    formData.append("file", file);

    const response = await axios.post("analyze/file", formData, {
      headers: {
        Accept: "application/json",
        "Content-Type": "multipart/form-data",
      },
    });

    if (response.data) {
      setIsLoadAnalyze(true);
      await getNotifyMessage(user_id);
      setIsLoadAnalyze(false);
    }
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
  }
}

export async function analyzeWebsite(
  user_id,
  website,
  reviews_id,
  setReviewId,
  setError,
  setShowError,
  setSuccess,
  setShowSuccess,
  setIsLoadAnalyze
) {
  try {
    const response = await axios.post(
      `analyze/source?website=${website}&reviews_id=${reviews_id}`
    );
    if (response.data) {
      setReviewId(null);
      setIsLoadAnalyze(true);
      await getNotifyMessage(user_id);
      setIsLoadAnalyze(false);
    }
  } catch (error) {
    if (error.response.status === 422) {
      setError("Укажите корректный адрес.");
    } else {
      setError(error.response.data.detail);
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

export function downloadAnalyzeResult(
  analyze_id,
  dt,
  setError,
  setShowError,
  setSuccess,
  setShowSuccess
) {
  try {
    axios
      .get(`analyze/download/${analyze_id}`, {
        responseType: "arraybuffer",
      })
      .then((response) => {
        setSuccess("Формируем результат анализа.");
        setShowSuccess(true);

        const parts = dt.split(/[.: ]+/);

        const formattedDate = `${parts[0]}-${parts[1]}-${parts[2]} ${parts[3]}:${parts[4]}:${parts[5]}`;

        const file_name = `Результат анализа за ${formattedDate}`;
        const blob = new Blob([response.data], {
          type: "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        });
        const link = document.createElement("a");
        link.href = window.URL.createObjectURL(blob);
        link.setAttribute("download", file_name);
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);

        setSuccess("Результат анализа сформирован.");
        setShowSuccess(true);
        setTimeout(() => {
          setShowSuccess(false);
          setSuccess(null);
        }, 2500);
      })
      .catch((error) => {
        if (error.response && error.response.status === 404) {
          setError("Результат анализа не найден.");
          setShowError(true);
          setShowSuccess(false);
          setSuccess(null);
        } else {
          console.log(error);
        }
        setTimeout(() => {
          setShowError(false);
          setError(null);
        }, 2500);
      });
  } catch (error) {
    console.error(error);
  }
}
