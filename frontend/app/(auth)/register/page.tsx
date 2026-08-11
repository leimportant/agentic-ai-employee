"use client";

import { useState } from "react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import Link from "next/link";
import { useRouter } from "next/navigation";
import { Chrome, ArrowRight } from "lucide-react";

export default function RegisterPage() {
  const router = useRouter();
  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState("");

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (password !== confirmPassword) {
      setError("Password tidak cocok");
      return;
    }
    setSubmitting(true);
    setError("");
    try {
      const response = await fetch("/api/v1/auth/register", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ name, email, password }),
      });
      const result = await response.json();
      if (result.success) {
        // Send OTP to email by default
        await fetch("/api/v1/auth/otp/send", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ email, channel: "email" }),
        });
        // Redirect to OTP verification with email param
        router.push(`/otp-verification?email=${encodeURIComponent(email)}`);
      } else {
        setError(result.detail || "Gagal mendaftar");
      }
    } catch {
      setError("Terjadi kesalahan, coba lagi");
    } finally {
      setSubmitting(false);
    }
  };

  const handleGoogle = async () => {
    try {
      const resp = await fetch("/api/v1/auth/google/login");
      const data = await resp.json();
      window.location.href = data.redirect_url;
    } catch {
      setError("Gagal menghubungi Google");
    }
  };

  return (
    <div className="space-y-6">
      <div className="space-y-2">
        <h2 className="text-2xl font-bold text-gray-900">Buat akun baru</h2>
        <p className="text-gray-500 text-sm">Mulai gratis 14 hari Pro trial, tanpa kartu kredit</p>
      </div>

      <Button
        variant="outline"
        className="w-full h-11 bg-gray-900 border-gray-900 text-white hover:bg-gray-800"
        onClick={handleGoogle}
      >
        <Chrome className="mr-2 h-4 w-4 text-white" />
        Daftar dengan Google
      </Button>

      <div className="relative">
        <div className="absolute inset-0 flex items-center">
          <span className="w-full border-t border-gray-200" />
        </div>
        <div className="relative flex justify-center text-xs">
          <span className="bg-white px-3 text-gray-400">atau pakai email</span>
        </div>
      </div>

      <form onSubmit={handleSubmit} className="space-y-3">
        <div>
          <label className="text-xs text-gray-500 mb-1.5 block">Nama lengkap</label>
          <Input type="text" value={name} onChange={(e) => setName(e.target.value)} placeholder="John Doe" className="h-11 bg-white border-gray-300 text-gray-900 placeholder:text-gray-400 focus:border-blue-600 focus:ring-blue-600/20" required />
        </div>
        <div>
          <label className="text-xs text-gray-500 mb-1.5 block">Email</label>
          <Input type="email" value={email} onChange={(e) => setEmail(e.target.value)} placeholder="nama@perusahaan.com" className="h-11 bg-white border-gray-300 text-gray-900 placeholder:text-gray-400 focus:border-blue-600 focus:ring-blue-600/20" required />
        </div>
        <div>
          <label className="text-xs text-gray-500 mb-1.5 block">Password</label>
          <Input type="password" value={password} onChange={(e) => setPassword(e.target.value)} placeholder="Minimal 8 karakter" className="h-11 bg-white border-gray-300 text-gray-900 placeholder:text-gray-400 focus:border-blue-600 focus:ring-blue-600/20" required minLength={8} />
        </div>
        <div>
          <label className="text-xs text-gray-500 mb-1.5 block">Konfirmasi password</label>
          <Input type="password" value={confirmPassword} onChange={(e) => setConfirmPassword(e.target.value)} placeholder="Ulangi password" className="h-11 bg-white border-gray-300 text-gray-900 placeholder:text-gray-400 focus:border-blue-600 focus:ring-blue-600/20" required minLength={8} />
        </div>
        {error && <p className="text-red-600 text-sm">{error}</p>}
        <Button type="submit" className="w-full h-11 bg-blue-600 hover:bg-blue-700 text-white font-medium" disabled={submitting}>
          {submitting ? "Memproses..." : "Buat Akun"}
          {!submitting && <ArrowRight className="ml-2 h-4 w-4" />}
        </Button>
      </form>

      <p className="text-gray-500 text-center text-sm">
        Sudah punya akun? <Link href="/login" className="text-blue-600 hover:text-blue-700 font-medium">Masuk</Link>
      </p>
    </div>
  );
}
