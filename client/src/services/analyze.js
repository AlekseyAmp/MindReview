import axios from '../utils/axios';
import Cookies from 'js-cookie';


export async function analyze_test(reviews, setError, setShowError, setSuccess, setShowSuccess, navigate) {
  try {
      setSuccess("Проводим анализ. Подождите несколько секунд.");
      setShowSuccess(true);
      setTimeout(() => {
        setShowSuccess(false);
        setSuccess(null);
    }, 2500);
      const response = await axios.post('analyze/test', { reviews });

      if (response.data) {
          localStorage.setItem('lastTestAnalyzeData', JSON.stringify(response.data));
          navigate('/analyze');
      }
  } catch (error) {
      const errorMessage = error.response.data.detail;
      setError(errorMessage);
      setShowError(true);
      setSuccess(null);
      setShowSuccess(false)
      setTimeout(() => {
          setShowError(false);
          setError(null);
      }, 2500);
  }
}



  