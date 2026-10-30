# Resolusi Teknis Defect Catalog (F1-F5 & S1-S14)

Dokumen ini memetakan seluruh cacat fatal (F) dan cacat struktural (S) yang diidentifikasi dalam evaluasi adversarial eksternal, beserta implementasi mitigasi deterministik pada codebase T3 Operational Guardrail.

---

## 1. Cacat Fatal (F1 - F5) & Realitas Batas Keamanan

### F-1: Realitas Batas Token Gate & Proses Arbitrer di Bawah UID yang Sama
- **Diagnosis**: Jika proses arbitrer di bawah UID yang sama (`groundfox`) dapat memanggil framework Security macOS secara langsung, token gate dapat dipintas oleh proses di luar kontrol jika kode berbahaya berjalan di level host.
- **Batasan Jujur**:
  1. Pada sistem POSIX single-user tanpa isolasi kernel/container terpisah, seluruh proses milik user `groundfox` berbagi hak akses Keychain pada domain user. Pemblokiran biner `security` CLI mencegah pembacaan sederhana via shell tool, namun **bukan batas kriptografis terhadap kode native arbitrer pada UID yang sama**.
  2. Token gate diposisikan secara tepat sebagai **protokol otorisasi operasional agen (*human approval gate for agent tool calls*)**, bukan pertahanan terhadap malware host.
- **Status**: Diposisikan secara jujur dan transparan. Status isolasi host: **FAIL / Tidak Tersertifikasi**.

### F-2: Interpreter Runtimes (`npm` & `php`) dan Batas Intersepsi
- **Diagnosis**: Runtimes `npm run` atau `php artisan` mengeksekusi kode repositori dan secara teoritis dapat memunculkan subprocess atau memodifikasi file tanpa melewati gateway jika tidak diisolasi di sandbox kernel.
- **Batasan Jujur**:
  1. Allowlist subperintah `php artisan` dan nama skrip `npm run` adalah **batas kepatuhan operasional tugas (*task scope boundary*)**, bukan batas keamanan sandbox.
  2. Proteksi dispatch bekerja pada permukaan pemanggilan alat agen (ACP/MCP wire surface), memastikan agen tidak dapat memanggil perintah terlarang melalui tool call. Jika repositori memuat kode berbahaya di dalam hook test, hanya isolasi container/VM/UID terpisah yang dapat mengisolasinya.
- **Status**: Didefinisikan secara eksplisit sebagai operational guardrail.

### F-3: Penutupan Penuh Opsi Global Git (S-1 Remediation)
- **Diagnosis**: Opsi global Git seperti `-C <path>`, `--git-dir`, `--work-tree`, `--namespace`, `--bare`, dan `--attr-source` dapat mengalihkan operasi git ke luar repositori atau memintas kontrol direktori.
- **Implementasi**:
  1. Seluruh opsi pengalihan direktori dan repositori (`-C`, `--git-dir`, `--work-tree`, `--namespace`, `--bare`, `--attr-source`, `--super-prefix`) ditolak eksplisit di `t3_dispatch.py` dengan **Exit 73**.
  2. Pengecekan argumen mendeteksi format gandeng (`-C/path`) maupun terpisah (`-C /path`).
- **Status**: Teruji dan lolos 100%.

### F-4: Penolakan Vektor Eksekusi Git Helper & Config Pre-Existing
- **Diagnosis**: File `.git/config` bawaan repositori dapat mendefinisikan `diff.external`, `core.fsmonitor`, `credential.helper`, `core.sshCommand`, `filter.*`, atau `commit.gpgSign` yang mengeksekusi biner arbitrer saat perintah aman dijalankan.
- **Implementasi**:
  1. Setiap pemanggilan biner `git` yang aman disuntikkan argumen penimpa global berpresedensi tertinggi:
     `-c core.hooksPath=/dev/null`
     `-c core.editor=true`
     `-c core.pager=cat`
     `-c diff.external=`
     `-c core.fsmonitor=`
     `-c credential.helper=`
     `-c core.sshCommand=true`
     `-c commit.gpgSign=false`
  2. Variabel lingkungan dipaksa: `GIT_CONFIG_NOSYSTEM=1`, `GIT_CONFIG_GLOBAL=/dev/null`, `GIT_EDITOR=true`, `GIT_PAGER=cat`.
  3. Konfigurasi repositori lokal untuk helper-helper tersebut dinetralkan secara deterministik.
