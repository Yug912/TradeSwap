import axios from "axios";

export const api = axios.create({ baseURL: import.meta.env.VITE_API_URL ?? "http://localhost:8000/api" });

api.interceptors.request.use((config) => {
  const token = localStorage.getItem("accessToken");
  if (token) config.headers.Authorization = `Bearer ${token}`;
  return config;
});

export type UserSkill = { id: number; skill_id: number; skill_name: string; direction: "teach" | "learn"; level: "beginner" | "intermediate" | "advanced" };
export type Profile = { id: number; username: string; email: string; first_name: string; last_name: string; bio: string; teach_skills: UserSkill[]; learn_skills: UserSkill[] };
export type Skill = { id: number; name: string };
