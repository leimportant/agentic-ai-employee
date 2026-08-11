import { create } from "zustand";
import { persist } from "zustand/middleware";
import { api } from "@/lib/api";

interface User {
  id: string;
  email: string;
  name: string;
  role: string;
  tenant_id: string;
  avatar_url?: string;
  is_verified: boolean;
}

interface AuthStore {
  user: User | null;
  token: string | null;
  isAuthenticated: boolean;
  setAuth: (user: User, token: string) => void;
  logout: () => void;
  fetchUser: () => Promise<void>;
}

export const useAuthStore = create<AuthStore>()(
  persist(
    (set, get) => ({
      user: null,
      token: null,
      isAuthenticated: false,

      setAuth: (user, token) => {
        api.defaults.headers.common["Authorization"] = `Bearer ${token}`;
        set({ user, token, isAuthenticated: true });
      },

      logout: () => {
        delete api.defaults.headers.common["Authorization"];
        set({ user: null, token: null, isAuthenticated: false });
      },

      fetchUser: async () => {
        try {
          const { data } = await api.get("/auth/me");
          set({ user: data });
        } catch {
          get().logout();
        }
      },
    }),
    { name: "auth" }
  )
);
