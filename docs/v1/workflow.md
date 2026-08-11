# Agentic AI Platform — Workflow Documentation

## 🏗️ Platform Overview

Platform SaaS multi-tenant yang menggunakan multi-agent AI untuk mensimulasikan tim engineering startup. Platform ini memiliki 2 layer utama:

1. **Generator Layer** — Python agents yang generate code & dokumen
2. **Product Layer** — Next.js web app (hasil dari generator) yang dipakai end-user

---

## 🔄 Development Workflow (Generator)

### Flow Lengkap

```
┌──────────────┐     ┌──────────────┐     ┌──────────────┐     ┌──────────────┐
│  commands/   │────▶│   main.py    │────▶│   agents/    │────▶│   runtime/   │
│  (prompts)   │     │  (generator) │     │  (classes)   │     │  (runners)   │
└──────────────┘     └──────────────┘     └──────────────┘     └──────────────┘
                                                                       │
                                                                       ▼
                                                               ┌──────────────┐
                                                               │   docs/v1/   │
                                                               │  (output)    │
                                                               └──────────────┘
```

### Step-by-Step

1. **Define Prompt** — Tulis instruksi di `commands/create_{role}.py`
2. **Generate Agent** — Jalankan `py main.py --agent {role}` → output ke `agents/{role}.py`
3. **Run Agent** — Jalankan `py runtime/run_agent_{role}.py "prompt"` → output ke `docs/v1/`
4. **Code Mode** — Jalankan `py runtime/run_agent_{role}.py --code "prompt"` → tulis langsung ke project

### Agent Roles & Responsibilities

| Order | Agent | Tugas | Depends On |
|-------|-------|-------|------------|
| 1 | CEO | Visi produk, prioritas MVP | — |
| 2 | Product Manager | PRD, user stories, roadmap | CEO |
| 3 | Architect | System design, ERD, API spec | PM |
| 4 | Database Engineer | Schema, migrations, RLS | Architect |
| 5 | Backend Engineer | FastAPI modules, REST API | Architect, DB |
| 6 | Frontend Engineer | Next.js pages, components | Architect, Backend |
| 7 | UI/UX Designer | Design tokens, wireframes | PM |
| 8 | QA Engineer | Testing, code review | Backend, Frontend |
| 9 | DevOps | Docker, CI/CD, deployment | All |
| 10 | Marketing | Copy, SEO, landing page | PM, UI/UX |
| 11 | Documentation | API docs, user guides | All |

### Recommended Execution Order

```bash
# Phase 1: Strategy & Planning
py runtime/run_agent_ceo.py "Tentukan MVP untuk AI Employee Platform"
py runtime/run_agent_product_manager.py "Buat PRD lengkap berdasarkan visi CEO"

# Phase 2: Architecture & Design
py runtime/run_agent_architect.py "Design arsitektur lengkap: folder structure, ERD, API"
py runtime/run_agent_ui_ux.py "Design spec untuk semua halaman MVP"

# Phase 3: Implementation
py runtime/run_agent_database_engineer.py --code "Buat SQLAlchemy models"
py runtime/run_agent_backend_engineer.py --code "Buat module auth + AI agents"
py runtime/run_agent_frontend_engineer.py --code "Buat halaman dashboard + billing"

# Phase 4: Quality & Deploy
py runtime/run_agent_qa.py "Review semua module: security + performance"
py runtime/run_agent_devops.py --code "Buat docker-compose + CI/CD"
py runtime/run_agent_documentation.py "Buat API docs + user guide"
py runtime/run_agent_marketing.py "Buat copy landing page + SEO"
```

---

## 🌐 Product Workflow (End-User)

### User Journey

```
┌─────────┐    ┌─────────┐    ┌──────────┐    ┌───────────┐    ┌──────────┐
│ Landing │───▶│Register │───▶│  Login   │───▶│   Home    │───▶│ App Use  │
│  Page   │    │  + OTP  │    │  (Auth)  │    │(Overview) │    │(Workspace)│
└─────────┘    └─────────┘    └──────────┘    └───────────┘    └──────────┘
```

### Authentication Flow

```
1. User buka /register
2. Isi form (nama, email, password) ATAU klik Google OAuth
3. Sistem kirim OTP via Telegram/WhatsApp/Email
4. User verify OTP di /otp-verification
5. Redirect ke /home (dashboard)
6. Session: JWT stored di cookie
```

### App Activation Flow

```
1. User di /home → lihat app yang aktif
2. Klik "Tambah App" atau buka /app-store
3. Browse available apps (AI CS, AI Sales, Konveksi, dll)
4. Klik "Activate" → app muncul di sidebar
5. Redirect ke workspace app
6. Deactivate → app hilang dari sidebar, data tetap tersimpan
```

### Daily Usage Flow

```
1. Login → /home (overview semua active apps)
2. Klik app icon di sidebar ATAU card di home
3. Masuk workspace app (layout berubah sesuai app)
4. Navigasi sub-menu dalam app
5. Switch app via icon sidebar
6. Settings/Billing via icon Settings
```

---

## 💳 Billing Workflow

### Plan Structure

| Feature | Starter (Free) | Pro (Rp 199k/bln) | Enterprise |
|---------|---------------|-------------------|------------|
| Messages/bulan | 1,000 | 10,000 | Unlimited |
| AI Agents | 1 | 5 | Unlimited |
| Apps | 2 | 5 | Unlimited |
| Integrations | 1 (WhatsApp) | Semua | Custom |
| Support | Community | Priority | Dedicated |
| Custom Training | ❌ | ✅ | ✅ |

### Upgrade Flow

