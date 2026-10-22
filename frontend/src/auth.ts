export function isAuthenticated() { return Boolean(localStorage.getItem("accessToken")); }

export function saveTokens(tokens: { access: string; refresh: string }) {
  localStorage.setItem("accessToken", tokens.access);
  localStorage.setItem("refreshToken", tokens.refresh);
}

export function signOut() { localStorage.removeItem("accessToken"); localStorage.removeItem("refreshToken"); }
