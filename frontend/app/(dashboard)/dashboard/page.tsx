"use client";

import { Bot, MessageSquare, Users, TrendingUp, ArrowUpRight, Zap, CreditCard, Clock } from "lucide-react";
import Link from "next/link";

const stats = [
  { label: "Total Chat", value: "1,234", change: "+12%", icon: MessageSquare, color: "blue" },
  { label: "Active Agents", value: "3", change: "+1", icon: Bot, color: "violet" },
  { label: "Customers", value: "89", change: "+8%", icon: Users, color: "emerald" },
  { label: "Revenue", value: "Rp 2.4jt", change: "+23%", icon: TrendingUp, color: "amber" },
];

const recentActivity = [
  { agent: "CS Agent", message: "Menyelesaikan 12 tiket baru", time: "2 menit lalu" },
  { agent: "Sales Agent", message: "Follow-up 5 lead baru", time: "15 menit lalu" },
  { agent: "Support Agent", message: "Eskalasi 1 tiket ke tim", time: "1 jam lalu" },
  { agent: "CS Agent", message: "Menjawab 28 FAQ otomatis", time: "3 jam lalu" },
];

const quickActions = [
  { label: "Buat Agent Baru", href: "/ai-agents", icon: Bot },
  { label: "Lihat Customers", href: "/customers", icon: Users },
  { label: "Upgrade Plan", href: "/billing", icon: CreditCard },
];

export default function DashboardPage() {
  return (
    <div className="space-y-6">
      {/* Greeting */}
      <div>
        <h1 className="text-2xl font-bold text-gray-900">Selamat datang, John Doe 👋</h1>
        <p className="text-gray-500 text-sm mt-1">Berikut ringkasan performa AI agents kamu hari ini.</p>
      </div>

      {/* Stats Grid */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        {stats.map((stat) => (
          <div key={stat.label} className="bg-white rounded-xl border border-gray-200 p-5 hover:shadow-md transition-shadow">
            <div className="flex items-center justify-between mb-3">
              <div className={`w-9 h-9 rounded-lg flex items-center justify-center ${
                stat.color === "blue" ? "bg-blue-50 text-blue-600" :
                stat.color === "violet" ? "bg-violet-50 text-violet-600" :
                stat.color === "emerald" ? "bg-emerald-50 text-emerald-600" :
                "bg-amber-50 text-amber-600"
              }`}>
                <stat.icon className="w-4 h-4" />
              </div>
              <span className="text-xs font-medium text-emerald-600 bg-emerald-50 px-2 py-0.5 rounded-full">
                {stat.change}
              </span>
            </div>
            <p className="text-2xl font-bold text-gray-900">{stat.value}</p>
            <p className="text-sm text-gray-500 mt-0.5">{stat.label}</p>
          </div>
        ))}
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Recent Activity */}
        <div className="lg:col-span-2 bg-white rounded-xl border border-gray-200 p-6">
          <div className="flex items-center justify-between mb-4">
            <h2 className="font-semibold text-gray-900">Aktivitas Terbaru</h2>
            <Link href="/ai-agents" className="text-sm text-blue-600 hover:text-blue-700 flex items-center gap-1">
              Lihat semua <ArrowUpRight className="w-3 h-3" />
            </Link>
          </div>
          <div className="space-y-4">
            {recentActivity.map((item, i) => (
              <div key={i} className="flex items-start gap-3">
                <div className="w-8 h-8 rounded-full bg-blue-50 text-blue-600 flex items-center justify-center shrink-0 mt-0.5">
                  <Bot className="w-4 h-4" />
                </div>
                <div className="flex-1 min-w-0">
                  <p className="text-sm text-gray-900 font-medium">{item.agent}</p>
                  <p className="text-sm text-gray-500">{item.message}</p>
                </div>
                <span className="text-xs text-gray-400 shrink-0 flex items-center gap-1">
                  <Clock className="w-3 h-3" />
                  {item.time}
                </span>
              </div>
            ))}
          </div>
        </div>

        {/* Quick Actions + Plan */}
        <div className="space-y-4">
          {/* Quick Actions */}
          <div className="bg-white rounded-xl border border-gray-200 p-5">
            <h2 className="font-semibold text-gray-900 mb-3">Aksi Cepat</h2>
            <div className="space-y-2">
              {quickActions.map((action) => (
                <Link
                  key={action.label}
                  href={action.href}
                  className="flex items-center gap-3 px-3 py-2.5 rounded-lg text-sm text-gray-700 hover:bg-gray-50 border border-gray-100 transition-colors"
                >
                  <action.icon className="w-4 h-4 text-gray-400" />
                  {action.label}
                  <ArrowUpRight className="w-3 h-3 ml-auto text-gray-300" />
                </Link>
              ))}
            </div>
          </div>

          {/* Current Plan */}
          <div className="bg-gradient-to-br from-blue-600 to-blue-700 rounded-xl p-5 text-white">
            <div className="flex items-center gap-2 mb-3">
              <Zap className="w-4 h-4" />
              <span className="text-sm font-medium">Plan Starter</span>
            </div>
            <div className="space-y-2 text-sm text-blue-100">
              <div className="flex justify-between">
                <span>Pesan terpakai</span>
                <span className="text-white font-medium">3,240 / 5,000</span>
              </div>
              <div className="w-full h-2 bg-blue-800 rounded-full overflow-hidden">
                <div className="h-full bg-white/80 rounded-full" style={{ width: "65%" }} />
              </div>
              <div className="flex justify-between">
                <span>Agents aktif</span>
                <span className="text-white font-medium">3 / 3</span>
              </div>
            </div>
            <Link
              href="/billing"
              className="mt-4 block text-center text-sm bg-white/20 hover:bg-white/30 rounded-lg py-2 transition-colors"
            >
              Upgrade ke Pro
            </Link>
          </div>
        </div>
      </div>
    </div>
  );
}
