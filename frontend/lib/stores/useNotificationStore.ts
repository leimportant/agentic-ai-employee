import { create } from "zustand";
import { api } from "@/lib/api";

interface Notification {
  id: string;
  type: string;
  title: string;
  message: string;
  action_url?: string;
  is_read: boolean;
  created_at: string;
}

interface NotificationStore {
  notifications: Notification[];
  unreadCount: number;
  fetch: (tenantId: string, userId: string) => Promise<void>;
  markRead: (id: string) => Promise<void>;
  markAllRead: (tenantId: string, userId: string) => Promise<void>;
}

export const useNotificationStore = create<NotificationStore>((set, get) => ({
  notifications: [],
  unreadCount: 0,

  fetch: async (tenantId, userId) => {
    try {
      const { data } = await api.get("/notifications", { params: { tenant_id: tenantId, user_id: userId } });
      set({ notifications: data, unreadCount: data.filter((n: Notification) => !n.is_read).length });
    } catch {}
  },

  markRead: async (id) => {
    await api.post(`/notifications/${id}/read`);
    set((s) => ({
      notifications: s.notifications.map((n) => n.id === id ? { ...n, is_read: true } : n),
      unreadCount: Math.max(0, s.unreadCount - 1),
    }));
  },

  markAllRead: async (tenantId, userId) => {
    await api.post("/notifications/read-all", null, { params: { tenant_id: tenantId, user_id: userId } });
    set((s) => ({
      notifications: s.notifications.map((n) => ({ ...n, is_read: true })),
      unreadCount: 0,
    }));
  },
}));
