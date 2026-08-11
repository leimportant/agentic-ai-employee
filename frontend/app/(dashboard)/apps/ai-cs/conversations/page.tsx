"use client";

import { useEffect, useState } from "react";
import { MessageSquare } from "lucide-react";
import { api } from "@/lib/api";

interface Conversation {
  id: string;
  ai_agent_id: string;
  customer_id: string;
  channel: string;
  status: string;
  created_at: string;
}

interface Message {
  id: string;
  role: string;
  content: string;
  created_at: string;
}

interface ConversationDetail extends Conversation {
  messages: Message[];
}

export default function ConversationsPage() {
  const [conversations, setConversations] = useState<Conversation[]>([]);
  const [selected, setSelected] = useState<ConversationDetail | null>(null);

  useEffect(() => {
    api.get("/conversations").then((r) => setConversations(r.data));
  }, []);

  const selectConvo = async (id: string) => {
    const { data } = await api.get(`/conversations/${id}`);
    setSelected(data);
  };

  return (
    <div className="flex h-full -m-4 sm:-m-6">
      {/* Conversation List */}
      <div className="w-72 border-r border-gray-200 bg-white flex flex-col shrink-0">
        <div className="p-4 border-b border-gray-100">
          <h2 className="font-semibold text-gray-900 text-sm">Conversations</h2>
          <p className="text-xs text-gray-400">{conversations.length} total</p>
        </div>
        <div className="flex-1 overflow-y-auto divide-y divide-gray-50">
          {conversations.map((c) => (
            <button
              key={c.id}
              onClick={() => selectConvo(c.id)}
              className={`w-full text-left px-4 py-3 hover:bg-gray-50 transition-colors ${selected?.id === c.id ? "bg-blue-50" : ""}`}
            >
              <div className="flex items-center gap-2">
                <span className={`w-2 h-2 rounded-full shrink-0 ${c.status === "active" ? "bg-emerald-500" : "bg-gray-300"}`} />
                <span className="text-sm text-gray-900 truncate">{c.id.slice(0, 12)}</span>
              </div>
              <div className="flex items-center gap-2 mt-1">
                <span className="text-xs text-gray-400">{c.channel}</span>
                <span className="text-xs text-gray-300">•</span>
                <span className="text-xs text-gray-400">{new Date(c.created_at).toLocaleDateString("id-ID")}</span>
              </div>
            </button>
          ))}
          {conversations.length === 0 && (
            <div className="p-6 text-center">
              <MessageSquare className="w-8 h-8 text-gray-200 mx-auto mb-2" />
              <p className="text-xs text-gray-400">Belum ada conversation</p>
            </div>
          )}
        </div>
      </div>

      {/* Chat View */}
      <div className="flex-1 flex flex-col bg-gray-50">
        {selected ? (
          <>
            <div className="px-5 py-3 bg-white border-b border-gray-200">
              <p className="text-sm font-medium text-gray-900">Conversation #{selected.id.slice(0, 8)}</p>
              <p className="text-xs text-gray-400">{selected.channel} • {selected.status} • {selected.messages.length} messages</p>
            </div>
            <div className="flex-1 overflow-y-auto p-5 space-y-3">
              {selected.messages.map((msg) => (
                <div key={msg.id} className={`flex ${msg.role === "user" ? "justify-end" : "justify-start"}`}>
                  <div className={`max-w-[70%] px-4 py-2.5 rounded-xl text-sm ${
                    msg.role === "user"
                      ? "bg-blue-600 text-white rounded-br-sm"
                      : "bg-white border border-gray-200 text-gray-800 rounded-bl-sm"
                  }`}>
                    <p>{msg.content}</p>
                    <p className={`text-[10px] mt-1 ${msg.role === "user" ? "text-blue-200" : "text-gray-300"}`}>
                      {msg.created_at ? new Date(msg.created_at).toLocaleTimeString("id-ID", { hour: "2-digit", minute: "2-digit" }) : ""}
                    </p>
                  </div>
                </div>
              ))}
            </div>
          </>
        ) : (
          <div className="flex-1 flex items-center justify-center">
            <div className="text-center">
              <MessageSquare className="w-12 h-12 text-gray-200 mx-auto mb-3" />
              <p className="text-sm text-gray-400">Pilih conversation untuk melihat chat</p>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
