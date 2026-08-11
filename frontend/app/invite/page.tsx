"use client";

import { useEffect, useState, Suspense } from "react";
import { useSearchParams, useRouter } from "next/navigation";
import { CheckCircle, XCircle } from "lucide-react";
import { api } from "@/lib/api";

function AcceptContent() {
  const searchParams = useSearchParams();
  const router = useRouter();
  const token = searchParams.get("token");
  const [status, setStatus] = useState<"loading" | "success" | "error">("loading");
  const [message, setMessage] = useState("");

  useEffect(() => {
    if (!token) { setStatus("error"); setMessage("Token tidak valid"); return; }
    api.post(`/team/invite/accept?token=${token}`)
      .then(() => { setStatus("success"); setMessage("Undangan diterima! Silakan login."); })
      .catch((e) => { setStatus("error"); setMessage(e.response?.data?.detail || "Gagal menerima undangan"); });
  }, [token]);

  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-50 p-4">
      <div className="bg-white rounded-xl border border-gray-200 p-8 max-w-sm w-full text-center">
        {status === "loading" && <p className="text-gray-500">Memproses undangan...</p>}
        {status === "success" && (
          <>
            <CheckCircle className="w-16 h-16 text-emerald-500 mx-auto mb-4" />
            <h2 className="text-lg font-bold text-gray-900 mb-2">Berhasil!</h2>
            <p className="text-sm text-gray-500 mb-6">{message}</p>
            <button onClick={() => router.push("/login")} className="px-6 py-2.5 bg-blue-600 text-white text-sm font-medium rounded-lg hover:bg-blue-700">
              Login
            </button>
          </>
        )}
        {status === "error" && (
          <>
            <XCircle className="w-16 h-16 text-red-400 mx-auto mb-4" />
            <h2 className="text-lg font-bold text-gray-900 mb-2">Gagal</h2>
            <p className="text-sm text-gray-500">{message}</p>
          </>
        )}
      </div>
    </div>
  );
}

export default function AcceptInvitePage() {
  return (
    <Suspense fallback={<div className="min-h-screen flex items-center justify-center"><p className="text-gray-400">Loading...</p></div>}>
      <AcceptContent />
    </Suspense>
  );
}
