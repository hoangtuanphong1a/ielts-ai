// Wrapper fetch: tự gắn JWT, tự refresh khi access token hết hạn.
const ACCESS = "ielts_access";
const REFRESH = "ielts_refresh";

export const tokens = {
  get access() { return localStorage.getItem(ACCESS); },
  get refresh() { return localStorage.getItem(REFRESH); },
  save({ access, refresh }) {
    if (access) localStorage.setItem(ACCESS, access);
    if (refresh) localStorage.setItem(REFRESH, refresh);
  },
  clear() {
    localStorage.removeItem(ACCESS);
    localStorage.removeItem(REFRESH);
  },
};

async function refreshAccess() {
  if (!tokens.refresh) return false;
  const res = await fetch("/api/auth/token/refresh/", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ refresh: tokens.refresh }),
  });
  if (!res.ok) return false;
  tokens.save(await res.json());
  return true;
}

export async function api(path, { method = "GET", body, retry = true } = {}) {
  const headers = { "Content-Type": "application/json" };
  if (tokens.access) headers.Authorization = `Bearer ${tokens.access}`;

  const res = await fetch(`/api${path}`, {
    method,
    headers,
    body: body ? JSON.stringify(body) : undefined,
  });

  if (res.status === 401 && retry && (await refreshAccess())) {
    return api(path, { method, body, retry: false });
  }

  const data = res.status === 204 ? null : await res.json().catch(() => null);
  if (!res.ok) {
    const err = new Error("API error");
    err.status = res.status;
    err.data = data;
    throw err;
  }
  return data;
}

// Gom lỗi DRF {field: ["msg"]} thành 1 chuỗi để hiển thị
export function errorText(err) {
  if (!err?.data) return "Something went wrong. Please try again.";
  if (typeof err.data.detail === "string") return err.data.detail;
  return Object.entries(err.data)
    .map(([k, v]) => `${k}: ${[].concat(v).join(" ")}`)
    .join("\n");
}
