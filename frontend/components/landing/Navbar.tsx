"use client";

import { Button } from "@/components/ui/button";
import Link from "next/link";
import { Zap, Menu, X } from "lucide-react";
import { useState } from "react";

export function Navbar() {
  const [open, setOpen] = useState(false);

  return (
    <header className="fixed top-0 w-full z-50 bg-white/95 backdrop-blur-md border-b border-gray-200">
      <nav className="max-w-[1200px] mx-auto px-6 h-16 flex items-center justify-between">
        <Link href="/" className="flex items-center gap-2">
          <div className="w-7 h-7 bg-blue-600 rounded-md flex items-center justify-center">
            <Zap className="w-4 h-4 text-white" />
          </div>
          <span className="font-bold text-gray-900">Agentic AI</span>
        </Link>

        {/* Desktop nav */}
        <div className="hidden md:flex items-center gap-8">
          <Link href="#features" className="text-sm font-medium text-gray-600 hover:text-blue-600 transition-colors">
            Fitur
          </Link>
          <Link href="#pricing" className="text-sm font-medium text-gray-600 hover:text-blue-600 transition-colors">
            Harga
          </Link>
          <Link href="#" className="text-sm font-medium text-gray-600 hover:text-blue-600 transition-colors">
            Docs
          </Link>
        </div>

        <div className="hidden md:flex items-center gap-3">
          <Link href="/login">
            <Button variant="ghost" className="text-gray-700 hover:text-gray-900 hover:bg-gray-100 text-sm font-medium">
              Log in
            </Button>
          </Link>
          <Link href="/register">
            <Button className="bg-blue-600 hover:bg-blue-700 text-white text-sm font-medium px-4">
              Mulai Gratis
            </Button>
          </Link>
        </div>

        {/* Mobile toggle */}
        <button className="md:hidden text-gray-700" onClick={() => setOpen(!open)}>
          {open ? <X className="w-5 h-5" /> : <Menu className="w-5 h-5" />}
        </button>
      </nav>

      {/* Mobile menu */}
      {open && (
        <div className="md:hidden bg-white border-t border-gray-200 px-6 py-4 space-y-3">
          <Link href="#features" className="block text-sm text-gray-600">Fitur</Link>
          <Link href="#pricing" className="block text-sm text-gray-600">Harga</Link>
          <Link href="/login" className="block text-sm text-gray-600">Log in</Link>
          <Link href="/register">
            <Button className="w-full bg-blue-600 text-white text-sm mt-2">Mulai Gratis</Button>
          </Link>
        </div>
      )}
    </header>
  );
}
