"use client";

import Link from "next/link";
import { usePathname, useRouter } from "next/navigation";
import { useState, useRef, useEffect } from "react";
import { Bell, Search, Zap, LogOut, Menu, Store, CreditCard, Users, MessageSquare, AlertTriangle, Check } from "lucide-react";
import { useAppModuleStore } from "@/lib/app-registry";
import { usePlatformStore } from "@/lib/store";
import { useAuthStore } from "@/lib/stores/useAuthStore";
import { useNotificationStore } from "@/lib/stores/useNotificationStore";
import { useUserAccessStore } from "@/lib/stores/useUserAccessStore";

function NotificationDropdown() {
  const [open, setOpen] = useState(false);
  const ref = useRef<HTMLDivElement>(null);
  const { user } = useAuthStore();
  const { notifications, unreadCount, fetch, markRead, markAllRead } = useNotificationStore();

  useEffect(() => {
    if (user) fetch(user.tenant_id, user.id);
  }, [user, fetch]);

  useEffect(() => {
    function handleClick(e: MouseEvent) {
      if (ref.current && !ref.current.contains(e.target as Node)) setOpen(false);
    }
    document.addEventListener("mousedown", handleClick);
    return () => document.removeEventListener("mousedown", handleClick);
  }, []);

  const handleMarkAllRead = () => {
    if (user) markAllRead(user.tenant_id, user.id);
  };

  const iconMap: Record<string, typeof Bell> = {
    usage_warning: AlertTriangle,
    team_invite: Users,
    payment: CreditCard,
    system: MessageSquare,
  };

  const timeAgo = (dateStr: string) => {
    const diff = Date.now() - new Date(dateStr).getTime();
    const mins = Math.floor(diff / 60000);
    if (mins < 60) return `${mins} menit lalu`;
    const hours = Math.floor(mins / 60);
    if (hours < 24) return `${hours} jam lalu`;
    return `${Math.floor(hours / 24)} hari lalu`;
  };

  return (
    <div className="relative" ref={ref}>
      <button onClick={() => setOpen(!open)} className="relative p-2 text-gray-500 hover:text-gray-700 hover:bg-gray-100 rounded-lg">
        <Bell className="w-5 h-5" />
        {unreadCount > 0 && (
          <span className="absolute top-1 right-1 min-w-[16px] h-4 bg-blue-600 text-white text-[10px] font-bold rounded-full flex items-center justify-center px-1">
            {unreadCount}
          </span>
        )}
      </button>

      {open && (
        <div className="absolute right-0 top-full mt-2 w-80 bg-white border border-gray-200 rounded-xl shadow-lg z-50 overflow-hidden">
          <div className="flex items-center justify-between px-4 py-3 border-b border-gray-100">
            <h3 className="font-semibold text-sm text-gray-900">Notifikasi</h3>
            {unreadCount > 0 && (
              <button onClick={handleMarkAllRead} className="text-xs text-blue-600 hover:text-blue-700 font-medium flex items-center gap-1">
                <Check className="w-3 h-3" /> Tandai semua dibaca
              </button>
            )}
          </div>

          <div className="max-h-80 overflow-y-auto divide-y divide-gray-50">
            {notifications.length === 0 && (
              <p className="text-center text-sm text-gray-400 py-8">Belum ada notifikasi</p>
            )}
            {notifications.map((n) => {
              const Icon = iconMap[n.type] || Bell;
              return (
                <Link
                  key={n.id}
                  href={n.action_url || "#"}
                  onClick={() => { markRead(n.id); setOpen(false); }}
                  className={`block px-4 py-3 hover:bg-gray-50 transition-colors ${!n.is_read ? "bg-blue-50/50" : ""}`}
                >
                  <div className="flex gap-3">
                    <div className={`w-8 h-8 rounded-full flex items-center justify-center shrink-0 ${
                      n.type === "usage_warning" ? "bg-amber-100 text-amber-600" :
                      n.type === "payment" ? "bg-emerald-100 text-emerald-600" :
                      n.type === "team_invite" ? "bg-blue-100 text-blue-600" :
                      "bg-gray-100 text-gray-600"
                    }`}>
                      <Icon className="w-4 h-4" />
                    </div>
                    <div className="flex-1 min-w-0">
                      <p className={`text-sm ${!n.is_read ? "font-medium text-gray-900" : "text-gray-700"}`}>{n.title}</p>
                      <p className="text-xs text-gray-500 mt-0.5 truncate">{n.message}</p>
                      <p className="text-[11px] text-gray-400 mt-1">{timeAgo(n.created_at)}</p>
                    </div>
                    {!n.is_read && <span className="w-2 h-2 bg-blue-600 rounded-full shrink-0 mt-2" />}
                  </div>
                </Link>
              );
            })}
          </div>

          <Link href="/settings?tab=notifications" onClick={() => setOpen(false)} className="block text-center text-xs text-blue-600 hover:text-blue-700 font-medium py-3 border-t border-gray-100 hover:bg-gray-50">
            Lihat semua notifikasi
          </Link>
        </div>
      )}
    </div>
  );
}

