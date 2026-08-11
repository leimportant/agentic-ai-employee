import {
  LayoutDashboard,
  MessageSquare,
  TrendingUp,
  Headphones,
  Factory,
  Package,
  Settings,
  HelpCircle,
} from "lucide-react";
import type { LucideIcon } from "lucide-react";
import { create } from "zustand";
import { api } from "@/lib/api";

const ICON_MAP: Record<string, LucideIcon> = {
  LayoutDashboard,
  MessageSquare,
  TrendingUp,
  Headphones,
  Factory,
  Package,
  Settings,
};

export interface AppModule {
  id: string;
  key: string;
  name: string;
  description: string;
  icon: LucideIcon;
  href: string;
  color: string;
  is_permanent: boolean;
  is_active: boolean;
  sort_order: number;
}

interface AppModuleStore {
  modules: AppModule[];
  loading: boolean;
  fetched: boolean;
  fetchModules: () => Promise<void>;
  getModule: (key: string) => AppModule | undefined;
}

export const useAppModuleStore = create<AppModuleStore>((set, get) => ({
  modules: [],
  loading: false,
  fetched: false,

  fetchModules: async () => {
    if (get().fetched) return;
    set({ loading: true });
    try {
      const { data } = await api.get("/app-modules");
      const modules: AppModule[] = data.map((m: any) => ({
        ...m,
        icon: ICON_MAP[m.icon] || HelpCircle,
        is_permanent: m.is_permanent,
        is_active: m.is_active,
      }));
      set({ modules, fetched: true });
    } catch (e) {
      console.error("Failed to fetch app modules", e);
    } finally {
      set({ loading: false });
    }
  },

  getModule: (key) => get().modules.find((m) => m.key === key),
}));