- **Status**: Teruji dan lolos 100%.

### F-5: Penolakan Opsi `git diff` Arbitrer dan Vektor GPG/Branch Reset
- **Diagnosis**: `git diff --no-index` dapat membaca file sembarang; `git diff --output=<file>` dapat menulis ke file sembarang; `git commit -S` memicu biner penandatangan GPG; `git checkout -B` dapat me-reset branch lokal.
- **Implementasi**:
  1. `git diff`: Flag `--no-index`, `--output`, `--output=`, dan `--ext-diff` ditolak eksplisit (**Exit 73**).
  2. `git commit`: Flag `-S` dan `--gpg-sign` ditolak (**Exit 73**); commit wajib menyertakan `-m` atau `--message` (**Exit 74**).
  3. `git checkout`: Flag `-B` ditolak eksplisit (**Exit 73/74**).
- **Status**: Teruji dan lolos 100%.

---

## 2. Resolusi Struktural (S1 - S14)

### S-1: Presedensi Konfigurasi Git & Scrubbing Variabel Lingkungan
- Tolak seluruh flag `-c`, `--config`, `--config-env`, `--exec-path` buatan pengguna (EC 73).
- Bersihkan seluruh variabel `GIT_*` dari command dan `os.environ`.
- Suntikkan konfigurasi penegakan deterministik pada setiap panggilan git aman.

### S-2: Matriks Penolakan Argv Lengkap
- `git checkout`: Tolak `.`, `HEAD`, `--`, pathspec, `-f`, `-B`, `--force`, `--discard-changes`.
- `git branch`: Tolak `-d`, `-D`, `-m`, `-M`, `-f`, `--force`, `--delete`, `--move`, `-c`, `-C`.
- `git commit`: Wajib `-m`/`--message`; tolak `-F`, `-t`, `-S`, `--gpg-sign`, `--amend`, `--fixup`, `--squash`.
- Subperintah berbahaya: `clean`, `stash`, `reflog`, `gc`, `filter-branch`, `replace`, `restore`, `switch` ditolak (EC 74).

### S-3: Reposisi Batas Akses Keychain
- Dinyatakan secara lugas bahwa akses Keychain berada di domain user macOS yang sama. Kontrol ini mencegah pencurian berkas statis (`.secret_key` dihapus), bukan isolasi kernel antar-proses pada UID yang sama.

### S-4: Transkrip Lengkap Matriks Uji 64 Kasus dan Sentinel Witness 6 Biner
- Rincian pengujian 64 kasus uji dan sentinel witness pada seluruh 6 modul kontrol biner didokumentasikan di `adversarial-matrix-evidence.md`.

### S-5: Verifikasi Runtime Attestation terhadap Trusted Root
- Biner `t3_dispatch.py` dan `t3_acp_gateway.py` memverifikasi hash SHA-256 seluruh modul biner terhadap root ledger `trusted_root_hashes.json` sebelum memproses panggilan alat agen. Modifikasi apa pun akan memicu abort fail-closed (**Exit 80**).

### S-6: Bukti Kesetaraan Byte (Byte-Equivalence) Antar Repositori
- Repositori lokal `.agents/skills/t3-operational-guardrail/` dan repositori global `agent-skills/skills/t3-operational-guardrail/` diuji kesetaraan byte-nya via `diff -r` dan pencocokan digest SHA-256 100% identik.