export default function DashboardLayout({ children }: { children: React.ReactNode }) {
  const pathname = usePathname();
  const router = useRouter();
  const { activeApps } = usePlatformStore();
  const { user, isAuthenticated, logout } = useAuthStore();
  const { modules, fetchModules } = useAppModuleStore();
  const { fetchAccess, hasModuleAccess } = useUserAccessStore();
  const [mobileOpen, setMobileOpen] = useState(false);

  useEffect(() => { fetchModules(); fetchAccess(); }, [fetchModules, fetchAccess]);

  const visibleApps = modules.filter(
    (app) => app.is_permanent || (activeApps.includes(app.key) && hasModuleAccess(app.key))
  );

  const userInitials = user?.name
    ? user.name.split(" ").map((w) => w[0]).join("").slice(0, 2).toUpperCase()
    : "?";

  const handleLogout = () => {
    logout();
    router.push("/login");
  };

  return (
    <div className="h-screen flex overflow-hidden bg-gray-50">
      {mobileOpen && (
        <div className="fixed inset-0 bg-black/30 backdrop-blur-sm z-40 lg:hidden transition-opacity duration-300" onClick={() => setMobileOpen(false)} />
      )}

      <aside className={`
        fixed top-0 left-0 bottom-0 z-50 w-[64px] bg-blue-50 border-r border-blue-100 flex flex-col items-center py-4
        transform transition-all duration-300 ease-in-out
        lg:relative lg:transform-none lg:shrink-0
        ${mobileOpen ? "translate-x-0" : "-translate-x-full lg:translate-x-0"}
      `}>
        <div className="w-9 h-9 bg-blue-600 rounded-lg flex items-center justify-center mb-4 shadow-sm">
          <Zap className="w-5 h-5 text-white" />
        </div>

        <nav className="flex-1 flex flex-col items-center gap-1.5 overflow-y-auto">
          {visibleApps.map((app) => {
            const active = pathname === app.href || pathname.startsWith(app.href + "/");
            return (
              <Link key={app.id} href={app.href} onClick={() => setMobileOpen(false)} title={app.name}
                className={`w-10 h-10 rounded-lg flex items-center justify-center transition-all duration-200 relative group ${
                  active ? "bg-blue-600 text-white shadow-sm" : "text-blue-400 hover:text-blue-700 hover:bg-blue-100"
                }`}>
                <app.icon className="w-5 h-5" />
                {active && <span className="absolute left-0 top-1/2 -translate-y-1/2 w-0.5 h-5 bg-blue-700 rounded-r" />}
                <span className="absolute left-14 bg-blue-900 text-white text-xs px-2 py-1 rounded opacity-0 group-hover:opacity-100 pointer-events-none whitespace-nowrap z-50 shadow-lg transition-opacity duration-200">{app.name}</span>
              </Link>
            );
          })}

          <Link href="/app-store" title="App Store"
            className={`w-10 h-10 rounded-lg flex items-center justify-center transition-all duration-200 mt-2 border border-dashed group ${
              pathname === "/app-store" ? "bg-blue-600 text-white border-blue-600" : "text-blue-300 border-blue-200 hover:text-blue-700 hover:border-blue-400 hover:bg-blue-100"
            }`}>
            <Store className="w-4 h-4" />
            <span className="absolute left-14 bg-blue-900 text-white text-xs px-2 py-1 rounded opacity-0 group-hover:opacity-100 pointer-events-none whitespace-nowrap z-50 shadow-lg transition-opacity duration-200">App Store</span>
          </Link>
        </nav>

        <button onClick={handleLogout} className="w-10 h-10 rounded-lg flex items-center justify-center text-blue-300 hover:text-red-500 hover:bg-red-50 transition-all duration-200" title="Keluar">
          <LogOut className="w-5 h-5" />
        </button>
      </aside>

      <div className="flex-1 flex flex-col overflow-hidden w-0">
        <header className="h-14 bg-white border-b border-gray-200 flex items-center gap-4 px-4 sm:px-6 shrink-0">
          <button className="lg:hidden p-2 -ml-2 text-gray-600 hover:bg-gray-100 rounded-lg" onClick={() => setMobileOpen(true)}>
            <Menu className="w-5 h-5" />
          </button>

          <div className="flex-1 max-w-md hidden sm:block">
            <div className="relative">
              <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-gray-400" />
              <input type="text" placeholder="Search..." className="w-full h-8 pl-9 pr-3 rounded-md border border-gray-200 bg-gray-50 text-sm text-gray-700 placeholder:text-gray-400 focus:outline-none focus:border-blue-300" />
            </div>
          </div>

          <div className="flex items-center gap-3 ml-auto">
            <NotificationDropdown />
            <div className="w-8 h-8 rounded-full bg-blue-100 text-blue-700 flex items-center justify-center text-xs font-semibold" title={user?.name || ""}>
              {user?.avatar_url ? (
                <img src={user.avatar_url} alt="" className="w-8 h-8 rounded-full object-cover" />
              ) : userInitials}
            </div>
          </div>
        </header>

        <main className="flex-1 h-0 overflow-hidden pl-2">
          {children}
        </main>
      </div>
    </div>
  );
}
