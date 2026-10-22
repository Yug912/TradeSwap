import { FormEvent, useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { api } from "../api";
import { saveTokens } from "../auth";

export function AuthPage({ mode }: { mode: "login" | "signup" }) {
  const navigate = useNavigate();
  const [error, setError] = useState("");
  const [showPassword, setShowPassword] = useState(false);
  const isSignup = mode === "signup";

  async function submit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault(); setError("");
    const form = new FormData(event.currentTarget);
    const payload = Object.fromEntries(form);
    try {
      const { data } = await api.post(isSignup ? "/register/" : "/login/", payload);
      saveTokens(data.tokens); navigate("/profile");
    } catch (err: any) {
      const response = err.response?.data;
      const fieldError = response && typeof response === "object"
        ? Object.entries(response).find(([key, value]) => key !== "detail" && Array.isArray(value))
        : undefined;
      setError(response?.detail || response?.non_field_errors?.[0] || (fieldError ? `${fieldError[0]}: ${(fieldError[1] as string[])[0]}` : "Please check your details and try again."));
    }
  }

  return <main className="auth"><section><h1>TradeSwap</h1><p>Trade what you know. Learn what you love.</p></section><form onSubmit={submit}><h2>{isSignup ? "Create your account" : "Welcome back"}</h2>
    {isSignup && <><label>First name<input name="first_name" /></label><label>Last name<input name="last_name" /></label><label>Email<input name="email" type="email" required /></label></>}
    <label>Username<input name="username" required /></label><label>Password<span className="password-field"><input name="password" type={showPassword ? "text" : "password"} minLength={8} required /><button type="button" className="show-password" onClick={() => setShowPassword(!showPassword)}>{showPassword ? "Hide" : "Show"}</button></span></label>
    {error && <p className="error">{error}</p>}<button>{isSignup ? "Sign up" : "Log in"}</button><p>{isSignup ? "Already have an account?" : "New to TradeSwap?"} <Link to={isSignup ? "/login" : "/signup"}>{isSignup ? "Log in" : "Sign up"}</Link></p>
  </form></main>;
}
