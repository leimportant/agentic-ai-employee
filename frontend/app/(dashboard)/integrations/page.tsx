"use client";

import { useState } from "react";
import { MessageSquare, Send, Mail, Globe, Instagram, ShoppingBag, CheckCircle2, Circle, Settings, ExternalLink, Search } from "lucide-react";
import type { LucideIcon } from "lucide-react";

interface Integration {
  id: string;
  name: string;
  description: string;
  icon: LucideIcon;
  color: string;
  bgColor: string;
  status: "connected" | "available" | "coming_soon";
  category: "messaging" | "email" | "web" | "marketplace";
}

const integrations: Integration[] = [
  {
    id: "whatsapp",
    name: "WhatsApp Business",
    description: "Terima & balas pesan WhatsApp otomatis via AI Agent",
    icon: MessageSquare,
    color: "text-green-600",
    bgColor: "bg-green-50",
    status: "connected",
    category: "messaging",
  },
  {
    id: "telegram",
    name: "Telegram Bot",
    description: "Chatbot Telegram untuk CS, notifikasi, dan OTP",
    icon: Send,
    color: "text-blue-500",
    bgColor: "bg-blue-50",
    status: "available",
    category: "messaging",
  },
  {
    id: "email",
    name: "Email (SMTP)",
    description: "Kirim email otomatis: notifikasi, marketing, invoice",
    icon: Mail,
    color: "text-amber-600",
    bgColor: "bg-amber-50",
    status: "available",
    category: "email",
  },
  {
    id: "webchat",
    name: "Web Chat Widget",
    description: "Embed chat widget di website kamu untuk live CS",
    icon: Globe,
    color: "text-indigo-600",
    bgColor: "bg-indigo-50",
    status: "available",
    category: "web",
  },
  {
    id: "instagram",
    name: "Instagram DM",
    description: "Auto-reply DM Instagram dari customer",
    icon: Instagram,
    color: "text-pink-600",
    bgColor: "bg-pink-50",
    status: "coming_soon",
    category: "messaging",
  },
  {
    id: "shopee",
    name: "Shopee Chat",
    description: "Integrasi chat Shopee untuk CS toko online",
    icon: ShoppingBag,
    color: "text-orange-600",
    bgColor: "bg-orange-50",
    status: "coming_soon",
    category: "marketplace",
  },
];

const categories = [
  { id: "all", label: "Semua" },
  { id: "messaging", label: "Messaging" },
  { id: "email", label: "Email" },
  { id: "web", label: "Web" },
  { id: "marketplace", label: "Marketplace" },
];

export default function IntegrationsPage() {
  const [filter, setFilter] = useState("all");
  const [search, setSearch] = useState("");

  const filtered = integrations.filter((i) => {
    const matchCategory = filter === "all" || i.category === filter;
    const matchSearch = i.name.toLowerCase().includes(search.toLowerCase());
    return matchCategory && matchSearch;
  });

  const connected = integrations.filter((i) => i.status === "connected").length;

  return (
    <div className="h-full overflow-y-auto p-4 sm:p-6 lg:p-8 max-w-6xl mx-auto space-y-6">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">Integrations</h1>
          <p className="text-gray-500 text-sm mt-1">
            Hubungkan AI Agent ke channel komunikasi pelanggan. <span className="text-blue-600 font-medium">{connected} aktif</span>
          </p>
        </div>
        <div className="relative w-full sm:w-64">
          <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-gray-400" />
          <input
            type="text"
            placeholder="Cari integrasi..."
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            className="w-full h-9 pl-9 pr-3 rounded-lg border border-gray-200 bg-white text-sm focus:outline-none focus:border-blue-300"
          />
        </div>
      </div>

      {/* Category Filter */}
      <div className="flex gap-2 flex-wrap">
        {categories.map((cat) => (
          <button
            key={cat.id}
            onClick={() => setFilter(cat.id)}
            className={`px-3 py-1.5 rounded-lg text-sm font-medium transition-colors ${
              filter === cat.id
                ? "bg-blue-600 text-white"
                : "bg-gray-100 text-gray-600 hover:bg-gray-200"
            }`}
          >
            {cat.label}
          </button>
        ))}
      </div>

      {/* Integration Cards */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
        {filtered.map((item) => (
          <div
            key={item.id}
            className={`bg-white border rounded-xl p-5 flex flex-col ${
              item.status === "coming_soon" ? "opacity-60 border-gray-100" : "border-gray-200 hover:border-blue-200 hover:shadow-sm transition-all"
            }`}
          >
            {/* Icon + Status */}
            <div className="flex items-start justify-between mb-4">
              <div className={`w-11 h-11 ${item.bgColor} rounded-xl flex items-center justify-center`}>
                <item.icon className={`w-5 h-5 ${item.color}`} />
              </div>
              {item.status === "connected" && (
                <span className="flex items-center gap-1 text-xs font-medium text-emerald-600 bg-emerald-50 px-2 py-1 rounded-full">
                  <CheckCircle2 className="w-3 h-3" /> Connected
                </span>
              )}
              {item.status === "coming_soon" && (
                <span className="text-xs font-medium text-gray-400 bg-gray-100 px-2 py-1 rounded-full">
                  Coming Soon
                </span>
              )}
              {item.status === "available" && (
                <span className="flex items-center gap-1 text-xs font-medium text-gray-500">
                  <Circle className="w-3 h-3" /> Belum aktif
                </span>
              )}
            </div>

            {/* Info */}
            <h3 className="font-semibold text-gray-900">{item.name}</h3>
            <p className="text-sm text-gray-500 mt-1 flex-1">{item.description}</p>

            {/* Action */}
            <div className="mt-4 pt-4 border-t border-gray-100">
              {item.status === "connected" && (
                <div className="flex items-center gap-2">
                  <button className="flex-1 flex items-center justify-center gap-1.5 text-sm font-medium text-gray-700 bg-gray-100 hover:bg-gray-200 py-2 rounded-lg transition-colors">
                    <Settings className="w-3.5 h-3.5" /> Kelola
                  </button>
                  <button className="flex items-center justify-center gap-1.5 text-sm font-medium text-red-600 hover:bg-red-50 px-3 py-2 rounded-lg transition-colors">
                    Disconnect
                  </button>
                </div>
              )}
              {item.status === "available" && (
                <button className="w-full flex items-center justify-center gap-1.5 text-sm font-medium text-white bg-blue-600 hover:bg-blue-700 py-2 rounded-lg transition-colors">
                  <ExternalLink className="w-3.5 h-3.5" /> Connect
                </button>
              )}
              {item.status === "coming_soon" && (
                <button className="w-full text-sm font-medium text-gray-400 bg-gray-50 py-2 rounded-lg cursor-not-allowed">
                  Segera Hadir
                </button>
              )}
            </div>
          </div>
        ))}
      </div>

      {filtered.length === 0 && (
        <div className="text-center py-12 text-gray-500 text-sm">
          Tidak ada integrasi yang cocok dengan filter.
        </div>
      )}
    </div>
  );
}
