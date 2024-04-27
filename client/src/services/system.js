import axios from "../utils/axios";

export async function getSystemInfo() {
    try {
      const response = await axios.get("system/info");
  
      if (response.data) {
        return response.data;
      }
    } catch (error) {
      const errorMessage = error.response.data.detail;
      console.error(errorMessage);
    }
  }
