# Agentic AI Employee Platform

Framework untuk generate SaaS web app menggunakan multi-agent AI yang mensimulasikan tim engineering startup.

## 📁 Struktur Project

```
agenticAi/
├── main.py                  # Generator: buat semua agent files via LLM
├── .env                     # API keys (GOOGLE_API_KEY, dll)
│
├── commands/                # Prompt/instruksi untuk generate setiap agent
│   ├── create_product_manager.py
│   ├── create_architect.py
│   ├── create_backend_engineer.py
│   ├── create_frontend_engineer.py
│   ├── create_qa.py
│   ├── create_documentation.py
│   ├── create_devops.py
│   ├── create_marketing.py
│   ├── create_ceo.py
│   ├── create_ui_ux.py
│   └── create_database_engineer.py
│
├── agents/                  # Agent classes (hasil generate)
│   ├── __init__.py
│   ├── *_.py                # ← BACKUP (file manual/stabil)
│   └── *.py                 # ← GENERATED (output dari main.py)
│
├── runtime/                 # Script untuk MENJALANKAN agent secara individual
│   ├── run_agent_ceo.py
│   ├── run_agent_product_manager.py
│   ├── run_agent_architect.py
│   ├── run_agent_backend_engineer.py
│   ├── run_agent_frontend_engineer.py
│   ├── run_agent_qa.py
│   ├── run_agent_devops.py
│   ├── run_agent_marketing.py
│   ├── run_agent_documentation.py
│   ├── run_agent_database_engineer.py
│   └── run_agent_ui_ux.py
│
├── builder/                 # Alternative generator (simpler version)
│   └── app.py
│
├── docs/v1/                 # Output dokumen dari runtime agents
│   └── *.md
│
├── tools/                   # (future) shared tools untuk agents
└── memory/                  # (future) agent memory/context storage
```

## 🔗 Hubungan Antar Folder

```
commands/          →  main.py  →  agents/
(PROMPT/instruksi)    (GENERATOR)   (OUTPUT: class Python)

agents/*_.py       =  BACKUP (file stabil, tidak di-overwrite)
agents/*.py        =  GENERATED (hasil dari main.py, bisa di-regenerate)

agents/            →  runtime/
(class definition)    (RUNNER: jalankan agent, simpan output ke docs/)
```

### Flow:

1. **`commands/`** berisi PROMPT instruksi untuk setiap role agent
2. **`main.py`** membaca prompt dari commands → kirim ke LLM → generate code → simpan ke `agents/*.py`
3. **`runtime/`** meng-import agent class dari `agents/*_.py` (backup) → jalankan → simpan output ke `docs/v1/`

## 🚀 Cara Pakai

### 1. Setup

```bash
pip install langchain-google-genai langchain-openai langchain-anthropic langchain-groq python-dotenv
```

Isi `.env` (minimal satu, bisa semua untuk fallback):
```
# Prioritas fallback: Groq → Gemini → OpenAI → Kiro
GROQ_API_KEY=gsk_your_groq_key
GOOGLE_API_KEY=your_google_api_key
OPENAI_API_KEY=your_openai_api_key
KIRO_API_KEY=your_anthropic_api_key
```

### 2. Generate Agents (main.py)

```bash
# Generate SEMUA agent
py main.py

# Generate agent tertentu saja
py main.py --agent architect backend_engineer

# Lihat daftar agent yang tersedia
py main.py --list
```

Output: `agents/{role}.py`

### 3. Jalankan Agent (runtime/)

Setiap agent bisa dijalankan dengan **interactive prompt** atau **CLI argument langsung**.
Output disimpan ke `docs/v1/{role}.md`.

#### 👔 CEO — Visi & Strategi
```bash
py runtime/run_agent_ceo.py
py runtime/run_agent_ceo.py "Tentukan prioritas MVP untuk launch bulan depan"
py runtime/run_agent_ceo.py "Breakdown fitur AI Customer Service jadi task untuk tim"
```
→ Output: `docs/v1/ceo_vision.md`

