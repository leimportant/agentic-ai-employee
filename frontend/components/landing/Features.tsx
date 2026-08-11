import { MessageSquare, TrendingUp, Headphones, Factory, BarChart3, Plug } from "lucide-react";

const features = [
  {
    icon: MessageSquare,
    title: "AI Customer Service",
    desc: "Chatbot WhatsApp & web 24/7. Jawab FAQ, terima order, dan handle komplain otomatis.",
  },
  {
    icon: TrendingUp,
    title: "AI Sales Agent",
    desc: "Follow-up lead, kirim penawaran, closing otomatis. Tingkatkan revenue tanpa tambah tim.",
  },
  {
    icon: Headphones,
    title: "AI Support",
    desc: "Eskalasi tiket cerdas, knowledge base AI, resolve issue lebih cepat untuk korporasi & UMKM.",
  },
  {
    icon: Factory,
    title: "Custom Apps",
    desc: "Digitalisasi & monitoring produksi, inventory, atau proses bisnis lainnya dengan AI agent.",
  },
  {
    icon: BarChart3,
    title: "Dashboard & Analytics",
    desc: "Pantau performa semua agent, tracking percakapan, dan analisa biaya token real-time.",
  },
  {
    icon: Plug,
    title: "Multi-Channel",
    desc: "Integrasikan ke WhatsApp, Telegram, web chat, dan sistem internal. Setup dalam 5 menit.",
  },
];

export function Features() {
  return (
    <section id="features" className="py-20 bg-white">
      <div className="max-w-[1200px] mx-auto px-6">
        <div className="text-center mb-14">
          <h2 className="text-3xl font-bold text-gray-900 tracking-tight">
            Satu platform, semua solusi AI
          </h2>
          <p className="mt-3 text-gray-500 text-lg">
            Dari customer service sampai monitoring produksi, semuanya bisa diotomasi.
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-5">
          {features.map((f) => (
            <div
              key={f.title}
              className="group p-6 bg-white border border-gray-200 rounded-xl shadow-sm hover:border-blue-500 hover:shadow-md transition-all duration-200 hover:-translate-y-0.5"
            >
              <div className="w-10 h-10 bg-blue-50 text-blue-600 rounded-lg flex items-center justify-center mb-4 group-hover:bg-blue-100 transition-colors">
                <f.icon className="w-5 h-5" />
              </div>
              <h3 className="text-base font-semibold text-gray-900 mb-2">{f.title}</h3>
              <p className="text-sm text-gray-500 leading-relaxed">{f.desc}</p>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}
