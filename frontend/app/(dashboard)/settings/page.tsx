"use client";

import { useState, Suspense } from "react";
import { useSearchParams } from "next/navigation";
import { User, Users, CreditCard, Key, Camera, Mail, Shield, Trash2, Plus, Copy, Eye, EyeOff } from "lucide-react";

// --- Tab: Profile ---
function ProfileTab() {
  return (
    <div className="space-y-6">
      <div className="bg-white border border-gray-200 rounded-xl p-6">
        <h3 className="font-semibold text-gray-900 mb-4">Profil</h3>
        <div className="flex items-center gap-4 mb-6">
          <div className="relative">
            <div className="w-16 h-16 rounded-full bg-blue-100 text-blue-700 flex items-center justify-center text-xl font-bold">JD</div>
            <button className="absolute -bottom-1 -right-1 w-7 h-7 bg-white border border-gray-200 rounded-full flex items-center justify-center text-gray-500 hover:bg-gray-50">
              <Camera className="w-3.5 h-3.5" />
            </button>
          </div>
          <div>
            <p className="font-medium text-gray-900">John Doe</p>
            <p className="text-sm text-gray-500">john@example.com</p>
          </div>
        </div>
        <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">Nama</label>
            <input type="text" defaultValue="John Doe" className="w-full h-9 px-3 rounded-lg border border-gray-200 text-sm focus:outline-none focus:border-blue-300" />
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">Email</label>
            <input type="email" defaultValue="john@example.com" disabled className="w-full h-9 px-3 rounded-lg border border-gray-200 text-sm bg-gray-50 text-gray-500" />
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">Nama Perusahaan</label>
            <input type="text" defaultValue="PT Maju Jaya" className="w-full h-9 px-3 rounded-lg border border-gray-200 text-sm focus:outline-none focus:border-blue-300" />
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">Telepon</label>
            <input type="text" defaultValue="+62 812-3456-7890" className="w-full h-9 px-3 rounded-lg border border-gray-200 text-sm focus:outline-none focus:border-blue-300" />
          </div>
        </div>
        <button className="mt-4 bg-blue-600 text-white text-sm font-medium px-4 py-2 rounded-lg hover:bg-blue-700">Simpan</button>
      </div>

      <div className="bg-white border border-gray-200 rounded-xl p-6">
        <h3 className="font-semibold text-gray-900 mb-4">Keamanan</h3>
        <div className="space-y-3">
          <div className="flex items-center justify-between py-2">
            <div className="flex items-center gap-3">
              <Shield className="w-4 h-4 text-gray-400" />
              <div>
                <p className="text-sm font-medium text-gray-900">Password</p>
                <p className="text-xs text-gray-500">Terakhir diubah 30 hari lalu</p>
              </div>
            </div>
            <button className="text-sm text-blue-600 hover:text-blue-700 font-medium">Ubah</button>
          </div>
          <div className="flex items-center justify-between py-2">
            <div className="flex items-center gap-3">
              <Mail className="w-4 h-4 text-gray-400" />
              <div>
                <p className="text-sm font-medium text-gray-900">Two-Factor Auth</p>
                <p className="text-xs text-gray-500">Belum diaktifkan</p>
              </div>
            </div>
            <button className="text-sm text-blue-600 hover:text-blue-700 font-medium">Aktifkan</button>
          </div>
        </div>
      </div>
    </div>
  );
}

// --- Tab: Team ---
const members = [
  { id: "1", name: "John Doe", email: "john@example.com", role: "owner", avatar: "JD" },
  { id: "2", name: "Jane Smith", email: "jane@example.com", role: "admin", avatar: "JS" },
  { id: "3", name: "Budi Santoso", email: "budi@example.com", role: "member", avatar: "BS" },
];

const pendingInvites = [
  { id: "1", email: "andi@example.com", role: "member", expires: "24 Jun 2026" },
];

