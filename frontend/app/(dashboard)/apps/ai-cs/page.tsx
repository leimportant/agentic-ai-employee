"use client";

import { useEffect, useState } from "react";
import { MessageSquare, Bot, Users, TrendingUp } from "lucide-react";
import { api } from "@/lib/api";

interface Agent {
  id: string;
  name: string;
  type: string;
  is_active: boolean;
}

interface Conversation {
  id: string;
  channel: string;
  status: string;
  created_at: string;
}

export default function AiCsDashboard() {
  const [agents, setAgents] = useState<Agent[]>([]);
  const [conversations, setConversations] = useState<Conversation[]>([]);

  useEffect(() => {
    api.get("/ai-agents").then((r) => setAgents(r.data)).catch(() => {});
    api.get("/conversations").then((r) => setConversations(r.data)).catch(() => {});
  }, []);

  const activeAgents = agents.filter((a) => a.is_active).length;
  const todayConvos = conversations.filter(
    (c) => new Date(c.created_at).toDateString() === new Date().toDateString()
  ).length;

  const stats = [
    { label: "Total Chat Hari Ini", value: String(todayConvos), icon: MessageSquare, color: "blue" },
    { label: "Agents Aktif", value: String(activeAgents), icon: Bot, color: "violet" },
    { label: "Total Conversations", value: String(conversations.length), icon: Users, color: "emerald" },
    { label: "Agents Total", value: String(agents.length), icon: TrendingUp, color: "amber" },
  ];

  return (
    <div className="space-y-6">
      <h1 className="text-xl font-bold text-gray-900">CS Dashboard</h1>
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        {stats.map((s) => (
          <div key={s.label} className="bg-white rounded-xl border border-gray-200 p-4">
            <s.icon className={`w-5 h-5 mb-2 ${
              s.color === "blue" ? "text-blue-600" :
              s.color === "violet" ? "text-violet-600" :
              s.color === "emerald" ? "text-emerald-600" : "text-amber-600"
            }`} />
            <p className="text-2xl font-bold text-gray-900">{s.value}</p>
            <p className="text-xs text-gray-500">{s.label}</p>
          </div>
        ))}
      </div>

      {/* Recent Conversations */}
      <div className="bg-white rounded-xl border border-gray-200 p-5">
        <h2 className="font-semibold text-gray-900 mb-3">Conversations Terbaru</h2>
        {conversations.length === 0 ? (
          <p className="text-sm text-gray-400 py-4 text-center">Belum ada conversation.</p>
        ) : (
          <div className="divide-y divide-gray-100">
            {conversations.slice(0, 10).map((c) => (
              <div key={c.id} className="py-2.5 flex items-center justify-between">
                <div className="flex items-center gap-3">
                  <span className={`w-2 h-2 rounded-full ${c.status === "active" ? "bg-emerald-500" : "bg-gray-300"}`} />
                  <span className="text-sm text-gray-700">{c.id.slice(0, 8)}...</span>
                  <span className="text-xs text-gray-400">{c.channel}</span>
                </div>
                <span className="text-xs text-gray-400">{new Date(c.created_at).toLocaleString("id-ID")}</span>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}