#### 📋 Product Manager — PRD & Roadmap
```bash
py runtime/run_agent_product_manager.py
py runtime/run_agent_product_manager.py "Buat PRD untuk fitur billing subscription dengan Midtrans"
py runtime/run_agent_product_manager.py "Tulis user stories untuk onboarding tenant baru"
```
→ Output: `docs/v1/prd.md`

#### 🏗️ Architect — System Design
```bash
py runtime/run_agent_architect.py
py runtime/run_agent_architect.py "Design arsitektur lengkap MVP: folder structure, ERD, API endpoints"
py runtime/run_agent_architect.py "Design auth flow: Google OAuth + OTP (Telegram/WA/Email)"
```
→ Output: `docs/v1/architecture.md`

#### ⚙️ Backend Engineer — FastAPI Implementation
```bash
py runtime/run_agent_backend_engineer.py
py runtime/run_agent_backend_engineer.py "Buat module auth: register, Google OAuth, OTP verification, JWT"
py runtime/run_agent_backend_engineer.py "Buat module ai_agents: CRUD agent + conversation endpoint"
```
→ Output: `docs/v1/backend.md`

#### 🎨 Frontend Engineer — Next.js Pages
```bash
py runtime/run_agent_frontend_engineer.py
py runtime/run_agent_frontend_engineer.py "Buat landing page hero section + pricing table"
py runtime/run_agent_frontend_engineer.py "Buat halaman dashboard admin dengan sidebar layout responsive"
```
→ Output: `docs/v1/frontend.md`

#### 🗄️ Database Engineer — Schema & Migrations
```bash
py runtime/run_agent_database_engineer.py
py runtime/run_agent_database_engineer.py "Buat SQLAlchemy models untuk semua tabel MVP"
py runtime/run_agent_database_engineer.py "Buat Alembic migration + RLS policy untuk tenant isolation"
```
→ Output: `docs/v1/database.md`

#### 🧪 QA Engineer — Testing & Review
```bash
py runtime/run_agent_qa.py
py runtime/run_agent_qa.py "Review auth module: cek security vulnerabilities dan tenant leakage"
py runtime/run_agent_qa.py "Tulis test cases pytest untuk billing module"
```
→ Output: `docs/v1/qa_report.md`

#### 🐳 DevOps — Deployment & Infra
```bash
py runtime/run_agent_devops.py
py runtime/run_agent_devops.py "Buat docker-compose.yml production + Nginx reverse proxy"
py runtime/run_agent_devops.py "Setup CI/CD GitHub Actions: test, build, deploy ke VPS"
```
→ Output: `docs/v1/devops.md`

#### 🎯 UI/UX Designer — Design Specs
```bash
py runtime/run_agent_ui_ux.py
py runtime/run_agent_ui_ux.py "Design spec landing page hero section dengan brand colors"
py runtime/run_agent_ui_ux.py "Design dashboard layout: sidebar, cards, tables"
```
→ Output: `docs/v1/ui_ux.md`

#### 📢 Marketing — Copy & Strategy
```bash
py runtime/run_agent_marketing.py
py runtime/run_agent_marketing.py "Buat copy landing page: headline, subheadline, CTA, features"
py runtime/run_agent_marketing.py "SEO strategy untuk keyword 'chatbot UMKM Indonesia'"
```
→ Output: `docs/v1/marketing.md`

#### 📝 Documentation — Technical Writing
```bash
py runtime/run_agent_documentation.py
py runtime/run_agent_documentation.py "Buat API documentation untuk auth module (endpoints, request/response)"
py runtime/run_agent_documentation.py "Buat user guide onboarding untuk pemilik UMKM"
```
→ Output: `docs/v1/documentation.md`

## 👥 Daftar Agents