function TeamTab() {
  const [showInvite, setShowInvite] = useState(false);

  return (
    <div className="space-y-6">
      {/* Members */}
      <div className="bg-white border border-gray-200 rounded-xl p-6">
        <div className="flex items-center justify-between mb-4">
          <h3 className="font-semibold text-gray-900">Anggota Tim ({members.length})</h3>
          <button onClick={() => setShowInvite(!showInvite)} className="flex items-center gap-1.5 text-sm font-medium text-white bg-blue-600 hover:bg-blue-700 px-3 py-1.5 rounded-lg">
            <Plus className="w-3.5 h-3.5" /> Undang
          </button>
        </div>

        {showInvite && (
          <div className="mb-4 p-4 bg-blue-50 border border-blue-100 rounded-lg">
            <div className="flex gap-2">
              <input type="email" placeholder="email@example.com" className="flex-1 h-9 px-3 rounded-lg border border-gray-200 text-sm focus:outline-none focus:border-blue-300" />
              <select className="h-9 px-3 rounded-lg border border-gray-200 text-sm">
                <option value="member">Member</option>
                <option value="admin">Admin</option>
                <option value="viewer">Viewer</option>
              </select>
              <button className="bg-blue-600 text-white text-sm font-medium px-4 rounded-lg hover:bg-blue-700">Kirim</button>
            </div>
          </div>
        )}

        <div className="divide-y divide-gray-100">
          {members.map((m) => (
            <div key={m.id} className="flex items-center justify-between py-3">
              <div className="flex items-center gap-3">
                <div className="w-9 h-9 rounded-full bg-gray-100 text-gray-700 flex items-center justify-center text-xs font-semibold">{m.avatar}</div>
                <div>
                  <p className="text-sm font-medium text-gray-900">{m.name}</p>
                  <p className="text-xs text-gray-500">{m.email}</p>
                </div>
              </div>
              <div className="flex items-center gap-2">
                <span className={`text-xs font-medium px-2 py-0.5 rounded-full ${
                  m.role === "owner" ? "bg-amber-50 text-amber-700" :
                  m.role === "admin" ? "bg-blue-50 text-blue-700" :
                  "bg-gray-100 text-gray-600"
                }`}>{m.role}</span>
                {m.role !== "owner" && (
                  <button className="p-1.5 text-gray-400 hover:text-red-500 hover:bg-red-50 rounded">
                    <Trash2 className="w-3.5 h-3.5" />
                  </button>
                )}
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Pending Invites */}
      {pendingInvites.length > 0 && (
        <div className="bg-white border border-gray-200 rounded-xl p-6">
          <h3 className="font-semibold text-gray-900 mb-4">Undangan Pending</h3>
          <div className="divide-y divide-gray-100">
            {pendingInvites.map((inv) => (
              <div key={inv.id} className="flex items-center justify-between py-3">
                <div>
                  <p className="text-sm font-medium text-gray-900">{inv.email}</p>
                  <p className="text-xs text-gray-500">Expires: {inv.expires} • Role: {inv.role}</p>
                </div>
                <button className="text-xs text-red-600 hover:text-red-700 font-medium">Batalkan</button>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}

// --- Tab: API Keys ---
function ApiKeysTab() {
  const [showKey, setShowKey] = useState(false);
  const apiKey = "ak_live_7f3d9a2b1c4e5f6g8h9i0j1k2l3m4n5o";

  return (
    <div className="space-y-6">
      <div className="bg-white border border-gray-200 rounded-xl p-6">
        <div className="flex items-center justify-between mb-4">
          <h3 className="font-semibold text-gray-900">API Keys</h3>
          <button className="flex items-center gap-1.5 text-sm font-medium text-white bg-blue-600 hover:bg-blue-700 px-3 py-1.5 rounded-lg">
            <Plus className="w-3.5 h-3.5" /> Generate Key
          </button>
        </div>

        <div className="bg-gray-50 border border-gray-200 rounded-lg p-4">
          <div className="flex items-center justify-between mb-2">
            <span className="text-sm font-medium text-gray-700">Production Key</span>
            <span className="text-xs text-gray-400">Dibuat: 15 Jun 2026</span>
          </div>
          <div className="flex items-center gap-2">
            <code className="flex-1 text-sm font-mono bg-white border border-gray-200 rounded px-3 py-2 text-gray-700">
              {showKey ? apiKey : "ak_live_••••••••••••••••••••••••••••"}
            </code>
            <button onClick={() => setShowKey(!showKey)} className="p-2 text-gray-400 hover:text-gray-600 hover:bg-gray-100 rounded">
              {showKey ? <EyeOff className="w-4 h-4" /> : <Eye className="w-4 h-4" />}
            </button>
            <button className="p-2 text-gray-400 hover:text-gray-600 hover:bg-gray-100 rounded">
              <Copy className="w-4 h-4" />
            </button>
          </div>
        </div>

        <div className="mt-4 p-3 bg-amber-50 border border-amber-100 rounded-lg">
          <p className="text-xs text-amber-700">⚠️ Jangan share API key. Gunakan environment variable untuk menyimpannya.</p>
        </div>
      </div>
    </div>
  );
}

// --- Main Settings Page ---
const tabs = [
  { id: "profile", label: "Profil", icon: User },
  { id: "team", label: "Tim", icon: Users },
  { id: "billing", label: "Billing", icon: CreditCard },
  { id: "api-keys", label: "API Keys", icon: Key },
];

export default function SettingsPage() {
  return (
    <Suspense fallback={<div className="p-8 text-gray-400">Loading...</div>}>
      <SettingsContent />
    </Suspense>
  );
}

function SettingsContent() {
  const searchParams = useSearchParams();
  const [activeTab, setActiveTab] = useState(searchParams.get("tab") || "profile");

  return (
    <div className="h-full overflow-y-auto p-4 sm:p-6 lg:p-8 max-w-4xl mx-auto">
      <h1 className="text-2xl font-bold text-gray-900 mb-6">Settings</h1>

      {/* Tab Navigation */}
      <div className="flex gap-1 border-b border-gray-200 mb-6 overflow-x-auto">
        {tabs.map((tab) => (
          <button
            key={tab.id}
            onClick={() => setActiveTab(tab.id)}
            className={`flex items-center gap-2 px-4 py-2.5 text-sm font-medium border-b-2 transition-colors whitespace-nowrap ${
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

      {/* Tab Content */}
      {activeTab === "profile" && <ProfileTab />}
      {activeTab === "team" && <TeamTab />}
      {activeTab === "billing" && (
        <div className="bg-white border border-gray-200 rounded-xl p-6 text-center">
          <CreditCard className="w-8 h-8 text-gray-300 mx-auto mb-3" />
          <p className="text-gray-500 text-sm mb-3">Kelola subscription dan pembayaran</p>
          <a href="/billing" className="text-sm text-blue-600 hover:text-blue-700 font-medium">Buka halaman Billing →</a>
        </div>
      )}
      {activeTab === "api-keys" && <ApiKeysTab />}
    </div>
  );
}
