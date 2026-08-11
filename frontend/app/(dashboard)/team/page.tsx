"use client";

import { useEffect, useState } from "react";
import { Users, Plus, Shield, UserCog, Package } from "lucide-react";
import { api } from "@/lib/api";
import { useAuthStore } from "@/lib/stores/useAuthStore";
import { useAppModuleStore } from "@/lib/app-registry";

interface Member {
  id: string;
  email: string;
  name: string | null;
  role: string;
  is_verified: boolean;
}

export default function TeamPage() {
  const { user } = useAuthStore();
  const { modules, fetchModules } = useAppModuleStore();
  const [members, setMembers] = useState<Member[]>([]);
  const [showInvite, setShowInvite] = useState(false);
  const [email, setEmail] = useState("");
  const [role, setRole] = useState("member");
  const [editingModules, setEditingModules] = useState<string | null>(null);
  const [memberModules, setMemberModules] = useState<string[]>([]);

  const isOwner = user?.role === "owner";
  const isAdmin = user?.role === "admin" || isOwner;

  useEffect(() => {
    loadMembers();
    fetchModules();
  }, [fetchModules]);

  const loadMembers = () => {
    api.get("/team/members").then((r) => setMembers(r.data)).catch(() => {});
  };

  const invite = async () => {
    await api.post("/team/invite", { email, role });
    setShowInvite(false);
    setEmail("");
    loadMembers();
  };

  const changeRole = async (memberId: string, newRole: string) => {
    await api.patch(`/team/members/${memberId}/role`, { role: newRole });
    loadMembers();
  };

  const openModuleAssign = async (memberId: string) => {
    const { data } = await api.get(`/team/members/${memberId}/modules`);
    setMemberModules(data.module_keys);
    setEditingModules(memberId);
  };

  const saveModules = async () => {
    if (!editingModules) return;
    await api.put(`/team/members/${editingModules}/modules`, { module_keys: memberModules });
    setEditingModules(null);
  };

  const toggleModule = (key: string) => {
    setMemberModules((prev) => prev.includes(key) ? prev.filter((k) => k !== key) : [...prev, key]);
  };

  const nonPermanentModules = modules.filter((m) => !m.is_permanent);

  const roleLabel: Record<string, string> = { owner: "Owner", admin: "Admin", member: "Member" };
  const roleColor: Record<string, string> = { owner: "bg-violet-100 text-violet-700", admin: "bg-blue-100 text-blue-700", member: "bg-gray-100 text-gray-600" };

  return (
    <div className="h-full overflow-y-auto p-4 sm:p-6 lg:p-8 max-w-4xl mx-auto space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">Tim</h1>
          <p className="text-sm text-gray-500 mt-1">Kelola anggota tim dan akses module.</p>
        </div>
        {isAdmin && (
          <button onClick={() => setShowInvite(true)} className="flex items-center gap-2 px-4 py-2 bg-blue-600 text-white text-sm rounded-lg hover:bg-blue-700">
            <Plus className="w-4 h-4" /> Invite Member
          </button>
        )}
      </div>

      {/* Invite Form */}
      {showInvite && (
        <div className="bg-white border border-gray-200 rounded-xl p-5 space-y-4">
          <h3 className="font-semibold text-gray-900">Invite Anggota Baru</h3>
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Email</label>
              <input type="email" value={email} onChange={(e) => setEmail(e.target.value)} placeholder="email@example.com"
                className="w-full h-9 px-3 rounded-lg border border-gray-200 text-sm focus:outline-none focus:border-blue-300" />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Role</label>
              <select value={role} onChange={(e) => setRole(e.target.value)}
                className="w-full h-9 px-3 rounded-lg border border-gray-200 text-sm focus:outline-none focus:border-blue-300">
                <option value="member">Member</option>
                {isOwner && <option value="admin">Admin</option>}
              </select>
            </div>
          </div>
          <div className="flex gap-2">
            <button onClick={invite} disabled={!email} className="px-4 py-2 bg-blue-600 text-white text-sm rounded-lg hover:bg-blue-700 disabled:opacity-50">Kirim Invite</button>
            <button onClick={() => setShowInvite(false)} className="px-4 py-2 text-gray-600 text-sm hover:bg-gray-100 rounded-lg">Batal</button>
          </div>
        </div>
      )}

      {/* Members List */}
      <div className="space-y-3">
        {members.map((m) => (
          <div key={m.id} className="bg-white border border-gray-200 rounded-xl p-4 flex items-center justify-between">
            <div className="flex items-center gap-3">
              <div className="w-10 h-10 rounded-full bg-gray-100 flex items-center justify-center text-sm font-semibold text-gray-600">
                {(m.name || m.email)[0].toUpperCase()}
              </div>
              <div>
                <p className="font-medium text-gray-900 text-sm">{m.name || m.email}</p>
                <p className="text-xs text-gray-400">{m.email}</p>
              </div>
            </div>
            <div className="flex items-center gap-2">
              <span className={`text-xs px-2.5 py-1 rounded-full font-medium ${roleColor[m.role] || roleColor.member}`}>
                {roleLabel[m.role] || m.role}
              </span>

              {/* Module assign button (only for members, by owner/admin) */}
              {m.role === "member" && isAdmin && (
                <button onClick={() => openModuleAssign(m.id)} className="p-2 text-gray-400 hover:text-blue-600 hover:bg-blue-50 rounded-lg" title="Assign Modules">
                  <Package className="w-4 h-4" />
                </button>
              )}

              {/* Role change (only by owner, not on self) */}
              {isOwner && m.id !== user?.id && m.role !== "owner" && (
                <select
                  value={m.role}
                  onChange={(e) => changeRole(m.id, e.target.value)}
                  className="text-xs h-8 px-2 rounded border border-gray-200 focus:outline-none focus:border-blue-300"
                >
                  <option value="admin">Admin</option>
                  <option value="member">Member</option>
                </select>
              )}
            </div>
          </div>
        ))}
      </div>

      {/* Module Assignment Modal */}
      {editingModules && (
        <div className="fixed inset-0 bg-black/30 z-50 flex items-center justify-center p-4" onClick={() => setEditingModules(null)}>
          <div className="bg-white rounded-xl p-6 w-full max-w-md space-y-4" onClick={(e) => e.stopPropagation()}>
            <h3 className="font-semibold text-gray-900">Assign Module Access</h3>
            <p className="text-sm text-gray-500">Pilih module yang bisa diakses member ini:</p>
            <div className="space-y-2 max-h-64 overflow-y-auto">
              {nonPermanentModules.map((mod) => (
                <label key={mod.key} className="flex items-center gap-3 p-2 rounded-lg hover:bg-gray-50 cursor-pointer">
                  <input type="checkbox" checked={memberModules.includes(mod.key)} onChange={() => toggleModule(mod.key)}
                    className="rounded border-gray-300" />
                  <div className={`w-8 h-8 ${mod.color} rounded flex items-center justify-center`}>
                    <mod.icon className="w-4 h-4 text-white" />
                  </div>
                  <span className="text-sm text-gray-700">{mod.name}</span>
                </label>
              ))}
            </div>
            <div className="flex gap-2 pt-2">
              <button onClick={saveModules} className="px-4 py-2 bg-blue-600 text-white text-sm rounded-lg hover:bg-blue-700">Simpan</button>
              <button onClick={() => setEditingModules(null)} className="px-4 py-2 text-gray-600 text-sm hover:bg-gray-100 rounded-lg">Batal</button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
