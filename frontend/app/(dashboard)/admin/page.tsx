"use client";

import { useState, useEffect } from "react";
import { Settings, Package, Save, ToggleLeft, ToggleRight, CreditCard } from "lucide-react";
import { api } from "@/lib/api";

interface Plan {
  id: string;
  name: string;
  slug: string;
  price_monthly: string;
  description: string;
  features: string[];
  is_popular: boolean;
  cta_text: string;
  sort_order: number;
  limits: Record<string, number>;
  is_active: boolean;
}

interface AppModule {
  id: string;
  key: string;
  name: string;
  description: string;
  icon: string;
  href: string;
  color: string;
  is_permanent: boolean;
  is_active: boolean;
  sort_order: number;
}

// --- Plans Tab ---
function PlansTab() {
  const [plans, setPlans] = useState<Plan[]>([]);
  const [editing, setEditing] = useState<Plan | null>(null);
  const [saving, setSaving] = useState(false);

  useEffect(() => {
    api.get("/admin/plans").then((r) => setPlans(r.data));
  }, []);

  const save = async () => {
    if (!editing) return;
    setSaving(true);
    try {
      const { data } = await api.put(`/admin/plans/${editing.id}`, {
        name: editing.name,
        price_monthly: editing.price_monthly,
        description: editing.description,
        features: editing.features,
        is_popular: editing.is_popular,
        cta_text: editing.cta_text,
        sort_order: editing.sort_order,
        limits: editing.limits,
        is_active: editing.is_active,
      });
      setPlans((prev) => prev.map((p) => (p.id === data.id ? data : p)));
      setEditing(null);
    } finally {
      setSaving(false);
    }
  };

  return (
    <div className="space-y-4">
      {plans.map((plan) => (
        <div key={plan.id} className="bg-white border border-gray-200 rounded-xl p-5">
          {editing?.id === plan.id ? (
            <div className="space-y-4">
              <div className="grid grid-cols-2 gap-4">
                <Field label="Name" value={editing.name} onChange={(v) => setEditing({ ...editing, name: v })} />
                <Field label="Price" value={editing.price_monthly} onChange={(v) => setEditing({ ...editing, price_monthly: v })} />
                <Field label="Description" value={editing.description} onChange={(v) => setEditing({ ...editing, description: v })} />
                <Field label="CTA Text" value={editing.cta_text} onChange={(v) => setEditing({ ...editing, cta_text: v })} />
              </div>
              <div>
                <label className="block text-xs font-medium text-gray-500 mb-1">Features (satu per baris)</label>
                <textarea
                  className="w-full h-24 px-3 py-2 rounded-lg border border-gray-200 text-sm focus:outline-none focus:border-blue-300"
                  value={editing.features.join("\n")}
                  onChange={(e) => setEditing({ ...editing, features: e.target.value.split("\n") })}
                />
              </div>
              <div>
                <label className="block text-xs font-medium text-gray-500 mb-1">Limits (JSON)</label>
                <textarea
                  className="w-full h-20 px-3 py-2 rounded-lg border border-gray-200 text-sm font-mono focus:outline-none focus:border-blue-300"
                  value={JSON.stringify(editing.limits, null, 2)}
                  onChange={(e) => {
                    try { setEditing({ ...editing, limits: JSON.parse(e.target.value) }); } catch {}
                  }}
                />
              </div>
              <div className="flex items-center gap-4">
                <label className="flex items-center gap-2 text-sm">
                  <input type="checkbox" checked={editing.is_active} onChange={(e) => setEditing({ ...editing, is_active: e.target.checked })} />
                  Active
                </label>
                <label className="flex items-center gap-2 text-sm">
                  <input type="checkbox" checked={editing.is_popular} onChange={(e) => setEditing({ ...editing, is_popular: e.target.checked })} />
                  Popular
                </label>
              </div>
              <div className="flex gap-2">
                <button onClick={save} disabled={saving} className="flex items-center gap-2 px-4 py-2 bg-blue-600 text-white text-sm rounded-lg hover:bg-blue-700 disabled:opacity-50">
                  <Save className="w-4 h-4" /> {saving ? "Saving..." : "Save"}
                </button>
                <button onClick={() => setEditing(null)} className="px-4 py-2 text-sm text-gray-600 hover:bg-gray-100 rounded-lg">Cancel</button>
              </div>
            </div>
          ) : (
            <div className="flex items-center justify-between">
              <div>
                <div className="flex items-center gap-2">
                  <h3 className="font-semibold text-gray-900">{plan.name}</h3>
                  <span className="text-xs text-gray-400">{plan.slug}</span>
                  {!plan.is_active && <span className="text-xs bg-red-100 text-red-600 px-2 py-0.5 rounded-full">Inactive</span>}
                  {plan.is_popular && <span className="text-xs bg-blue-100 text-blue-600 px-2 py-0.5 rounded-full">Popular</span>}
                </div>
                <p className="text-sm text-gray-500 mt-1">{plan.price_monthly} — {plan.description}</p>
                <p className="text-xs text-gray-400 mt-1 font-mono">limits: {JSON.stringify(plan.limits)}</p>
              </div>
              <button onClick={() => setEditing(plan)} className="px-3 py-1.5 text-sm text-blue-600 hover:bg-blue-50 rounded-lg">Edit</button>
            </div>
          )}
        </div>
      ))}
    </div>
  );
}

