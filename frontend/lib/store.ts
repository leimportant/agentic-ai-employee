import { create } from "zustand";
import { persist } from "zustand/middleware";

interface PlatformStore {
  activeApps: string[];
  activateApp: (appId: string) => void;
  deactivateApp: (appId: string) => void;
  isAppActive: (appId: string) => boolean;
}

export const usePlatformStore = create<PlatformStore>()(
  persist(
    (set, get) => ({
      activeApps: ["ai-cs"], // default: CS aktif

      activateApp: (appId) =>
        set((state) => ({
          activeApps: state.activeApps.includes(appId)
            ? state.activeApps
            : [...state.activeApps, appId],
        })),

      deactivateApp: (appId) =>
        set((state) => ({
          activeApps: state.activeApps.filter((id) => id !== appId),
        })),

      isAppActive: (appId) => get().activeApps.includes(appId),
    }),
    { name: "platform-apps" }
  )
);
