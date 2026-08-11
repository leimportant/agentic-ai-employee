import { create } from "zustand";
import { api } from "@/lib/api";

interface Plan {
  id: string;
  name: string;
  slug: string;
  price_monthly: string;
  description: string | null;
  features: string[] | null;
  is_popular: boolean;
  cta_text: string | null;
  sort_order: number;
  limits: { messages: number; agents: number; apps: number; storage_mb: number };
  is_active: boolean;
}

interface Usage {
  messages: number;
  messages_limit: number;
  agents: number;
  agents_limit: number;
  apps: number;
  apps_limit: number;
  storage_mb: number;
  storage_limit_mb: number;
  period_start: string;
  period_end: string;
}

interface Subscription {
  id: string;
  plan: Plan;
  status: string;
  current_period_start: string;
  current_period_end: string;
}

interface BillingStore {
  plans: Plan[];
  usage: Usage | null;
  subscription: Subscription | null;
  fetchPlans: () => Promise<void>;
  fetchUsage: (tenantId: string) => Promise<void>;
  fetchOverview: (tenantId: string) => Promise<void>;
  subscribe: (tenantId: string, planId: string) => Promise<void>;
}

export const useBillingStore = create<BillingStore>((set) => ({
  plans: [],
  usage: null,
  subscription: null,

  fetchPlans: async () => {
    const { data } = await api.get("/billing/plans");
    set({ plans: data });
  },

  fetchUsage: async (tenantId) => {
    const { data } = await api.get("/billing/usage", { params: { tenant_id: tenantId } });
    set({ usage: data });
  },

  fetchOverview: async (tenantId) => {
    const { data } = await api.get("/billing/overview", { params: { tenant_id: tenantId } });
    set({ subscription: data.subscription, usage: data.usage });
  },

  subscribe: async (tenantId, planId) => {
    const { data } = await api.post("/billing/subscribe", { plan_id: planId }, { params: { tenant_id: tenantId } });
    set({ subscription: data });
  },
}));
