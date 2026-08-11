"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import { usePathname } from "next/navigation";
import {
  Factory, ClipboardList, Layers, Package, Users, Settings,
  BarChart3, Bot, MessageSquare, HelpCircle,
} from "lucide-react";
import type { LucideIcon } from "lucide-react";
import { api } from "@/lib/api";
import { useUserAccessStore } from "@/lib/stores/useUserAccessStore";

const ICON_MAP: Record<string, LucideIcon> = {
  Factory, ClipboardList, Layers, Package, Users, Settings,
  BarChart3, Bot, MessageSquare,
};

interface MenuItem {
  id: string;
  key: string;
  label: string;
  icon: string | null;
  href: string;
  sort_order: number;
}

export default function KonveksiLayout({ children }: { children: React.ReactNode }) {
  const pathname = usePathname();
  const { hasSubMenuAccess } = useUserAccessStore();
  const [menus, setMenus] = useState<MenuItem[]>([]);

  useEffect(() => {
    api.get("/menus/konveksi").then((r) => setMenus(r.data)).catch(() => {});
  }, []);

  const visibleMenus = menus.filter(
    (m) => m.key === "overview" || hasSubMenuAccess("konveksi", m.key)
  );

  return (
    <div className="flex flex-col h-full">
      <div className="bg-white border-b border-gray-200 px-4 sm:px-6 shrink-0">
        <div className="flex items-center gap-1 overflow-x-auto">
          {visibleMenus.map((tab) => {
            const active = pathname === tab.href;
            const Icon = ICON_MAP[tab.icon || ""] || HelpCircle;
            return (
              <Link
                key={tab.id}
                href={tab.href}
                className={`flex items-center gap-2 px-4 py-3 text-sm font-medium border-b-2 whitespace-nowrap transition-colors ${
                  active
                    ? "border-orange-500 text-orange-600"
                    : "border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300"
                }`}
              >
                <Icon className="w-4 h-4" />
                {tab.label}
              </Link>
            );
          })}
        </div>
      </div>

      <div className="flex-1 overflow-y-auto p-4 sm:p-6">
        {children}
      </div>
    </div>
  );
}