// --- App Modules Tab ---
function AppModulesTab() {
  const [modules, setModules] = useState<AppModule[]>([]);

  useEffect(() => {
    api.get("/admin/app-modules").then((r) => setModules(r.data));
  }, []);

  const toggle = async (mod: AppModule) => {
    const { data } = await api.put(`/admin/app-modules/${mod.id}`, { is_active: !mod.is_active });
    setModules((prev) => prev.map((m) => (m.id === data.id ? data : m)));
  };

  return (
    <div className="space-y-3">
      {modules.map((mod) => (
        <div key={mod.id} className="bg-white border border-gray-200 rounded-xl p-4 flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className={`w-9 h-9 ${mod.color} rounded-lg flex items-center justify-center text-white text-xs font-bold`}>
              {mod.icon.slice(0, 2)}
            </div>
            <div>
              <div className="flex items-center gap-2">
                <h4 className="font-medium text-gray-900 text-sm">{mod.name}</h4>
                <span className="text-xs text-gray-400">{mod.key}</span>
                {mod.is_permanent && <span className="text-xs bg-gray-100 text-gray-500 px-2 py-0.5 rounded-full">System</span>}
              </div>
              <p className="text-xs text-gray-500">{mod.description}</p>
            </div>
          </div>
          {!mod.is_permanent && (
            <button onClick={() => toggle(mod)} className="p-1" title={mod.is_active ? "Deactivate" : "Activate"}>
              {mod.is_active ? (
                <ToggleRight className="w-8 h-8 text-blue-600" />
              ) : (
                <ToggleLeft className="w-8 h-8 text-gray-300" />
              )}
            </button>
          )}
        </div>
      ))}
    </div>
  );
}

// --- Payments Tab ---
interface Payment {
  id: string;
  tenant_id: string;
  user_id: string;
  plan_id: string;
  amount: string;
  bank_name: string;
  account_name: string;
  proof_url: string;
  status: string;
  notes: string | null;
  created_at: string;
}

