"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import { MessageSquare, TrendingUp, Headphones, Factory, Package, ArrowRight, ArrowLeft, Check, Sparkles } from "lucide-react";
import { usePlatformStore } from "@/lib/store";

const steps = ["Tujuan", "Pilih Apps", "Selesai"];

const useCases = [
  { id: "cs", label: "Customer Service", desc: "Auto-reply chat dari pelanggan 24/7", icon: MessageSquare },
  { id: "sales", label: "Sales & Marketing", desc: "Follow-up lead & closing otomatis", icon: TrendingUp },
  { id: "support", label: "Support & Ticketing", desc: "Manajemen tiket & knowledge base", icon: Headphones },
  { id: "operations", label: "Operasional / Produksi", desc: "Monitoring produksi & order tracking", icon: Factory },
  { id: "inventory", label: "Inventory & Stok", desc: "Kelola stok & product catalog", icon: Package },
];

const appSuggestions: Record<string, string[]> = {
  cs: ["ai-cs"],
  sales: ["ai-sales"],
  support: ["ai-support"],
  operations: ["konveksi"],
  inventory: ["inventory"],
};

export default function OnboardingPage() {
  const router = useRouter();
  const { activateApp } = usePlatformStore();
  const [step, setStep] = useState(0);
  const [selectedCases, setSelectedCases] = useState<string[]>([]);
  const [companyName, setCompanyName] = useState("");

  const toggleCase = (id: string) => {
    setSelectedCases((prev) => prev.includes(id) ? prev.filter((c) => c !== id) : [...prev, id]);
  };

  const suggestedApps = [...new Set(selectedCases.flatMap((c) => appSuggestions[c] || []))];

  const handleFinish = () => {
    suggestedApps.forEach((appId) => activateApp(appId));
    router.push("/home");
  };

  return (
    <div className="min-h-screen bg-gray-50 flex items-center justify-center p-4">
      <div className="w-full max-w-lg bg-white rounded-2xl shadow-lg border border-gray-100 overflow-hidden">
        {/* Progress */}
        <div className="px-6 pt-6">
          <div className="flex items-center gap-2 mb-6">
            {steps.map((s, i) => (
              <div key={s} className="flex items-center gap-2">
                <div className={`w-7 h-7 rounded-full flex items-center justify-center text-xs font-semibold ${
                  i < step ? "bg-blue-600 text-white" :
                  i === step ? "bg-blue-100 text-blue-700 ring-2 ring-blue-200" :
                  "bg-gray-100 text-gray-400"
                }`}>
                  {i < step ? <Check className="w-3.5 h-3.5" /> : i + 1}
                </div>
                {i < steps.length - 1 && <div className={`w-8 h-0.5 ${i < step ? "bg-blue-600" : "bg-gray-200"}`} />}
              </div>
            ))}
            <span className="ml-2 text-xs text-gray-400">{steps[step]}</span>
          </div>
        </div>

        <div className="px-6 pb-6">
          {/* Step 0: Use case */}
          {step === 0 && (
            <div className="space-y-4">
              <div>
                <h2 className="text-xl font-bold text-gray-900">Apa tujuan kamu? 🎯</h2>
                <p className="text-sm text-gray-500 mt-1">Pilih satu atau lebih, kami akan merekomendasikan apps yang cocok.</p>
              </div>

              <div>
                <label className="text-xs text-gray-500 mb-1.5 block">Nama bisnis (opsional)</label>
                <input
                  type="text"
                  value={companyName}
                  onChange={(e) => setCompanyName(e.target.value)}
                  placeholder="PT Maju Jaya"
                  className="w-full h-10 px-3 rounded-lg border border-gray-200 text-sm focus:outline-none focus:border-blue-300"
                />
              </div>

              <div className="space-y-2">
                {useCases.map((uc) => (
                  <button
                    key={uc.id}
                    onClick={() => toggleCase(uc.id)}
                    className={`w-full flex items-center gap-3 p-3 rounded-lg border text-left transition-all ${
                      selectedCases.includes(uc.id)
                        ? "border-blue-500 bg-blue-50"
                        : "border-gray-200 hover:border-gray-300"
                    }`}
                  >
                    <div className={`w-9 h-9 rounded-lg flex items-center justify-center shrink-0 ${
                      selectedCases.includes(uc.id) ? "bg-blue-100 text-blue-600" : "bg-gray-100 text-gray-400"
                    }`}>
                      <uc.icon className="w-4 h-4" />
                    </div>
                    <div className="flex-1">
                      <p className="text-sm font-medium text-gray-900">{uc.label}</p>
                      <p className="text-xs text-gray-500">{uc.desc}</p>
                    </div>
                    {selectedCases.includes(uc.id) && <Check className="w-4 h-4 text-blue-600 shrink-0" />}
                  </button>
                ))}
              </div>
            </div>
          )}

          {/* Step 1: Confirm apps */}
          {step === 1 && (
            <div className="space-y-4">
              <div>
                <h2 className="text-xl font-bold text-gray-900">Apps yang direkomendasikan ✨</h2>
                <p className="text-sm text-gray-500 mt-1">Berdasarkan pilihan kamu, berikut apps yang akan diaktifkan:</p>
              </div>

              <div className="space-y-2">
                {suggestedApps.length > 0 ? suggestedApps.map((appId) => (
                  <div key={appId} className="flex items-center gap-3 p-3 bg-blue-50 border border-blue-100 rounded-lg">
                    <Check className="w-4 h-4 text-blue-600" />
                    <span className="text-sm font-medium text-gray-900 capitalize">{appId.replace(/-/g, " ").replace("ai ", "AI ")}</span>
                  </div>
                )) : (
                  <p className="text-sm text-gray-500 py-4 text-center">Pilih tujuan di step sebelumnya untuk mendapatkan rekomendasi.</p>
                )}
              </div>

              <div className="bg-gradient-to-r from-blue-50 to-indigo-50 border border-blue-100 rounded-lg p-4">
                <div className="flex items-start gap-2">
                  <Sparkles className="w-4 h-4 text-blue-600 mt-0.5" />
                  <div>
                    <p className="text-sm font-medium text-gray-900">Pro Trial Aktif — 14 Hari</p>
                    <p className="text-xs text-gray-500 mt-0.5">Semua fitur Pro tersedia gratis. Setelah trial berakhir, kamu tetap bisa menggunakan plan Starter.</p>
                  </div>
                </div>
              </div>
            </div>
          )}

          {/* Step 2: Done */}
          {step === 2 && (
            <div className="text-center py-6 space-y-4">
              <div className="w-16 h-16 bg-emerald-100 rounded-full flex items-center justify-center mx-auto">
                <Check className="w-8 h-8 text-emerald-600" />
              </div>
              <div>
                <h2 className="text-xl font-bold text-gray-900">Selamat! 🎉</h2>
                <p className="text-sm text-gray-500 mt-1">Workspace kamu sudah siap. Mulai eksplorasi apps yang sudah diaktifkan.</p>
              </div>
              {companyName && <p className="text-sm text-gray-700 font-medium">{companyName}</p>}
            </div>
          )}

          {/* Navigation */}
          <div className="flex items-center justify-between mt-6 pt-4 border-t border-gray-100">
            {step > 0 ? (
              <button onClick={() => setStep(step - 1)} className="flex items-center gap-1 text-sm text-gray-500 hover:text-gray-700">
                <ArrowLeft className="w-4 h-4" /> Kembali
              </button>
            ) : <div />}

            {step < 2 ? (
              <button
                onClick={() => setStep(step + 1)}
                disabled={step === 0 && selectedCases.length === 0}
                className="flex items-center gap-1 bg-blue-600 text-white text-sm font-medium px-5 py-2.5 rounded-lg hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed"
              >
                Lanjut <ArrowRight className="w-4 h-4" />
              </button>
            ) : (
              <button
                onClick={handleFinish}
                className="flex items-center gap-1 bg-blue-600 text-white text-sm font-medium px-5 py-2.5 rounded-lg hover:bg-blue-700"
              >
                Masuk Dashboard <ArrowRight className="w-4 h-4" />
              </button>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}
