"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import { usePathname } from "next/navigation";
import {
  BarChart3, Bot, MessageSquare, Settings, HelpCircle,
} from "lucide-react";
import type { LucideIcon } from "lucide-react";
import { api } from "@/lib/api";
import { useUserAccessStore } from "@/lib/stores/useUserAccessStore";

const ICON_MAP: Record<string, LucideIcon> = {
  BarChart3, Bot, MessageSquare, Settings,
};

interface MenuItem {
  id: string;
  key: string;
  label: string;
  icon: string | null;
  href: string;
}

export default function AiCsLayout({ children }: { children: React.ReactNode }) {
  const pathname = usePathname();
  const { hasSubMenuAccess } = useUserAccessStore();
  const [menus, setMenus] = useState<MenuItem[]>([]);

  useEffect(() => {
    api.get("/menus/ai-cs").then((r) => setMenus(r.data)).catch(() => {});
  }, []);

  const visibleMenus = menus.filter(
    (m) => m.key === "dashboard" || m.key === "settings" || hasSubMenuAccess("ai-cs", m.key)
  );

  return (
    <div className="flex h-full">
      <div className="w-52 bg-white border-r border-gray-200 shrink-0 hidden md:flex flex-col">
        <div className="px-4 py-4 border-b border-gray-100">
          <h2 className="font-semibold text-gray-900 text-sm">AI Customer Service</h2>
          <p className="text-xs text-gray-400 mt-0.5">Manage chatbot &amp; conversations</p>
        </div>
        <nav className="flex-1 px-2 py-3 space-y-0.5">
          {visibleMenus.map((item) => {
            const active = pathname === item.href;
            const Icon = ICON_MAP[item.icon || ""] || HelpCircle;
            return (
              <Link
                key={item.id}
                href={item.href}
                className={`flex items-center gap-2.5 px-3 py-2 rounded-md text-sm transition-colors ${
                  active ? "bg-blue-50 text-blue-700 font-medium" : "text-gray-600 hover:bg-gray-100"
                }`}
              >
                <Icon className={`w-4 h-4 ${active ? "text-blue-600" : "text-gray-400"}`} />
                {item.label}
              </Link>
            );
          })}
        </nav>
      </div>

      <div className="flex-1 overflow-y-auto p-4 sm:p-6">
        {children}
      </div>
    </div>
  );
}
