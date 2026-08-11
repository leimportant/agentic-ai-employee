"use client";

import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import Link from "next/link";
import { useState } from "react";
import { useRouter } from "next/navigation";
import { Chrome, ArrowRight } from "lucide-react";

export default function LoginPage() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const router = useRouter();

  return (
    <div className="space-y-6">
      <div className="space-y-2">
        <h2 className="text-2xl font-bold text-gray-900">Masuk ke akun kamu</h2>
        <p className="text-gray-500 text-sm">Kelola AI agents dan pantau performa bisnis</p>
      </div>

      <Button
        variant="outline"
        className="w-full h-11 bg-gray-900 border-gray-900 text-white hover:bg-gray-800"
        onClick={() => router.push("/dashboard")}
      >
        <Chrome className="mr-2 h-4 w-4 text-white" />
        Lanjutkan dengan Google
      </Button>

      <div className="relative">
        <div className="absolute inset-0 flex items-center">
          <span className="w-full border-t border-gray-200" />
        </div>
        <div className="relative flex justify-center text-xs">
          <span className="bg-white px-3 text-gray-400">atau pakai email</span>
        </div>
      </div>

      <div className="space-y-3">
        <div>
          <label className="text-xs text-gray-500 mb-1.5 block">Email</label>
          <Input
            type="email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            placeholder="nama@perusahaan.com"
            className="h-11 bg-white border-gray-300 text-gray-900 placeholder:text-gray-400 focus:border-blue-600 focus:ring-blue-600/20"
          />
        </div>
        <div>
          <div className="flex justify-between items-center mb-1.5">
            <label className="text-xs text-gray-500">Password</label>
            <Link href="/forgot-password" className="text-xs text-blue-600 hover:text-blue-700">
              Lupa password?
            </Link>
          </div>
          <Input
            type="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            placeholder="••••••••"
            className="h-11 bg-white border-gray-300 text-gray-900 placeholder:text-gray-400 focus:border-blue-600 focus:ring-blue-600/20"
          />
        </div>
      </div>

      <Button className="w-full h-11 bg-blue-600 hover:bg-blue-700 text-white font-medium">
        Masuk
        <ArrowRight className="ml-2 h-4 w-4" />
      </Button>

      <p className="text-gray-500 text-center text-sm">
        Belum punya akun?{" "}
        <Link href="/register" className="text-blue-600 hover:text-blue-700 font-medium">
          Daftar gratis
        </Link>
      </p>
    </div>
  );
}
