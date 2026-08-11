# Multi-App SaaS Platform — Rule Flow & Workflow

## 🏗️ Arsitektur Platform

```
┌─────────────────────────────────────────────────────────┐
│  PLATFORM SHELL (shared layout)                         │
│  ┌──────┬────────────────────────────────────────────┐  │
│  │ Icon │  App Workspace (layout per app)            │  │
│  │ Bar  │                                            │  │
│  │      │  ┌─────────────────────────────────────┐   │  │
│  │ 🏠   │  │  App-specific sub menu + content    │   │  │
│  │ 🤖   │  │                                     │   │  │
│  │ 🏭   │  │  (tiap app beda layout)             │   │  │
│  │ 📦   │  │                                     │   │  │
│  │ ⚙️   │  └─────────────────────────────────────┘   │  │
│  └──────┴────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────┘
```

## 📋 Konsep

### 1. Platform Level
- **Platform Shell**: Icon sidebar kiri (app switcher) + top bar (search, notif, user)
- **Home**: Dashboard overview semua app yang aktif
- **App Store**: Halaman untuk activate/deactivate apps
- **Settings**: Global settings (profil, tim, billing)

### 2. App Level
- Setiap app = module independen dengan layout sendiri
- User bisa activate/deactivate app dari App Store
- App yang aktif muncul di icon sidebar
- Setiap app punya sub-menu, pages, dan workflow sendiri

## 📦 Daftar Apps (Modular)

| App ID | Nama | Icon | Deskripsi | Layout |
|--------|------|------|-----------|--------|
| `home` | Home | 🏠 | Dashboard overview | Stats + recent activity |
| `ai-cs` | AI Customer Service | 💬 | Chatbot CS otomatis | Chat panel + analytics |
| `ai-sales` | AI Sales Agent | 📈 | Sales automation | Pipeline + leads |
| `ai-support` | AI Support | 🎧 | Ticket & escalation | Ticket list + detail |
| `konveksi` | Konveksi App | 🏭 | Monitoring produksi | Kanban + timeline |
| `inventory` | Inventory | 📦 | Stock management | Table + alerts |
| `settings` | Settings | ⚙️ | Platform settings | Tabs form |

## 🔄 User Flow

### Onboarding
```
Register → Login → Home (empty state) → App Store → Activate App(s) → Redirect ke App
```

### App Activation
```
App Store → Klik "Activate" pada app → 
  → App muncul di icon sidebar
  → App tersedia di home dashboard
  → User bisa masuk ke workspace app
```

### App Deactivation
```
Settings → Apps → Klik "Deactivate" →
  → App hilang dari icon sidebar
  → Data TIDAK dihapus (bisa activate lagi)
```

### Switching App
```
Klik icon app di sidebar kiri → Masuk ke workspace app tersebut (layout berubah)
```

## 🗂️ Folder Structure

```
frontend/app/(dashboard)/
├── layout.tsx                    ← Platform shell (icon sidebar + topbar)
├── home/page.tsx                 ← Overview semua active apps
├── app-store/page.tsx            ← Activate/deactivate apps
│
├── apps/
│   ├── ai-cs/                    ← AI Customer Service workspace
│   │   ├── layout.tsx            ← CS-specific sub menu
│   │   ├── page.tsx              ← CS dashboard
│   │   ├── agents/page.tsx       ← Agent list
│   │   ├── conversations/page.tsx
│   │   └── analytics/page.tsx
│   │
│   ├── ai-sales/                 ← AI Sales workspace
│   │   ├── layout.tsx            ← Sales-specific sub menu
│   │   ├── page.tsx              ← Sales dashboard
│   │   ├── pipeline/page.tsx
│   │   ├── leads/page.tsx
│   │   └── campaigns/page.tsx
│   │
│   ├── ai-support/               ← AI Support workspace
│   │   ├── layout.tsx            ← Support-specific sub menu
│   │   ├── page.tsx              ← Support dashboard
│   │   ├── tickets/page.tsx
│   │   └── knowledge-base/page.tsx
│   │
│   ├── konveksi/                 ← Konveksi/Produksi workspace
│   │   ├── layout.tsx            ← Produksi-specific layout (kanban)
│   │   ├── page.tsx              ← Production overview
│   │   ├── orders/page.tsx       ← Order tracking
│   │   ├── production/page.tsx   ← Production monitoring
│   │   ├── materials/page.tsx    ← Bahan baku
│   │   └── workers/page.tsx      ← Pekerja/operator
│   │
│   └── inventory/                ← Inventory workspace
│       ├── layout.tsx
│       ├── page.tsx
│       ├── products/page.tsx
│       └── alerts/page.tsx
│
└── settings/
    ├── page.tsx                  ← Profil
    ├── team/page.tsx
    ├── billing/page.tsx
    └── apps/page.tsx             ← Manage active apps
```

## 🔐 Rule: App Visibility

```typescript
// Data model
interface UserApp {
  appId: string;
  active: boolean;
  activatedAt: Date;
  config?: Record<string, any>;  // app-specific settings
}

// Rules:
// 1. Home & Settings selalu visible (tidak bisa deactivate)
// 2. App lain harus di-activate dulu
// 3. Icon sidebar hanya tampil app yang active
// 4. Route guard: jika user akses app yang belum active → redirect ke App Store
// 5. Setiap app punya layout sendiri (sub menu berbeda)
// 6. Deactivate app TIDAK hapus data
```

## 🎨 Layout Per App

### AI Customer Service
```
[Sub Menu]          [Content]
- Dashboard         Chat interface / analytics
- Agents            Agent CRUD + config
- Conversations     Chat history + search
- Analytics         Charts + metrics
```

### AI Sales
```
[Sub Menu]          [Content]
- Dashboard         Pipeline overview
- Leads             Lead list + scoring
- Pipeline          Kanban board
- Campaigns         Outreach campaigns
```

### Konveksi App
```
[Sub Menu]          [Content]
- Overview          Production stats
- Orders            Order tracking (timeline)
- Production        Kanban (cutting → sewing → QC → packing)
- Materials         Stock bahan baku
- Workers           Operator assignment
```

## 📊 State Management

```typescript
// Zustand store
interface PlatformStore {
  user: User;
  activeApps: UserApp[];       // apps yang di-activate user
  currentApp: string | null;   // app yang sedang dibuka
  
  activateApp: (appId: string) => void;
  deactivateApp: (appId: string) => void;
  setCurrentApp: (appId: string) => void;
}
```

## 🔄 Workflow: Activate App Baru

```
1. User buka /app-store
2. Lihat list semua available apps (card grid)
3. Klik "Activate" pada app (misal: AI Sales)
4. API call: POST /api/v1/apps/activate { appId: "ai-sales" }
5. Backend enable app untuk tenant/user
6. Frontend update store → app muncul di sidebar
7. Redirect ke /apps/ai-sales (workspace app)
8. User lihat app dashboard (empty state jika baru)
```

## 🔄 Workflow: User Daily Usage

```
1. Login → /home (overview cards semua active apps)
2. Klik card "AI Sales" atau icon di sidebar
3. Masuk /apps/ai-sales → layout berubah ke Sales workspace
4. Navigasi di sub menu Sales (leads, pipeline, dll)
5. Klik icon "Konveksi" di sidebar → pindah ke /apps/konveksi
6. Layout berubah ke Konveksi workspace (kanban style)
7. Klik icon "Home" → balik ke overview
```