| Agent | Role | Output File |
|-------|------|-------------|
| CEOAgent | Visi produk, prioritas, keputusan strategis | `ceo_vision.md` |
| ProductManagerAgent | PRD, roadmap, user stories | `prd.md` |
| ArchitectAgent | System design, multi-tenant architecture | `architecture.md` |
| BackendEngineerAgent | FastAPI, PostgreSQL, REST API | `backend.md` |
| FrontendEngineerAgent | Next.js, React, TailwindCSS, shadcn/ui | `frontend.md` |
| DatabaseEngineerAgent | Schema, migrations, indexing, RLS | `database.md` |
| QAAgent | Code review, testing, bug finding | `qa_report.md` |
| DevOpsAgent | Docker, Nginx, deployment, VPS | `devops.md` |
| UIUXAgent | Wireframes, design tokens, accessibility | `ui_ux.md` |
| MarketingAgent | SEO, landing page, marketing strategy | `marketing.md` |
| DocumentationAgent | README, API docs, technical writing | `documentation.md` |

## 📝 Konvensi Naming

- `agents/*_.py` → backup/stabil (import dari `runtime/`)
- `agents/*.py` → generated (output dari `main.py`)
- `commands/create_{role}.py` → prompt instruksi per agent
- `runtime/run_agent_{role}.py` → runner per agent


#### 📝 Mode Code (--code) — generate + tulis langsung ke project
```bash
  py runtime/run_agent_backend_engineer.py --code "Buat module auth: register, OAuth, OTP, JWT"
  py runtime/run_agent_frontend_engineer.py --code "Buat landing page hero section + pricing table"
  py runtime/run_agent_database_engineer.py --code "Buat SQLAlchemy models untuk semua tabel MVP"

  py runtime/run_agent_frontend_engineer.py --code "Buat halaman login: Google OAuth button + OTP verification form"
  py runtime/run_agent_frontend_engineer.py --code "Buat dashboard layout: sidebar responsive + halaman overview dengan stats cards"
  py runtime/run_agent_frontend_engineer.py --code "Buat halaman AI Agents: table list + create dialog"

```


Database Migration Commands
  
  cd D:\wwroot\agenticAi\backend
  
  # 1. Setup venv + install (sekali)
  py -m venv venv
  venv\Scripts\activate
  pip install -r requirements.txt
  
  # 2. Generate migration dari models
  alembic revision --autogenerate -m "initial schema"
  
  # 3. Jalankan migration ke database
  alembic upgrade head
  
  # 4. Rollback 1 step
  alembic downgrade -1
  
  # 5. Lihat status migration
  alembic current
  alembic history
  
  Tables yang Akan Di-generate
  
  Migration --autogenerate akan buat semua tabel ini otomatis dari models:
  
  ┌───────────────┬──────────────┐
  │ Table           │ Model        │
  ├─────────────────┼──────────────┤
  │ users           │ User         │
  ├─────────────────┼───────────────┤
  │ tenants         │ Tenant        │
  ├─────────────────┼───────────────┤
  │ plans           │ Plan          │
  ├─────────────────┼───────────────┤
  │ subscriptions   │ Subscription  │
  ├─────────────────┼───────────────┤
  │ invoices        │ Invoice       │
  ├─────────────────┼───────────────┤
  │ usage_logs      │ UsageLog      │
  ├─────────────────┼───────────────┤
  │ otp_codes       │ OtpCode       │
  ├─────────────────┼───────────────┤
  │ ai_agents       │ AiAgent       │
  ├─────────────────┼───────────────┤
  │ customers       │ Customer      │
  ├─────────────────┼───────────────┤
  │ conversations   │ Conversation  │
  ├─────────────────┼───────────────┤
  │ messages        │ Message       │
  ├─────────────────┼───────────────┤
  │ knowledge_bases │ KnowledgeBase │
  ├─────────────────┼───────────────┤
  │ kb_documents    │ KbDocument    │
  ├─────────────────┼───────────────┤
  │ team_invites    │ TeamInvite    │
  ├─────────────────┼───────────────┤
  │ notifications   │ Notification  │
  └─────────────────┴───────────────┘
  
  Prerequisite: PostgreSQL harus running dan database agentic_ai sudah dibuat:
  
  CREATE DATABASE agentic_ai;
  
  Atau update DATABASE_URL di backend/.env sesuai database kamu.

RUn Migration
cd D:\wwroot\agenticAi\backend
  .venv\Scripts\activate; alembic upgrade head
  
  # 2. Run seeder
  .venv\Scripts\activate; python -m app.seeders.app_modules