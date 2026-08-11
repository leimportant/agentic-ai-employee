import { Navbar } from "@/components/landing/Navbar";
import { Hero } from "@/components/landing/Hero";
import { Features } from "@/components/landing/Features";
import { Pricing } from "@/components/landing/Pricing";
import { ArrowRight } from "lucide-react";
import Link from "next/link";

export default function LandingPage() {
  return (
    <div className="landing bg-white min-h-screen text-gray-900">
      <Navbar />
      <Hero />
      <Features />
      <Pricing />
      <CTASection />
      <Footer />
    </div>
  );
}

function CTASection() {
  return (
    <section className="py-20 bg-white">
      <div className="max-w-[1200px] mx-auto px-6 text-center">
        <h2 className="text-3xl font-bold text-gray-900 tracking-tight">
          Siap tingkatkan bisnis kamu?
        </h2>
        <p className="mt-3 text-gray-500 text-lg max-w-md mx-auto">
          Mulai gratis hari ini. Tidak perlu kartu kredit.
        </p>
        <Link
          href="/register"
          className="inline-flex items-center gap-2 mt-8 bg-blue-600 hover:bg-blue-700 text-white font-medium px-6 py-3 rounded-lg text-sm transition-colors"
        >
          Mulai Gratis Sekarang
          <ArrowRight className="w-4 h-4" />
        </Link>
      </div>
    </section>
  );
}

function Footer() {
  return (
    <footer className="border-t border-gray-200 bg-gray-50 py-10">
      <div className="max-w-[1200px] mx-auto px-6 flex flex-col md:flex-row justify-between items-center gap-4">
        <p className="text-gray-500 text-sm">
          © 2026 Agentic AI Employee Platform. All rights reserved.
        </p>
        <div className="flex gap-6 text-sm text-gray-500">
          <Link href="#" className="hover:text-gray-900">Privacy</Link>
          <Link href="#" className="hover:text-gray-900">Terms</Link>
          <Link href="#" className="hover:text-gray-900">Contact</Link>
        </div>
      </div>
    </footer>
  );
}
