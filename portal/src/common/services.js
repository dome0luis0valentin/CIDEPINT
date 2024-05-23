import axios from "axios";
axios.defaults.baseURL = "https://admin-grupo24.proyecto2023.linti.unlp.edu.ar";
const axiosInstance = axios.create({
  baseURL: "https://admin-grupo24.proyecto2023.linti.unlp.edu.ar",
  headers: {
    "Content-Type": "application/json",
    // 'Access-Control-Allow-Origin':'*',
    // 'Accept': '*/*',
}
});


axiosInstance.interceptors.request.use(
  (config) => {
    const token = window.localStorage.getItem("token");
    if(token) {
      config.headers["Authorization"] = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

export default axiosInstance;