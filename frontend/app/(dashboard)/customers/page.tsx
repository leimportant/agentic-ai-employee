"use client";

import { useEffect, useState } from "react";
import { Users, Plus, Search, MessageSquare, Phone, Mail, Trash2 } from "lucide-react";
import { useCustomerStore } from "@/lib/stores/useCustomerStore";
import { useAuthStore } from "@/lib/stores/useAuthStore";

const channelIcons: Record<string, typeof MessageSquare> = {
  whatsapp: Phone,
  telegram: MessageSquare,
  email: Mail,
  webchat: MessageSquare,
};

export default function CustomersPage() {
  const { user } = useAuthStore();
  const { customers, loading, fetch, remove } = useCustomerStore();
  const [search, setSearch] = useState("");

  useEffect(() => {
    if (user) fetch(user.tenant_id);
  }, [user, fetch]);

  const filtered = customers.filter((c) =>
    c.name.toLowerCase().includes(search.toLowerCase()) ||
    c.email?.toLowerCase().includes(search.toLowerCase()) ||
    c.phone?.includes(search)
  );

  return (
    <div className="h-full overflow-y-auto p-4 sm:p-6 lg:p-8 max-w-6xl mx-auto space-y-6">
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">Customers</h1>
          <p className="text-gray-500 text-sm mt-1">{customers.length} total pelanggan</p>
        </div>
        <button className="flex items-center gap-1.5 bg-blue-600 text-white text-sm font-medium px-4 py-2.5 rounded-lg hover:bg-blue-700 shrink-0">
          <Plus className="w-4 h-4" /> Tambah Customer
        </button>
      </div>

      {/* Search */}
      <div className="relative max-w-sm">
        <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-gray-400" />
        <input
          type="text"
          value={search}
          onChange={(e) => setSearch(e.target.value)}
          placeholder="Cari nama, email, atau telepon..."
          className="w-full h-9 pl-9 pr-3 rounded-lg border border-gray-200 bg-white text-sm focus:outline-none focus:border-blue-300"
        />
      </div>

      {/* Table */}
      {loading ? (
        <div className="text-center py-12 text-gray-400 text-sm">Memuat data...</div>
      ) : filtered.length > 0 ? (
        <div className="bg-white border border-gray-200 rounded-xl overflow-hidden">
          <table className="w-full text-sm">
            <thead className="bg-gray-50 border-b border-gray-200">
              <tr>
                <th className="text-left px-5 py-3 text-gray-600 font-medium">Nama</th>
                <th className="text-left px-5 py-3 text-gray-600 font-medium hidden sm:table-cell">Kontak</th>
                <th className="text-left px-5 py-3 text-gray-600 font-medium hidden md:table-cell">Channel</th>
                <th className="text-left px-5 py-3 text-gray-600 font-medium hidden lg:table-cell">Terakhir Chat</th>
                <th className="px-5 py-3" />
              </tr>
            </thead>
            <tbody>
              {filtered.map((c) => {
                const ChIcon = channelIcons[c.channel] || MessageSquare;
                return (
                  <tr key={c.id} className="border-b border-gray-100 last:border-0 hover:bg-gray-50">
                    <td className="px-5 py-3">
                      <div className="flex items-center gap-3">
                        <div className="w-8 h-8 rounded-full bg-blue-50 text-blue-700 flex items-center justify-center text-xs font-semibold shrink-0">
                          {c.name.split(" ").map((w) => w[0]).join("").slice(0, 2).toUpperCase()}
                        </div>
                        <span className="font-medium text-gray-900">{c.name}</span>
                      </div>
                    </td>
                    <td className="px-5 py-3 text-gray-600 hidden sm:table-cell">{c.email || c.phone || "-"}</td>
                    <td className="px-5 py-3 hidden md:table-cell">
                      <span className="flex items-center gap-1.5 text-gray-500">
                        <ChIcon className="w-3.5 h-3.5" /> {c.channel}
                      </span>
                    </td>
                    <td className="px-5 py-3 text-gray-400 text-xs hidden lg:table-cell">
                      {c.last_message_at ? new Date(c.last_message_at).toLocaleDateString("id-ID") : "-"}
                    </td>
                    <td className="px-5 py-3">
                      <button
                        onClick={() => user && remove(user.tenant_id, c.id)}
                        className="p-1.5 text-gray-400 hover:text-red-500 hover:bg-red-50 rounded"
                      >
                        <Trash2 className="w-3.5 h-3.5" />
                      </button>
                    </td>
                  </tr>
                );
              })}
            </tbody>
          </table>
        </div>
      ) : (
        <div className="text-center py-16 bg-white rounded-xl border border-gray-200">
          <Users className="w-10 h-10 text-gray-300 mx-auto mb-3" />
          <p className="text-gray-500 text-sm mb-1">
            {search ? "Tidak ditemukan customer yang cocok" : "Belum ada customer"}
          </p>
          {!search && <p className="text-gray-400 text-xs">Customer akan otomatis ditambahkan saat chat masuk</p>}
        </div>
      )}
    </div>
  );
}
