"use client";

import { useEffect } from "react";
import { Check, Zap, Crown, Building2, CreditCard, Receipt, TrendingUp, AlertCircle } from "lucide-react";
import { useState } from "react";
import { useBillingStore } from "@/lib/stores/useBillingStore";
import { useAuthStore } from "@/lib/stores/useAuthStore";

const planIcons: Record<string, typeof Zap> = { starter: Zap, pro: Crown, enterprise: Building2 };
const planColors: Record<string, string> = { starter: "gray", pro: "blue", enterprise: "violet" };

export default function BillingPage() {
  const { user } = useAuthStore();
  const { plans, usage, subscription, fetchPlans, fetchOverview } = useBillingStore();
  const [billingPeriod, setBillingPeriod] = useState<"monthly" | "yearly">("monthly");

  useEffect(() => {
    fetchPlans();
    if (user) fetchOverview(user.tenant_id);
  }, [user, fetchPlans, fetchOverview]);

  const currentSlug = subscription?.plan?.slug || "starter";

  const usageItems = usage ? [
    { label: "Pesan", used: usage.messages, limit: usage.messages_limit, unit: "pesan" },
    { label: "AI Agents", used: usage.agents, limit: usage.agents_limit, unit: "agent" },
    { label: "Apps Aktif", used: usage.apps, limit: usage.apps_limit, unit: "apps" },
    { label: "Storage", used: usage.storage_mb, limit: usage.storage_limit_mb, unit: "MB" },
  ] : [];

  return (
    <div className="h-full overflow-y-auto p-4 sm:p-6 lg:p-8 max-w-6xl mx-auto space-y-8">
      <div>
        <h1 className="text-2xl font-bold text-gray-900">Billing & Plan</h1>
        <p className="text-gray-500 text-sm mt-1">Kelola subscription dan pantau penggunaan kamu.</p>
      </div>

      {/* Current Plan Banner */}
      <div className="bg-gradient-to-r from-blue-600 to-indigo-600 rounded-xl p-6 text-white flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4">
        <div>
          <div className="flex items-center gap-2 mb-1">
            <Zap className="w-5 h-5" />
            <span className="font-semibold text-lg">Plan {subscription?.plan?.name || "Starter"}</span>
            {subscription?.status === "trialing" && (
              <span className="bg-white/20 text-xs px-2 py-0.5 rounded-full">Trial</span>
            )}
          </div>
          <p className="text-blue-100 text-sm">
            {subscription ? `Aktif hingga ${new Date(subscription.current_period_end).toLocaleDateString("id-ID")}` : "Free plan"}
          </p>
        </div>
        {currentSlug === "starter" && (
          <button className="bg-white text-blue-700 font-medium text-sm px-5 py-2.5 rounded-lg hover:bg-blue-50 transition-colors shrink-0">
            Upgrade Plan
          </button>
        )}
      </div>

      {/* Usage Stats */}
      {usageItems.length > 0 && (
        <section>
          <h2 className="font-semibold text-gray-900 mb-4 flex items-center gap-2">
            <TrendingUp className="w-4 h-4" /> Penggunaan Bulan Ini
          </h2>
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
            {usageItems.map((item) => {
              const pct = Math.round((item.used / item.limit) * 100);
              const isWarning = pct >= 80;
              return (
                <div key={item.label} className="bg-white border border-gray-200 rounded-xl p-4">
                  <div className="flex items-center justify-between mb-2">
                    <span className="text-sm text-gray-600">{item.label}</span>
                    {isWarning && <AlertCircle className="w-4 h-4 text-amber-500" />}
                  </div>
                  <p className="text-xl font-bold text-gray-900">
                    {item.used.toLocaleString()} <span className="text-sm font-normal text-gray-400">/ {item.limit.toLocaleString()} {item.unit}</span>
                  </p>
                  <div className="mt-3 w-full h-2 bg-gray-100 rounded-full overflow-hidden">
                    <div className={`h-full rounded-full ${isWarning ? "bg-amber-500" : "bg-blue-500"}`} style={{ width: `${Math.min(pct, 100)}%` }} />
                  </div>
                  <p className={`text-xs mt-1 ${isWarning ? "text-amber-600" : "text-gray-400"}`}>{pct}% terpakai</p>
                </div>
              );
            })}
          </div>
        </section>
      )}

      {/* Plan Cards */}
      <section>
        <div className="flex items-center justify-between mb-4">
          <h2 className="font-semibold text-gray-900">Pilih Plan</h2>
          <div className="flex items-center bg-gray-100 rounded-lg p-1 text-sm">
            <button onClick={() => setBillingPeriod("monthly")} className={`px-3 py-1.5 rounded-md transition-colors ${billingPeriod === "monthly" ? "bg-white shadow-sm text-gray-900 font-medium" : "text-gray-500"}`}>Bulanan</button>
            <button onClick={() => setBillingPeriod("yearly")} className={`px-3 py-1.5 rounded-md transition-colors ${billingPeriod === "yearly" ? "bg-white shadow-sm text-gray-900 font-medium" : "text-gray-500"}`}>
              Tahunan <span className="text-emerald-600 text-xs ml-1">-20%</span>
            </button>
          </div>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          {(plans.length > 0 ? plans : [
            { id: "1", name: "Starter", slug: "starter", price_monthly: "Gratis", limits: { messages: 1000, agents: 1, apps: 2, storage_mb: 100 }, is_active: true },
            { id: "2", name: "Pro", slug: "pro", price_monthly: "Rp 199k", limits: { messages: 10000, agents: 5, apps: 5, storage_mb: 500 }, is_active: true },
            { id: "3", name: "Enterprise", slug: "enterprise", price_monthly: "Custom", limits: { messages: -1, agents: -1, apps: -1, storage_mb: -1 }, is_active: true },
          ]).map((plan) => {
            const isCurrent = plan.slug === currentSlug;
            const isPopular = plan.slug === "pro";
            const Icon = planIcons[plan.slug] || Zap;
            const color = planColors[plan.slug] || "gray";

            return (
              <div key={plan.id} className={`relative bg-white border rounded-xl p-6 flex flex-col ${isPopular ? "border-blue-300 ring-2 ring-blue-100" : "border-gray-200"}`}>
                {isPopular && <span className="absolute -top-3 left-1/2 -translate-x-1/2 bg-blue-600 text-white text-xs font-medium px-3 py-1 rounded-full">Paling Populer</span>}
                <div className={`w-10 h-10 rounded-lg flex items-center justify-center mb-4 ${color === "gray" ? "bg-gray-100 text-gray-600" : color === "blue" ? "bg-blue-100 text-blue-600" : "bg-violet-100 text-violet-600"}`}>
                  <Icon className="w-5 h-5" />
                </div>
                <h3 className="font-semibold text-gray-900 text-lg">{plan.name}</h3>
                <div className="mt-4 mb-6">
                  <span className="text-3xl font-bold text-gray-900">{plan.price_monthly}</span>
                  {plan.slug !== "starter" && plan.slug !== "enterprise" && <span className="text-gray-500 text-sm">/bulan</span>}
                </div>
                <ul className="space-y-2.5 flex-1 text-sm text-gray-600">
                  <li className="flex items-center gap-2"><Check className="w-4 h-4 text-emerald-500" />{plan.limits.messages === -1 ? "Unlimited" : plan.limits.messages.toLocaleString()} pesan/bulan</li>
                  <li className="flex items-center gap-2"><Check className="w-4 h-4 text-emerald-500" />{plan.limits.agents === -1 ? "Unlimited" : plan.limits.agents} AI Agents</li>
                  <li className="flex items-center gap-2"><Check className="w-4 h-4 text-emerald-500" />{plan.limits.apps === -1 ? "Unlimited" : plan.limits.apps} Apps</li>
                </ul>
                <button
                  className={`mt-6 w-full py-2.5 rounded-lg text-sm font-medium transition-colors ${
                    isCurrent ? "bg-gray-100 text-gray-500 cursor-default" : isPopular ? "bg-blue-600 text-white hover:bg-blue-700" : "bg-gray-900 text-white hover:bg-gray-800"
                  }`}
                  disabled={isCurrent}
                >
                  {isCurrent ? "Plan Saat Ini" : plan.slug === "enterprise" ? "Hubungi Sales" : "Upgrade"}
                </button>
              </div>
            );
          })}
        </div>
      </section>

      {/* Payment Method */}
      <section>
        <h2 className="font-semibold text-gray-900 mb-4 flex items-center gap-2"><CreditCard className="w-4 h-4" /> Metode Pembayaran</h2>
        <div className="bg-white border border-gray-200 rounded-xl p-5">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-3">
              <div className="w-10 h-10 bg-gray-100 rounded-lg flex items-center justify-center"><CreditCard className="w-5 h-5 text-gray-500" /></div>
              <div>
                <p className="text-sm font-medium text-gray-900">Belum ada metode pembayaran</p>
                <p className="text-xs text-gray-500">Tambahkan kartu atau e-wallet untuk upgrade</p>
              </div>
            </div>
            <button className="text-sm text-blue-600 hover:text-blue-700 font-medium">+ Tambah</button>
          </div>
        </div>
      </section>
    </div>
  );
}
