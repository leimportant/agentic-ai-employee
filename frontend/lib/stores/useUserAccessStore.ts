import { create } from "zustand";
import { api } from "@/lib/api";

interface ModuleAccess {
  module_key: string;
  sub_menus: string[] | null; // null = all sub-menus
}

interface UserAccessStore {
  role: string;
  modules: ModuleAccess[] | "__all__";
  fetched: boolean;
  fetchAccess: () => Promise<void>;
  hasModuleAccess: (key: string) => boolean;
  hasSubMenuAccess: (moduleKey: string, subMenu: string) => boolean;
}

export const useUserAccessStore = create<UserAccessStore>((set, get) => ({
  role: "",
  modules: "__all__",
  fetched: false,

  fetchAccess: async () => {
    if (get().fetched) return;
    try {
      const { data } = await api.get("/team/me/modules");
      set({ role: data.role, modules: data.modules, fetched: true });
    } catch {
      set({ fetched: true });
    }
  },

  hasModuleAccess: (key: string) => {
    const { role, modules } = get();
    if (role === "owner" || role === "admin") return true;
    if (modules === "__all__") return true;
    return modules.some((m) => m.module_key === key);
  },

  hasSubMenuAccess: (moduleKey: string, subMenu: string) => {
    const { role, modules } = get();
    if (role === "owner" || role === "admin") return true;
    if (modules === "__all__") return true;
    const mod = modules.find((m) => m.module_key === moduleKey);
    if (!mod) return false;
    if (mod.sub_menus === null) return true; // null = all sub-menus
    return mod.sub_menus.includes(subMenu);
  },
}));
