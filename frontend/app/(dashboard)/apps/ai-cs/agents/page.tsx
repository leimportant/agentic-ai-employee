"use client";

import { useEffect, useState } from "react";
import { Bot, Plus, Power, Pencil, Trash2 } from "lucide-react";
import { api } from "@/lib/api";

interface Agent {
  id: string;
  name: string;
  type: string;
  system_prompt: string;
  is_active: boolean;
}

export default function AgentsPage() {
  const [agents, setAgents] = useState<Agent[]>([]);
  const [showCreate, setShowCreate] = useState(false);
  const [name, setName] = useState("");
  const [prompt, setPrompt] = useState("Kamu adalah AI Customer Service yang ramah dan membantu.");

  useEffect(() => {
    loadAgents();
  }, []);

  const loadAgents = () => {
    api.get("/ai-agents").then((r) => setAgents(r.data));
  };

  const create = async () => {
    await api.post("/ai-agents", { name, system_prompt: prompt });
    setShowCreate(false);
    setName("");
    loadAgents();
  };

  const toggle = async (agent: Agent) => {
    await api.put(`/ai-agents/${agent.id}`, { is_active: !agent.is_active });
    loadAgents();
  };

  const remove = async (id: string) => {
    if (!confirm("Hapus agent ini?")) return;
    await api.delete(`/ai-agents/${id}`);
    loadAgents();
  };

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h1 className="text-xl font-bold text-gray-900">AI Agents</h1>
        <button onClick={() => setShowCreate(true)} className="flex items-center gap-2 px-4 py-2 bg-blue-600 text-white text-sm rounded-lg hover:bg-blue-700">
          <Plus className="w-4 h-4" /> Buat Agent
        </button>
      </div>

      {/* Create Form */}
      {showCreate && (
        <div className="bg-white border border-gray-200 rounded-xl p-5 space-y-4">
          <h3 className="font-semibold text-gray-900">Agent Baru</h3>
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">Nama Agent</label>
            <input type="text" value={name} onChange={(e) => setName(e.target.value)} placeholder="CS WhatsApp"
              className="w-full h-9 px-3 rounded-lg border border-gray-200 text-sm focus:outline-none focus:border-blue-300" />
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">System Prompt</label>
            <textarea value={prompt} onChange={(e) => setPrompt(e.target.value)} rows={4}
              className="w-full px-3 py-2 rounded-lg border border-gray-200 text-sm focus:outline-none focus:border-blue-300" />
          </div>
          <div className="flex gap-2">
            <button onClick={create} disabled={!name} className="px-4 py-2 bg-blue-600 text-white text-sm rounded-lg hover:bg-blue-700 disabled:opacity-50">Simpan</button>
            <button onClick={() => setShowCreate(false)} className="px-4 py-2 text-gray-600 text-sm hover:bg-gray-100 rounded-lg">Batal</button>
          </div>
        </div>
      )}

      {/* Agent List */}
      <div className="space-y-3">
        {agents.length === 0 && !showCreate && (
          <div className="text-center py-12 bg-white rounded-xl border border-gray-200">
            <Bot className="w-10 h-10 text-gray-300 mx-auto mb-3" />
            <p className="text-gray-500 text-sm">Belum ada agent. Buat agent pertama kamu.</p>
          </div>
        )}
        {agents.map((agent) => (
          <div key={agent.id} className="bg-white border border-gray-200 rounded-xl p-4 flex items-center justify-between">
            <div className="flex items-center gap-3">
              <div className={`w-10 h-10 rounded-lg flex items-center justify-center ${agent.is_active ? "bg-emerald-100" : "bg-gray-100"}`}>
                <Bot className={`w-5 h-5 ${agent.is_active ? "text-emerald-600" : "text-gray-400"}`} />
              </div>
              <div>
                <div className="flex items-center gap-2">
                  <h3 className="font-medium text-gray-900 text-sm">{agent.name}</h3>
                  <span className={`text-xs px-2 py-0.5 rounded-full ${agent.is_active ? "bg-emerald-50 text-emerald-600" : "bg-gray-100 text-gray-500"}`}>
                    {agent.is_active ? "Running" : "Stopped"}
                  </span>
                </div>
                <p className="text-xs text-gray-400 mt-0.5 truncate max-w-md">{agent.system_prompt.slice(0, 80)}...</p>
              </div>
            </div>
            <div className="flex items-center gap-1">
              <button onClick={() => toggle(agent)} title={agent.is_active ? "Stop" : "Start"}
                className={`p-2 rounded-lg ${agent.is_active ? "text-emerald-600 hover:bg-emerald-50" : "text-gray-400 hover:bg-gray-100"}`}>
                <Power className="w-4 h-4" />
              </button>
              <button onClick={() => remove(agent.id)} className="p-2 text-gray-400 hover:text-red-500 hover:bg-red-50 rounded-lg">
                <Trash2 className="w-4 h-4" />
              </button>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
