import { toast } from "react-toastify";
import "react-toastify/dist/ReactToastify.css";
import { BASE_WS_URL } from "../constants/baseURL";

export function getNotifyMessage(userId, setSuccess, setShowSuccess) {
  return new Promise((resolve, reject) => {
    const socket = new WebSocket(`${BASE_WS_URL}/analyze/ws/${userId}`);

    socket.onopen = () => {
      console.log("WebSocket подключен");
    };

    socket.onmessage = (event) => {
      resolve(event.data);
      toast.success(event.data, {
        position: "bottom-left",
        autoClose: 3000,
        hideProgressBar: false,
        closeOnClick: true,
        pauseOnHover: true,
        draggable: true,
        style: {
          borderRadius: "7px",
          backgroundColor: "#635BFF",
          color: "#FEFFFF",
          fontFamily: "Mulish",
          fontWeight: "bold",
          fontSize: "16px",
        },
      });
    };

    socket.onclose = () => {
      console.log("WebSocket закрыт");
      reject("WebSocket закрыт");
    };

    socket.onerror = (error) => {
      console.error("WebSocket ошибка:", error);
      reject(error);
    };
  });
}
