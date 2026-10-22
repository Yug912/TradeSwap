import { Navigate, Route, Routes } from "react-router-dom";
import { ProtectedRoute } from "./components/ProtectedRoute";
import { AuthPage } from "./pages/AuthPage";
import { ProfilePage } from "./pages/ProfilePage";

export default function App() {
  return <Routes><Route path="/login" element={<AuthPage mode="login" />} /><Route path="/signup" element={<AuthPage mode="signup" />} /><Route element={<ProtectedRoute />}><Route path="/profile" element={<ProfilePage />} /></Route><Route path="*" element={<Navigate to="/profile" replace />} /></Routes>;
}
