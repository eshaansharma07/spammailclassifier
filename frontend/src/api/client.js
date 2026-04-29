import axios from "axios";

const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL || (import.meta.env.PROD ? "" : "http://localhost:8000"),
  timeout: 15000,
  headers: {
    "Content-Type": "application/json",
  },
});

export async function classifyMessage(message) {
  const { data } = await api.post("/predict", { message });
  return data;
}