```
1. User di /billing → lihat current plan & usage
2. Klik "Upgrade" pada plan yang diinginkan
3. Redirect ke payment gateway (Midtrans/Xendit)
4. Bayar → webhook konfirmasi → plan aktif
5. Fitur baru langsung tersedia
6. Invoice tersimpan di history
```

### Usage Tracking

```
- Messages: counter per bulan, reset setiap tanggal 1
- Agents: count active agents
- Storage: total file upload size
- API calls: request count ke backend
- Alert di 80% usage → suggest upgrade
```

### Billing API Endpoints

| Method | Endpoint | Deskripsi |
|--------|----------|-----------|
| GET | `/api/v1/billing/plans` | List semua plan yang tersedia |
| GET | `/api/v1/billing/overview?tenant_id=` | Overview: subscription + usage + invoices |
| GET | `/api/v1/billing/usage?tenant_id=` | Usage detail (messages, agents, apps, storage) |
| POST | `/api/v1/billing/subscribe?tenant_id=` | Subscribe ke plan baru |
| POST | `/api/v1/billing/cancel?tenant_id=` | Cancel subscription |
| POST | `/api/v1/billing/webhook` | Payment gateway webhook (Midtrans) |
| GET | `/api/v1/billing/invoices?tenant_id=` | List invoice history |

### Usage Gating (Enforcement)

```
Middleware: app/middleware/usage_gate.py

Gated Routes:
- POST /api/v1/conversations/send → checks "messages" quota
- POST /api/v1/ai-agents          → checks "agents" quota
- POST /api/v1/apps/activate      → checks "apps" quota

Response when exceeded (HTTP 429):
{
  "error": "quota_exceeded",
  "metric": "messages",
  "message": "Kuota messages sudah habis. Upgrade plan untuk melanjutkan."
}
```

### Subscription States

```
pending   → menunggu pembayaran
active    → aktif, bisa dipakai
trialing  → trial period (14 hari)
past_due  → pembayaran gagal, grace period
canceled  → dibatalkan (masih akses sampai period end)
expired   → sudah lewat period end
```

---

## 🔌 Integration Workflow

### Supported Channels

| Channel | Status | Use Case |
|---------|--------|----------|
| WhatsApp (WA Business API) | ✅ Ready | CS, Sales, Notifikasi |
| Telegram Bot | ✅ Ready | CS, OTP, Notifikasi |
| Email (SMTP/SendGrid) | ✅ Ready | Notifikasi, Marketing |
| Web Chat Widget | ✅ Ready | CS embed di website |
| Instagram DM | 🔜 Coming | CS, Marketing |
| Shopee Chat | 🔜 Coming | E-commerce CS |

### Connection Flow

```
1. User buka /integrations
2. Pilih channel (misal: WhatsApp)
3. Klik "Connect"
4. Isi credentials (API key, phone number, dll)
5. Test connection → success/fail feedback
6. Assign ke AI Agent tertentu
7. Channel aktif → pesan masuk otomatis di-handle agent
```

### WhatsApp Setup Detail

```
1. Buat WhatsApp Business Account
2. Daftar di Meta Business → dapatkan API token
3. Masukkan token + phone number ID di /integrations
4. Verify webhook URL (auto-generated)
5. Test kirim pesan → konfirmasi connected
6. Assign ke agent → live!
```

---

## 📂 Frontend Route Structure

```
/ (landing)
├── /login
├── /register
├── /otp-verification
│
├── /home                    ← Dashboard overview
├── /app-store               ← Browse & activate apps
├── /billing                 ← Plans, usage, payment
├── /integrations            ← Channel connections
├── /settings                ← Profile, team, preferences
│
├── /apps/ai-cs/             ← AI Customer Service workspace
│   ├── agents/
│   ├── conversations/
│   └── analytics/
│
├── /apps/ai-sales/          ← AI Sales workspace
│   ├── pipeline/
│   ├── leads/
│   └── campaigns/
│
├── /apps/konveksi/          ← Konveksi workspace
│   ├── orders/
│   ├── production/
│   └── materials/
│
└── /apps/inventory/         ← Inventory workspace
    ├── products/
    └── alerts/
```

---

## 🛡️ Security & Multi-Tenant

```
- Tenant isolation via RLS (Row Level Security) di PostgreSQL
- JWT token per session, refresh token rotation
- API rate limiting per tenant/plan
- Webhook signature verification untuk payment & integrations
- Encrypted credentials storage untuk API keys integrasi
- Audit log untuk semua perubahan kritis
```

---

## 🚀 Deployment Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    Nginx (Reverse Proxy)                  │
├──────────────────────┬──────────────────────────────────┤
│  Next.js (Frontend)  │  FastAPI (Backend)                │
│  Port 3000           │  Port 8000                        │
├──────────────────────┴──────────────────────────────────┤
│              PostgreSQL + Redis                           │
├─────────────────────────────────────────────────────────┤
│              Docker Compose (VPS)                         │
└─────────────────────────────────────────────────────────┘
```

---

## 📋 Tech Stack Summary

| Layer | Technology |
|-------|-----------|
| Frontend | Next.js 14, React 18, TailwindCSS, shadcn/ui, Zustand |
| Backend | FastAPI, SQLAlchemy, Alembic, Pydantic |
| Database | PostgreSQL (Supabase/self-hosted) |
| Cache | Redis |
| Auth | JWT + Google OAuth + OTP (Telegram/WA/Email) |
| Payment | Midtrans / Xendit |
| AI | LangChain + Gemini/GPT/Groq |
| Deploy | Docker, Nginx, GitHub Actions, VPS |
