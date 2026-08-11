"use client";

import Link from "next/link";
import { useEffect } from "react";
import { ArrowUpRight } from "lucide-react";
import { useAppModuleStore } from "@/lib/app-registry";
import { usePlatformStore } from "@/lib/store";
import { useAuthStore } from "@/lib/stores/useAuthStore";

export default function HomePage() {
  const { activeApps } = usePlatformStore();
  const { user } = useAuthStore();
  const { modules, fetchModules } = useAppModuleStore();

  useEffect(() => { fetchModules(); }, [fetchModules]);

  const userApps = modules.filter(
    (app) => !app.is_permanent && activeApps.includes(app.key)
  );

  const greeting = user?.name ? `Selamat datang, ${user.name} 👋` : "Selamat datang 👋";

  return (
    <div className="h-full overflow-y-auto p-4 sm:p-6 lg:p-8 max-w-6xl mx-auto space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-gray-900">{greeting}</h1>
        <p className="text-gray-500 text-sm mt-1">Pilih app untuk mulai bekerja.</p>
      </div>

      {userApps.length > 0 ? (
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
          {userApps.map((app) => (
            <Link key={app.id} href={app.href} className="group bg-white border border-gray-200 rounded-xl p-5 hover:border-blue-300 hover:shadow-md transition-all">
              <div className="flex items-start justify-between">
                <div className={`w-10 h-10 ${app.color} rounded-lg flex items-center justify-center`}>
                  <app.icon className="w-5 h-5 text-white" />
                </div>
                <ArrowUpRight className="w-4 h-4 text-gray-300 group-hover:text-blue-500 transition-colors" />
              </div>
              <h3 className="mt-3 font-semibold text-gray-900">{app.name}</h3>
              <p className="text-sm text-gray-500 mt-1">{app.description}</p>
            </Link>
          ))}

          <Link href="/app-store" className="border-2 border-dashed border-gray-200 rounded-xl p-5 flex flex-col items-center justify-center text-center hover:border-blue-300 hover:bg-blue-50/50 transition-all min-h-[140px]">
            <div className="w-10 h-10 bg-gray-100 rounded-lg flex items-center justify-center text-gray-400 mb-2">
              <span className="text-xl">+</span>
            </div>
            <p className="text-sm font-medium text-gray-500">Tambah App</p>
          </Link>
        </div>
      ) : (
        <div className="text-center py-16 bg-white rounded-xl border border-gray-200">
          <p className="text-gray-500 mb-4">Belum ada app yang aktif.</p>
          <Link href="/app-store" className="inline-flex items-center gap-2 bg-blue-600 text-white text-sm font-medium px-4 py-2 rounded-lg hover:bg-blue-700">
            Buka App Store
          </Link>
        </div>
      )}
    </div>
  );
}
