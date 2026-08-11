import { Button } from "@/components/ui/button";
import Link from "next/link";
import { ArrowRight } from "lucide-react";

export function Hero() {
  return (
    <section className="pt-36 pb-20 bg-gradient-to-b from-white to-gray-50">
      <div className="max-w-[1200px] mx-auto px-6 grid grid-cols-1 lg:grid-cols-2 gap-16 items-center">
        {/* Left - Text */}
        <div className="animate-fade-up">
          <h1 className="text-4xl lg:text-5xl font-bold text-gray-900 leading-tight tracking-tight">
            Platform{" "}
            <span className="text-blue-600">AI Agents</span>{" "}
            untuk Bisnis Kamu.
          </h1>
          <p className="mt-6 text-lg text-gray-600 max-w-md leading-relaxed">
            Customer service, sales, support, hingga monitoring produksi — semua bisa diotomasi dengan AI agents. Untuk korporasi maupun UMKM.
          </p>
          <div className="flex flex-wrap gap-3 mt-8">
            <Link href="/register">
              <Button className="bg-blue-600 hover:bg-blue-700 text-white font-medium px-6 h-11 text-sm">
                Start Building
                <ArrowRight className="ml-2 h-4 w-4" />
              </Button>
            </Link>
            <Button variant="outline" className="border-gray-300 text-gray-700 hover:bg-gray-50 font-medium px-6 h-11 text-sm">
              Lihat Dokumentasi
            </Button>
          </div>
        </div>

        {/* Right - Laptop & Phone Illustration */}
        <div className="relative h-[450px] flex items-center justify-center [perspective:1200px]">
          {/* Laptop */}
          <div className="animate-float">
            <div className="w-[420px] h-[270px] bg-white rounded-xl border border-gray-200 shadow-xl relative overflow-hidden">
              {/* Screen content */}
              <div className="p-4 h-full flex flex-col">
                {/* Chat header */}
                <div className="flex items-center gap-3 pb-3 border-b border-gray-100">
                  <div className="w-8 h-8 rounded-full bg-blue-50 text-blue-600 flex items-center justify-center text-xs font-semibold">CS</div>
                  <div>
                    <div className="text-sm font-semibold text-gray-900">Support Agent</div>
                    <div className="text-xs text-gray-400">Active • GPT-4</div>
                  </div>
                </div>

                {/* Chat messages */}
                <div className="flex-1 flex flex-col justify-end gap-2 pt-3">
                  <div className="self-start bg-gray-100 text-gray-800 text-xs px-3 py-2 rounded-lg rounded-bl-sm max-w-[75%] animate-fade-up delay-100">
                    Bagaimana cara refund tiket saya?
                  </div>
                  <div className="self-end bg-blue-600 text-white text-xs px-3 py-2 rounded-lg rounded-br-sm max-w-[75%] animate-fade-up delay-300">
                    Saya bantu proses refund. Mohon konfirmasi nomor pesanan Anda.
                  </div>
                </div>

                {/* Trace steps (LangSmith style) */}
                <div className="mt-3 pt-3 border-t border-gray-100 space-y-1.5">
                  <div className="flex items-center gap-2 text-xs">
                    <div className="w-2 h-2 rounded-full bg-blue-600" />
                    <span className="font-mono text-blue-600 font-medium">Intent: Refund Request</span>
                    <span className="ml-auto text-gray-400">120ms</span>
                  </div>
                  <div className="flex items-center gap-2 text-xs">
                    <div className="w-2 h-2 rounded-full bg-blue-600" />
                    <span className="font-mono text-blue-600 font-medium">Tool: Search Orders</span>
                    <span className="ml-auto text-gray-400">340ms</span>
                  </div>
                  <div className="flex items-center gap-2 text-xs">
                    <div className="w-2 h-2 rounded-full bg-gray-300 animate-pulse-dot" />
                    <span className="font-mono text-gray-400">Action: Process Refund</span>
                  </div>
                </div>
              </div>
            </div>
            {/* Laptop base */}
            <div className="w-[470px] h-4 bg-gray-100 border border-gray-200 rounded-b-xl mx-auto -mt-px shadow-sm" />
          </div>

          {/* Phone */}
          <div className="absolute right-0 top-12 animate-float-phone">
            <div className="w-[140px] h-[280px] bg-white rounded-[28px] border-[5px] border-gray-800 shadow-xl relative overflow-hidden">
              {/* Notch */}
              <div className="absolute top-0 left-1/2 -translate-x-1/2 w-14 h-4 bg-gray-800 rounded-b-xl z-10" />
              {/* Screen */}
              <div className="h-full pt-6 pb-3 px-2 flex flex-col justify-end gap-1.5">
                <div className="bg-gray-100 text-gray-800 text-[10px] px-2.5 py-1.5 rounded-xl rounded-bl-sm self-start max-w-[85%]">
                  Halo! Ada yang bisa dibantu?
                </div>
                <div className="bg-blue-600 text-white text-[10px] px-2.5 py-1.5 rounded-xl rounded-br-sm self-end max-w-[85%]">
                  Refund tiket #1234
                </div>
                <div className="bg-gray-100 text-gray-800 text-[10px] px-2.5 py-1.5 rounded-xl rounded-bl-sm self-start max-w-[85%]">
                  Sedang memproses...
                </div>
                <div className="bg-gray-100 text-gray-800 text-[10px] px-2.5 py-1.5 rounded-xl rounded-bl-sm self-start max-w-[85%] flex items-center gap-1">
                  <span className="text-green-600">✓</span> Berhasil di-refund
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}
