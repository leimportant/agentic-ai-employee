import { create } from "zustand";
import { api } from "@/lib/api";

interface Customer {
  id: string;
  name: string;
  email?: string;
  phone?: string;
  channel: string;
  last_message_at?: string;
  created_at: string;
}

interface CustomerStore {
  customers: Customer[];
  loading: boolean;
  fetch: (tenantId: string) => Promise<void>;
  create: (tenantId: string, data: Partial<Customer>) => Promise<void>;
  remove: (tenantId: string, customerId: string) => Promise<void>;
}

export const useCustomerStore = create<CustomerStore>((set, get) => ({
  customers: [],
  loading: false,

  fetch: async (tenantId) => {
    set({ loading: true });
    try {
      const { data } = await api.get("/customers", { params: { tenant_id: tenantId } });
      set({ customers: data });
    } finally {
      set({ loading: false });
    }
  },

  create: async (tenantId, customerData) => {
    const { data } = await api.post("/customers", customerData, { params: { tenant_id: tenantId } });
    set((s) => ({ customers: [data, ...s.customers] }));
  },

  remove: async (tenantId, customerId) => {
    await api.delete(`/customers/${customerId}`, { params: { tenant_id: tenantId } });
    set((s) => ({ customers: s.customers.filter((c) => c.id !== customerId) }));
  },
}));
