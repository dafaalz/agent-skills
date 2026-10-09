# Claude Web Skills (Sonnet 5.5 Medium)

Kumpulan skill kustom yang dioptimalkan khusus untuk **Claude Web** (claude.ai) menggunakan model **Claude Sonnet 5.5** dengan setelan effort medium.

Setiap skill telah disesuaikan agar:
1. Menghilangkan asumsi perkakas CLI/shell yang tidak tersedia di web.
2. Menerapkan panduan resmi *Prompting Claude Sonnet 5.5* (steering initiative & scope, eliminasi reasoning extraction, fact-checking via web search, dan kelengkapan kode).
3. Memanfaatkan **Claude Artifacts** untuk output dokumen (Design Spec ADR, Laporan Audit UI/UX, Rewrite Teks, Motion Code, Implementation Plans, dan Preview UI Komponen).
4. Menyertakan dokumen `references/` lengkap dalam paket arsip `.skill` / `.zip`.

---

## Daftar Skill

| Skill | Fungsi Utama | Pemicu (Trigger) |
|---|---|---|
| [unslop](file:///Users/groundfox/agent-skills/web-skills/unslop/SKILL.md) | Membersihkan AI slop, klise korporat, dan memulihkan ritme tulisan manusia (EN & ID). | "unslop", "hapus gaya AI", "edit tulisan ini", "review gaya bahasa" |
| [brainstorming](file:///Users/groundfox/agent-skills/web-skills/brainstorming/SKILL.md) | Validasi ide, stress-testing arsitektur via teknik grilling, dan pembuatan dokumen ADR Design Spec. | "brainstorm", "desain arsitektur", "grill ide saya", "rancang fitur baru" |
| [ui-ux-review](file:///Users/groundfox/agent-skills/web-skills/ui-ux-review/SKILL.md) | Audit antarmuka & kode frontend secara empiris (WCAG 2.2 AA, cognitive laws, Before-After-Why). | "audit UI", "review UX", "cek accessibility", "audit form ini" |
| [ui-motion](file:///Users/groundfox/agent-skills/web-skills/ui-motion/SKILL.md) | Desain & optimasi animasi hardware-accelerated, micro-interactions, dan token easing. | "bikin animasi", "ui-motion", "perbaiki transisi CSS", "gesture interaction" |
| [frontend-design](file:///Users/groundfox/agent-skills/web-skills/frontend-design/SKILL.md) | Desain antarmuka craft tinggi, kalibrasi dial (kreativitas/densitas), token warna, dan preview komponen UI. | "desain frontend", "bikin landing page", "rancang UI", "buat komponen React/Tailwind" |
| [writing-for-agents](file:///Users/groundfox/agent-skills/web-skills/writing-for-agents/SKILL.md) | Penulisan instruksi agent (AGENTS.md, SKILL.md, prompt) dan Phased Implementation Plans bertahap. | "tulis instruksi agent", "bikin skill baru", "buat implementation plan", "tulis AGENTS.md" |

---

## Cara Upload ke Claude Web

Berdasarkan fitur native **Upload a skill** di Claude Web:

1. Buka [claude.ai](https://claude.ai).
2. Masuk ke menu **Customize** (ikon profil / pengaturan) lalu pilih **Skills**.
3. Klik tombol **+ Add** $\rightarrow$ **Upload a skill**.
4. Drag & drop file `.skill` (atau `.zip`) dari folder `web-skills/dist/`:
   - `web-skills/dist/unslop.skill`
   - `web-skills/dist/brainstorming.skill`
   - `web-skills/dist/ui-ux-review.skill`
   - `web-skills/dist/ui-motion.skill`
   - `web-skills/dist/frontend-design.skill`
   - `web-skills/dist/writing-for-agents.skill`
5. Pastikan toggle skill diaktifkan (**ON**).
