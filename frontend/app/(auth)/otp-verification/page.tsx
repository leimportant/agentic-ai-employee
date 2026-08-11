"use client";

import { useState, useEffect, Suspense } from "react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { useRouter, useSearchParams } from "next/navigation";
import { ArrowRight, Mail, Send, MessageSquare, CheckCircle2 } from "lucide-react";

const channels = [
  { id: "email", label: "Email", icon: Mail, description: "Kode dikirim ke email" },
  { id: "telegram", label: "Telegram", icon: Send, description: "Kode dikirim ke Telegram" },
  { id: "whatsapp", label: "WhatsApp", icon: MessageSquare, description: "Kode dikirim ke WhatsApp" },
];

function OtpContent() {
  const router = useRouter();
  const searchParams = useSearchParams();
  const email = searchParams.get("email") || "";

  const [otp, setOtp] = useState("");
  const [channel, setChannel] = useState("email");
  const [destination, setDestination] = useState("");
  const [error, setError] = useState("");
  const [success, setSuccess] = useState("");
  const [submitting, setSubmitting] = useState(false);
  const [resendCooldown, setResendCooldown] = useState(60);

  useEffect(() => {
    if (resendCooldown <= 0) return;
    const t = setTimeout(() => setResendCooldown((c) => c - 1), 1000);
    return () => clearTimeout(t);
  }, [resendCooldown]);

  const handleResend = async () => {
    setError("");
    setSuccess("");
    try {
      const body: Record<string, string> = { email, channel };
      if (channel !== "email" && destination) {
        body.destination = destination;
      }
      await fetch("/api/v1/auth/otp/send", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(body),
      });
      setResendCooldown(60);
      setSuccess(`OTP dikirim ulang via ${channel}`);
    } catch {
      setError("Gagal mengirim ulang OTP");
    }
  };

  const handleVerify = async (e: React.FormEvent) => {
    e.preventDefault();
    setSubmitting(true);
    setError("");
    try {
      const resp = await fetch("/api/v1/auth/otp/verify", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email, code: otp }),
      });
      const data = await resp.json();
      if (resp.ok && data.access_token) {
        localStorage.setItem("token", data.access_token);
        // New user → onboarding, existing → home
        router.push(data.is_new_user ? "/onboarding" : "/home");
      } else {
        setError(data.detail || "OTP tidak valid");
      }
    } catch {
      setError("Terjadi kesalahan, coba lagi");
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <div className="space-y-6">
      <div className="space-y-2">
        <h2 className="text-2xl font-bold text-gray-900">Verifikasi OTP</h2>
        <p className="text-gray-500 text-sm">
          Masukkan kode 6 digit yang dikirim ke <span className="font-medium text-gray-700">{email}</span>
        </p>
      </div>

      {/* Channel selector */}
      <div>
        <label className="text-xs text-gray-500 mb-2 block">Kirim kode via:</label>
        <div className="grid grid-cols-3 gap-2">
          {channels.map((ch) => (
            <button
              key={ch.id}
              type="button"
              onClick={() => { setChannel(ch.id); setSuccess(""); }}
              className={`flex flex-col items-center gap-1 p-3 rounded-lg border text-xs font-medium transition-all ${
                channel === ch.id
                  ? "border-blue-500 bg-blue-50 text-blue-700"
                  : "border-gray-200 text-gray-500 hover:border-gray-300"
              }`}
            >
              <ch.icon className="w-4 h-4" />
              {ch.label}
            </button>
          ))}
        </div>
      </div>

      {/* Destination for telegram/whatsapp */}
      {channel !== "email" && (
        <div>
          <label className="text-xs text-gray-500 mb-1.5 block">
            {channel === "telegram" ? "Telegram Chat ID" : "Nomor WhatsApp"}
          </label>
          <Input
            type="text"
            value={destination}
            onChange={(e) => setDestination(e.target.value)}
            placeholder={channel === "telegram" ? "123456789" : "628123456789"}
            className="h-11 bg-white border-gray-300 text-gray-900 placeholder:text-gray-400 focus:border-blue-600"
          />
          <p className="text-[11px] text-gray-400 mt-1">
            {channel === "telegram" ? "Kirim /start ke bot kami untuk mendapatkan Chat ID" : "Format: 628xxx (tanpa +)"}
          </p>
        </div>
      )}

      {/* OTP Input */}
      <form onSubmit={handleVerify} className="space-y-4">
        <div>
          <label className="text-xs text-gray-500 mb-1.5 block">Kode OTP</label>
          <Input
            type="text"
            value={otp}
            onChange={(e) => setOtp(e.target.value.replace(/\D/g, "").slice(0, 6))}
            placeholder="000000"
            className="h-12 bg-white border-gray-300 text-gray-900 text-center text-lg tracking-[0.5em] font-mono placeholder:text-gray-300 focus:border-blue-600"
            maxLength={6}
            required
          />
        </div>

        {error && <p className="text-red-600 text-sm">{error}</p>}
        {success && (
          <p className="text-emerald-600 text-sm flex items-center gap-1">
            <CheckCircle2 className="w-3.5 h-3.5" /> {success}
          </p>
        )}

        <Button type="submit" className="w-full h-11 bg-blue-600 hover:bg-blue-700 text-white font-medium" disabled={submitting || otp.length < 6}>
          {submitting ? "Memverifikasi..." : "Verifikasi"}
          {!submitting && <ArrowRight className="ml-2 h-4 w-4" />}
        </Button>
      </form>

      {/* Resend */}
      <div className="text-center">
        {resendCooldown > 0 ? (
          <p className="text-gray-400 text-sm">Kirim ulang dalam {resendCooldown}s</p>
        ) : (
          <button onClick={handleResend} className="text-blue-600 hover:text-blue-700 text-sm font-medium">
            Kirim ulang OTP via {channels.find((c) => c.id === channel)?.label}
          </button>
        )}
      </div>
    </div>
  );
}

export default function OtpVerificationPage() {
  return (
    <Suspense fallback={<div className="p-8 text-gray-400">Loading...</div>}>
      <OtpContent />
    </Suspense>
  );
}
