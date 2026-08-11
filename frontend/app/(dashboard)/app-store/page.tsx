"use client";

import { useEffect } from "react";
import { useAppModuleStore } from "@/lib/app-registry";
import { usePlatformStore } from "@/lib/store";
import { Check } from "lucide-react";

export default function AppStorePage() {
  const { activeApps, activateApp, deactivateApp } = usePlatformStore();
  const { modules, fetchModules } = useAppModuleStore();

  useEffect(() => { fetchModules(); }, [fetchModules]);

  const availableApps = modules.filter((app) => !app.is_permanent);

  return (
    <div className="h-full overflow-y-auto p-4 sm:p-6 lg:p-8 max-w-6xl mx-auto space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-gray-900">App Store</h1>
        <p className="text-gray-500 text-sm mt-1">Aktifkan module yang kamu butuhkan untuk bisnis.</p>
      </div>

      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
        {availableApps.map((app) => {
          const isActive = activeApps.includes(app.key);
          return (
            <div
              key={app.key}
              className={`bg-white border rounded-xl p-5 transition-all ${
                isActive ? "border-blue-300 ring-1 ring-blue-100" : "border-gray-200"
              }`}
            >
              <div className="flex items-start justify-between">
                <div className={`w-10 h-10 ${app.color} rounded-lg flex items-center justify-center`}>
                  <app.icon className="w-5 h-5 text-white" />
                </div>
                {isActive && (
                  <span className="flex items-center gap-1 text-xs font-medium text-blue-600 bg-blue-50 px-2 py-0.5 rounded-full">
                    <Check className="w-3 h-3" /> Aktif
                  </span>
                )}
              </div>
              <h3 className="mt-3 font-semibold text-gray-900">{app.name}</h3>
              <p className="text-sm text-gray-500 mt-1 mb-4">{app.description}</p>
              <button
                onClick={() => isActive ? deactivateApp(app.key) : activateApp(app.key)}
                className={`w-full py-2 rounded-lg text-sm font-medium transition-colors ${
                  isActive
                    ? "bg-gray-100 text-gray-600 hover:bg-red-50 hover:text-red-600"
                    : "bg-blue-600 text-white hover:bg-blue-700"
                }`}
              >
                {isActive ? "Deactivate" : "Activate"}
              </button>
            </div>
          );
        })}
      </div>
    </div>
  );
}
