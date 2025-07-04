import axios from "axios";

export function uploadFile(file) {
  const form = new FormData();
  form.append("file", file);
  return axios.post("/upload", form, {
    headers: { "Content-Type": "multipart/form-data" }
  });
}

export function getStatus(taskId) {
  return axios.get(`/status/${taskId}`);
}