function PaymentsTab() {
  const [payments, setPayments] = useState<Payment[]>([]);
  const [filter, setFilter] = useState("pending");

  useEffect(() => {
    api.get(`/admin/payments?status=${filter}`).then((r) => setPayments(r.data));
  }, [filter]);

  const approve = async (id: string) => {
    await api.post(`/admin/payments/${id}/approve`);
    setPayments((prev) => prev.filter((p) => p.id !== id));
  };

  const reject = async (id: string) => {
    const notes = prompt("Alasan reject (opsional):");
    await api.post(`/admin/payments/${id}/reject`, { notes });
    setPayments((prev) => prev.filter((p) => p.id !== id));
  };

  return (
    <div className="space-y-4">
      <div className="flex gap-2">
        {["pending", "approved", "rejected"].map((s) => (
          <button key={s} onClick={() => setFilter(s)}
            className={`px-3 py-1.5 text-xs font-medium rounded-lg ${filter === s ? "bg-blue-600 text-white" : "bg-gray-100 text-gray-600 hover:bg-gray-200"}`}>
            {s.charAt(0).toUpperCase() + s.slice(1)}
          </button>
        ))}
      </div>

      {payments.length === 0 && <p className="text-gray-400 text-sm py-8 text-center">Tidak ada payment {filter}.</p>}

      {payments.map((p) => (
        <div key={p.id} className="bg-white border border-gray-200 rounded-xl p-5">
          <div className="flex items-start justify-between gap-4">
            <div className="space-y-1 text-sm">
              <p className="font-medium text-gray-900">{p.account_name} <span className="text-gray-400">via {p.bank_name}</span></p>
              <p className="text-gray-600">Jumlah: <strong>{p.amount}</strong></p>
              <p className="text-xs text-gray-400">{new Date(p.created_at).toLocaleString("id-ID")}</p>
            </div>
            <a href={`${process.env.NEXT_PUBLIC_API_URL?.replace("/api/v1", "") || "http://localhost:8000"}${p.proof_url}`} target="_blank" rel="noopener"
              className="shrink-0 px-3 py-1.5 text-xs bg-gray-100 text-gray-700 rounded-lg hover:bg-gray-200">
              Lihat Bukti
            </a>
          </div>
          {filter === "pending" && (
            <div className="flex gap-2 mt-4 pt-3 border-t border-gray-100">
              <button onClick={() => approve(p.id)} className="px-4 py-2 bg-emerald-600 text-white text-sm rounded-lg hover:bg-emerald-700">Approve</button>
              <button onClick={() => reject(p.id)} className="px-4 py-2 bg-red-50 text-red-600 text-sm rounded-lg hover:bg-red-100">Reject</button>
            </div>
          )}
          {p.notes && <p className="text-xs text-red-500 mt-2">Catatan: {p.notes}</p>}
        </div>
      ))}
    </div>
  );
}

// --- Shared ---
function Field({ label, value, onChange }: { label: string; value: string; onChange: (v: string) => void }) {
  return (
    <div>
      <label className="block text-xs font-medium text-gray-500 mb-1">{label}</label>
      <input
        type="text"
        value={value}
        onChange={(e) => onChange(e.target.value)}
        className="w-full h-9 px-3 rounded-lg border border-gray-200 text-sm focus:outline-none focus:border-blue-300"
      />
    </div>
  );
}

// --- Main ---
const tabs = [
  { id: "plans", label: "Plans", icon: Settings },
  { id: "modules", label: "App Modules", icon: Package },
  { id: "payments", label: "Payments", icon: CreditCard },
];

export default function AdminPage() {
  const [activeTab, setActiveTab] = useState("plans");

  return (
    <div className="h-full overflow-y-auto p-4 sm:p-6 lg:p-8 max-w-4xl mx-auto">
      <h1 className="text-2xl font-bold text-gray-900 mb-1">Platform Admin</h1>
      <p className="text-sm text-gray-500 mb-6">Kelola plans, limits, dan app modules.</p>

      <div className="flex gap-1 border-b border-gray-200 mb-6">
        {tabs.map((tab) => (
          <button
            key={tab.id}
            onClick={() => setActiveTab(tab.id)}
            className={`flex items-center gap-2 px-4 py-2.5 text-sm font-medium border-b-2 transition-colors ${
              activeTab === tab.id
                ? "border-blue-600 text-blue-600"
                : "border-transparent text-gray-500 hover:text-gray-700"
            }`}
          >
            <tab.icon className="w-4 h-4" />
            {tab.label}
          </button>
        ))}
      </div>

      {activeTab === "plans" && <PlansTab />}
      {activeTab === "modules" && <AppModulesTab />}
      {activeTab === "payments" && <PaymentsTab />}
    </div>
  );
}
