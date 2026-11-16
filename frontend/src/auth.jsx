import { createContext, useContext, useEffect, useState } from "react";
import { api, tokens } from "./api.js";

const AuthContext = createContext(null);

export function AuthProvider({ children }) {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (!tokens.access) {
      setLoading(false);
      return;
    }
    api("/auth/me/")
      .then(setUser)
      .catch(() => tokens.clear())
      .finally(() => setLoading(false));
  }, []);

  async function login(username, password) {
    const data = await api("/auth/token/", {
      method: "POST",
      body: { username, password },
      retry: false,
    });
    tokens.save(data);
    setUser(await api("/auth/me/"));
  }

  async function register(username, email, password) {
    await api("/auth/register/", {
      method: "POST",
      body: { username, email, password },
      retry: false,
    });
    await login(username, password);
  }

  function logout() {
    tokens.clear();
    setUser(null);
  }

  // PATCH /auth/me/: sửa email / mục tiêu học, cập nhật luôn user trong context
  async function updateMe(data) {
    const updated = await api("/auth/me/", { method: "PATCH", body: data });
    setUser(updated);
    return updated;
  }

  return (
    <AuthContext.Provider value={{ user, loading, login, register, logout, updateMe }}>
      {children}
    </AuthContext.Provider>
  );
}

export const useAuth = () => useContext(AuthContext);
