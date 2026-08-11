"use client";

import { useState, useEffect, Suspense } from "react";
import { useSearchParams, useRouter } from "next/navigation";
import { Upload, CheckCircle, Copy, Building2 } from "lucide-react";
import { api } from "@/lib/api";
import { useAuthStore } from "@/lib/stores/useAuthStore";
import { useBillingStore } from "@/lib/stores/useBillingStore";

export default function PayPage() {
  return (
    <Suspense fallback={<div className="p-8 text-gray-400">Loading...</div>}>
      <PayContent />
    </Suspense>
  );
}

function PayContent() {
  const searchParams = useSearchParams();
  const router = useRouter();
  const { user } = useAuthStore();
  const { plans, fetchPlans } = useBillingStore();
  const planId = searchParams.get("plan_id");

  const [bankInfo, setBankInfo] = useState<{ bank_name: string; account_number: string; account_name: string } | null>(null);
  const [file, setFile] = useState<File | null>(null);
  const [bankName, setBankName] = useState("");
  const [accountName, setAccountName] = useState("");
  const [submitting, setSubmitting] = useState(false);
  const [done, setDone] = useState(false);
  const [copied, setCopied] = useState(false);

  const plan = plans.find((p) => p.id === planId);

  useEffect(() => { fetchPlans(); }, [fetchPlans]);
  useEffect(() => {
    api.get("/billing/bank-info").then((r) => setBankInfo(r.data));
  }, []);

  const copyRek = () => {
    if (bankInfo) {
      navigator.clipboard.writeText(bankInfo.account_number);
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    }
  };

  const submit = async () => {
    if (!file || !planId || !user) return;
    setSubmitting(true);
    const form = new FormData();
    form.append("plan_id", planId);
    form.append("amount", plan?.price_monthly || "");
    form.append("bank_name", bankName);
    form.append("account_name", accountName);
    form.append("proof", file);
    try {
      await api.post("/billing/pay", form, { headers: { "Content-Type": "multipart/form-data" } });
      setDone(true);
    } finally {
      setSubmitting(false);
    }
  };

  if (done) {
    return (
      <div className="h-full flex items-center justify-center p-6">
        <div className="text-center max-w-sm">
          <CheckCircle className="w-16 h-16 text-emerald-500 mx-auto mb-4" />
          <h2 className="text-xl font-bold text-gray-900 mb-2">Bukti Transfer Diterima</h2>
          <p className="text-gray-500 text-sm mb-6">Tim kami akan memverifikasi pembayaran kamu dalam 1x24 jam (biasanya kurang dari 1 jam).</p>
          <button onClick={() => router.push("/billing")} className="px-6 py-2.5 bg-blue-600 text-white text-sm font-medium rounded-lg hover:bg-blue-700">
            Kembali ke Billing
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="h-full overflow-y-auto p-4 sm:p-6 lg:p-8 max-w-lg mx-auto space-y-6">
      <div>
        <h1 className="text-xl font-bold text-gray-900">Konfirmasi Pembayaran</h1>
        {plan && <p className="text-sm text-gray-500 mt-1">Plan <strong>{plan.name}</strong> — {plan.price_monthly}/bulan</p>}
      </div>

      {/* Bank Info */}
      {bankInfo && (
        <div className="bg-blue-50 border border-blue-200 rounded-xl p-5">
          <div className="flex items-center gap-2 mb-3">
            <Building2 className="w-5 h-5 text-blue-600" />
            <h3 className="font-semibold text-blue-900">Transfer ke:</h3>
          </div>
          <div className="space-y-2 text-sm">
            <div className="flex justify-between">
              <span className="text-gray-600">Bank</span>
              <span className="font-medium text-gray-900">{bankInfo.bank_name}</span>
            </div>
            <div className="flex justify-between items-center">
              <span className="text-gray-600">No. Rekening</span>
              <div className="flex items-center gap-2">
                <span className="font-mono font-medium text-gray-900">{bankInfo.account_number}</span>
                <button onClick={copyRek} className="text-blue-600 hover:text-blue-700">
                  <Copy className="w-4 h-4" />
                </button>
                {copied && <span className="text-xs text-emerald-600">Copied!</span>}
              </div>
            </div>
            <div className="flex justify-between">
              <span className="text-gray-600">Atas Nama</span>
              <span className="font-medium text-gray-900">{bankInfo.account_name}</span>
            </div>
            {plan && (
              <div className="flex justify-between pt-2 border-t border-blue-200">
                <span className="text-gray-600 font-medium">Jumlah Transfer</span>
                <span className="font-bold text-blue-900">{plan.price_monthly}</span>
              </div>
            )}
          </div>
        </div>
      )}

      {/* Form */}
      <div className="bg-white border border-gray-200 rounded-xl p-5 space-y-4">
        <h3 className="font-semibold text-gray-900">Upload Bukti Transfer</h3>

        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">Bank Pengirim</label>
          <input type="text" value={bankName} onChange={(e) => setBankName(e.target.value)} placeholder="BCA / Mandiri / BNI / dll"
            className="w-full h-9 px-3 rounded-lg border border-gray-200 text-sm focus:outline-none focus:border-blue-300" />
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">Nama Pengirim</label>
          <input type="text" value={accountName} onChange={(e) => setAccountName(e.target.value)} placeholder="Nama sesuai rekening"
            className="w-full h-9 px-3 rounded-lg border border-gray-200 text-sm focus:outline-none focus:border-blue-300" />
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">Bukti Transfer</label>
          <label className="flex flex-col items-center justify-center border-2 border-dashed border-gray-200 rounded-lg p-6 cursor-pointer hover:border-blue-300 hover:bg-blue-50/30 transition-colors">
            <Upload className="w-8 h-8 text-gray-300 mb-2" />
            <span className="text-sm text-gray-500">{file ? file.name : "Klik untuk upload gambar"}</span>
            <span className="text-xs text-gray-400 mt-1">JPG, PNG, atau PDF</span>
            <input type="file" accept="image/*,.pdf" className="hidden" onChange={(e) => setFile(e.target.files?.[0] || null)} />
          </label>
        </div>

        <button
          onClick={submit}
          disabled={!file || !bankName || !accountName || submitting}
          className="w-full py-2.5 bg-blue-600 text-white text-sm font-medium rounded-lg hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
        >
          {submitting ? "Mengirim..." : "Kirim Bukti Transfer"}
        </button>
      </div>
    </div>
  );
}
