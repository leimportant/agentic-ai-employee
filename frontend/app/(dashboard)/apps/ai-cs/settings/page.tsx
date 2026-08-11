"use client";

import { useState } from "react";
import { Copy, Check } from "lucide-react";
import { useAuthStore } from "@/lib/stores/useAuthStore";

export default function AiCsSettingsPage() {
  const { user } = useAuthStore();
  const [waToken, setWaToken] = useState("");
  const [saved, setSaved] = useState(false);
  const [copied, setCopied] = useState(false);

  const webhookUrl = `${process.env.NEXT_PUBLIC_API_URL?.replace("/api/v1", "") || "http://localhost:8000"}/api/v1/webhook/whatsapp/${user?.tenant_id || "YOUR_TENANT_ID"}`;

  const copyWebhook = () => {
    navigator.clipboard.writeText(webhookUrl);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  const save = () => {
    // TODO: save wa_api_token to tenant settings via API
    setSaved(true);
    setTimeout(() => setSaved(false), 2000);
  };

  return (
    <div className="space-y-6 max-w-2xl">
      <h1 className="text-xl font-bold text-gray-900">Settings</h1>

      {/* WhatsApp Integration */}
      <div className="bg-white border border-gray-200 rounded-xl p-5 space-y-4">
        <h3 className="font-semibold text-gray-900">WhatsApp Integration (Fonnte)</h3>
        <p className="text-sm text-gray-500">Hubungkan chatbot ke WhatsApp melalui Fonnte API.</p>

        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">Webhook URL</label>
          <p className="text-xs text-gray-400 mb-2">Masukkan URL ini di dashboard Fonnte → Webhook URL:</p>
          <div className="flex items-center gap-2">
            <code className="flex-1 text-xs bg-gray-50 border border-gray-200 rounded-lg px-3 py-2 text-gray-700 break-all">{webhookUrl}</code>
            <button onClick={copyWebhook} className="p-2 text-gray-400 hover:text-blue-600 hover:bg-blue-50 rounded-lg shrink-0">
              {copied ? <Check className="w-4 h-4 text-emerald-600" /> : <Copy className="w-4 h-4" />}
            </button>
          </div>
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">Fonnte API Token</label>
          <input
            type="password"
            value={waToken}
            onChange={(e) => setWaToken(e.target.value)}
            placeholder="Masukkan token dari dashboard Fonnte"
            className="w-full h-9 px-3 rounded-lg border border-gray-200 text-sm focus:outline-none focus:border-blue-300"
          />
        </div>

        <button onClick={save} className="px-4 py-2 bg-blue-600 text-white text-sm rounded-lg hover:bg-blue-700">
          {saved ? "Tersimpan!" : "Simpan"}
        </button>
      </div>

      {/* Setup Guide */}
      <div className="bg-blue-50 border border-blue-200 rounded-xl p-5">
        <h4 className="font-semibold text-blue-900 text-sm mb-2">Cara Setup:</h4>
        <ol className="text-sm text-blue-800 space-y-1 list-decimal list-inside">
          <li>Daftar di <a href="https://fonnte.com" target="_blank" className="underline">fonnte.com</a></li>
          <li>Scan QR WhatsApp di dashboard Fonnte</li>
          <li>Copy API Token → paste di field di atas</li>
          <li>Copy Webhook URL di atas → paste di dashboard Fonnte</li>
          <li>Selesai! Pesan masuk akan otomatis dijawab oleh AI Agent kamu</li>
        </ol>
      </div>
    </div>
  );
}
