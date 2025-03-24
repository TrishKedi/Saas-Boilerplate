import axios from "axios";
import { headers } from "next/headers";

const API_URL = process.env.NEXT_PUBLIC_BASE_URL;

export const loginUser = async ({username, password}: { username: string; password: string }) => {
  const formData = new URLSearchParams(); // ✅ Convert to `application/x-www-form-urlencoded`
  formData.append("username", username);
  formData.append("password", password)

  const response = await axios.post(`${API_URL}/auth/jwt/login`, formData, {
    headers: {"Content-Type" : "application/x-www-form-urlencoded"}
  });

  return response.data;
};

export const registerUser = async (data: { email: string; password: string }) => {
  const response = await axios.post(`${API_URL}/auth/register`, data);
  return response.data;
};

export const getCurrentUser = async (access_token: string | null) => {
  const response = await axios.get(`${API_URL}/users/me`, {
    headers: {
        "Authorization" : `BEARER ${access_token}`
    }
  });
  return response.data;
};
