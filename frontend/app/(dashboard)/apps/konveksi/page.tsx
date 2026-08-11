import { ClipboardList, Layers, AlertTriangle, CheckCircle } from "lucide-react";

const stats = [
  { label: "Order Aktif", value: "12", icon: ClipboardList, color: "text-orange-600 bg-orange-50" },
  { label: "Dalam Produksi", value: "8", icon: Layers, color: "text-blue-600 bg-blue-50" },
  { label: "Selesai Hari Ini", value: "5", icon: CheckCircle, color: "text-emerald-600 bg-emerald-50" },
  { label: "Perlu Perhatian", value: "2", icon: AlertTriangle, color: "text-red-600 bg-red-50" },
];

export default function KonveksiOverview() {
  return (
    <div className="space-y-6">
      <h1 className="text-xl font-bold text-gray-900">Monitoring Produksi</h1>
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        {stats.map((s) => (
          <div key={s.label} className="bg-white rounded-xl border border-gray-200 p-4">
            <div className={`w-8 h-8 rounded-lg flex items-center justify-center mb-2 ${s.color}`}>
              <s.icon className="w-4 h-4" />
            </div>
            <p className="text-2xl font-bold text-gray-900">{s.value}</p>
            <p className="text-xs text-gray-500">{s.label}</p>
          </div>
        ))}
      </div>
    </div>
  );
}
