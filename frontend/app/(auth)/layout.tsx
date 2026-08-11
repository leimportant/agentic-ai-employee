import { Zap } from "lucide-react";

export default function AuthLayout({ children }: { children: React.ReactNode }) {
  return (
    <div className="min-h-screen bg-white flex">
      {/* Left Panel - Branding */}
      <div className="hidden lg:flex lg:w-1/2 relative overflow-hidden bg-gradient-to-br from-blue-600 to-blue-800 p-12 flex-col justify-between">
        {/* Grid pattern */}
        <div className="absolute inset-0 opacity-10" style={{
          backgroundImage: `linear-gradient(rgba(255,255,255,0.2) 1px, transparent 1px), linear-gradient(90deg, rgba(255,255,255,0.2) 1px, transparent 1px)`,
          backgroundSize: '60px 60px'
        }} />

        {/* Floating orbs */}
        <div className="absolute top-20 left-20 w-72 h-72 bg-white/10 rounded-full blur-3xl animate-float" />
        <div className="absolute bottom-20 right-20 w-96 h-96 bg-blue-400/20 rounded-full blur-3xl animate-float-phone" />

        {/* Logo */}
        <div className="relative z-10">
          <div className="flex items-center gap-2">
            <div className="p-2 rounded-lg bg-white/20 border border-white/30">
              <Zap className="h-5 w-5 text-white" />
            </div>
            <span className="text-white text-lg font-semibold">Agentic AI</span>
          </div>
        </div>

        {/* Center illustration */}
        <div className="relative z-10 flex-1 flex items-center justify-center">
          <svg viewBox="0 0 400 300" className="w-full max-w-sm opacity-90" fill="none">
            <circle cx="200" cy="150" r="40" className="fill-white/10 stroke-white/50" strokeWidth="1.5" />
            <circle cx="200" cy="150" r="28" className="fill-white/5 stroke-white/30" strokeWidth="1" />
            <circle cx="200" cy="150" r="4" className="fill-white" />
            <circle cx="200" cy="50" r="24" className="fill-white/10 stroke-white/40" strokeWidth="1" />
            <path d="M192 46 L208 46 M192 50 L204 50 M192 54 L200 54" className="stroke-white/70" strokeWidth="1.2" strokeLinecap="round" />
            <line x1="200" y1="74" x2="200" y2="110" className="stroke-white/30" strokeWidth="1" strokeDasharray="4 3" />
            <circle cx="320" cy="150" r="24" className="fill-white/10 stroke-white/40" strokeWidth="1" />
            <path d="M312 158 L316 152 L320 156 L324 144 L328 148" className="stroke-white/70" strokeWidth="1.2" strokeLinecap="round" />
            <line x1="240" y1="150" x2="296" y2="150" className="stroke-white/30" strokeWidth="1" strokeDasharray="4 3" />
            <circle cx="200" cy="250" r="24" className="fill-white/10 stroke-white/40" strokeWidth="1" />
            <circle cx="200" cy="244" r="4" className="fill-white/60" />
            <path d="M192 254 Q200 258 208 254" className="stroke-white/70" strokeWidth="1.2" strokeLinecap="round" />
            <line x1="200" y1="190" x2="200" y2="226" className="stroke-white/30" strokeWidth="1" strokeDasharray="4 3" />
            <circle cx="80" cy="150" r="24" className="fill-white/10 stroke-white/40" strokeWidth="1" />
            <rect x="72" y="142" width="16" height="16" rx="3" className="stroke-white/70 fill-none" strokeWidth="1.2" />
            <line x1="104" y1="150" x2="160" y2="150" className="stroke-white/30" strokeWidth="1" strokeDasharray="4 3" />
          </svg>
        </div>

        {/* Bottom text */}
        <div className="relative z-10 space-y-3">
          <h1 className="text-3xl font-bold text-white">
            Karyawan AI untuk<br />Bisnis Kamu
          </h1>
          <p className="text-blue-100 text-sm leading-relaxed max-w-sm">
            Otomasi customer service &amp; sales 24/7 dengan AI agents. Setup 5 menit, langsung jalan.
          </p>
          <div className="flex items-center gap-3 pt-2">
            <div className="flex -space-x-2">
              {[1,2,3,4].map(i => (
                <div key={i} className="w-7 h-7 rounded-full bg-white/20 border-2 border-blue-700 flex items-center justify-center text-xs text-white">
                  {String.fromCharCode(64 + i)}
                </div>
              ))}
            </div>
            <span className="text-blue-200 text-xs">500+ UMKM Indonesia</span>
          </div>
        </div>
      </div>

      {/* Right Panel - Form */}
      <div className="w-full lg:w-1/2 flex items-center justify-center p-6 bg-white">
        <div className="w-full max-w-sm">
          {children}
        </div>
      </div>
    </div>
  );
}
