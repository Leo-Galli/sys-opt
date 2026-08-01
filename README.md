<div align="center">

# 🛠️ sys-opt

**Universal Hardware Inspector & Multi-OS Optimizer**

> Inspect your hardware, tune your operating system — in **your language**.  
> Ispeziona il tuo hardware, ottimizza il tuo sistema — **nella tua lingua**.

![Python](https://img.shields.io/badge/Python-3.8%2B-3776AB?logo=python&logoColor=white&style=for-the-badge)
![License](https://img.shields.io/github/license/Leo-Galli/sys-opt?style=for-the-badge)
![Version](https://img.shields.io/badge/version-1.0.0-blueviolet?style=for-the-badge)
![Platforms](https://img.shields.io/badge/Platform-Windows%20%7C%20macOS%20%7C%20Linux-2ea44f?style=for-the-badge)
![Languages](https://img.shields.io/badge/i18n-10%20Languages-brightgreen?style=for-the-badge)
![CLI](https://img.shields.io/badge/CLI-Rich%20Terminal%20UI-cyan?style=for-the-badge)
![Zero Crash](https://img.shields.io/badge/Zero--Crash-Guaranteed-success?style=for-the-badge)

![Stars](https://img.shields.io/github/stars/Leo-Galli/sys-opt?style=for-the-badge&logo=github&color=gold)
![Forks](https://img.shields.io/github/forks/Leo-Galli/sys-opt?style=for-the-badge&logo=github)
![Issues](https://img.shields.io/github/issues/Leo-Galli/sys-opt?style=for-the-badge&logo=github)
![Last commit](https://img.shields.io/github/last-commit/Leo-Galli/sys-opt?style=for-the-badge&logo=github)
![Contributors](https://img.shields.io/github/contributors/Leo-Galli/sys-opt?style=for-the-badge&logo=github)
![Repo size](https://img.shields.io/github/repo-size/Leo-Galli/sys-opt?style=for-the-badge)
![CI](https://img.shields.io/github/actions/workflow/status/Leo-Galli/sys-opt/ci.yml?style=for-the-badge&logo=githubactions&logoColor=white&label=CI)
![PyPI](https://img.shields.io/pypi/v/sys-opt?style=for-the-badge&logo=pypi&logoColor=white)
![PyPI downloads](https://img.shields.io/pypi/dm/sys-opt?style=for-the-badge&logo=pypi&logoColor=white)
![PRs welcome](https://img.shields.io/badge/PRs-Welcome-ff69b4?style=for-the-badge)
![Made with ❤️](https://img.shields.io/badge/Made%20with-%E2%9D%A4%EF%B8%8F-red?style=for-the-badge)

**Repository:** [https://github.com/Leo-Galli/sys-opt](https://github.com/Leo-Galli/sys-opt)

</div>

---

`sys-opt` is a production-grade, **zero-crash** command-line tool that performs a deep **hardware & OS inspection** and a safe, **multi-OS optimization** — fully localized in **10 languages** and automatically adapted to your operating system. No configuration needed: install, run, done.

---

## 📑 Table of Contents

- [✨ Features](#-features)
- [🌍 Supported Languages](#-supported-languages)
- [📦 Installation](#-installation)
  - [⚡ Quick install from GitHub](#-quick-install-from-github)
  - [🐧 Linux](#-linux)
  - [🍎 macOS](#-macos)
  - [🪟 Windows](#-windows)
- [🚀 Usage](#-usage)
  - [Interactive menu](#interactive-menu)
  - [Non-interactive flags](#non-interactive-flags)
  - [🎯 Optimization profiles](#-optimization-profiles)
  - [🔐 Elevation](#-elevation)
  - [What each optimizer step does](#what-each-optimizer-step-does)
- [🗂️ Project Structure](#-project-structure)
- [🧪 Testing](#-testing)
- [🩺 Troubleshooting](#-troubleshooting)
- [❓ FAQ](#-faq)
- [🌐 Quick Start Guides (10 languages)](#-quick-start-guides-10-languages)
- [🚀 Releasing to PyPI](#-releasing-to-pypi)
- [🌙 Nightly Benchmark](#-nightly-benchmark)
- [⚠️ Disclaimer](#-disclaimer)
- [📄 License](#-license)

---

## ✨ Features

**🔍 Hardware & OS Inspector** — clean, rich-formatted tables:

| Section | Details |
|---|---|
| OS & Kernel | Name, build, architecture, hostname, uptime |
| Motherboard / Machine | Manufacturer, product model, serial number |
| CPU | Model, physical cores, logical processors, base & current frequency |
| Memory (RAM) | Total, available, used, usage %, speed (MHz), module count |
| Graphics (GPU) | Integrated & dedicated controllers, VRAM, driver version |
| Storage | Physical drives (NVMe/SSD/HDD), partition layout, size, free space % |

**🚀 Multi-OS Optimizer** (elevation-aware):

| OS | What it does |
|---|---|
| 🪟 Windows 10/11 | Purges `%TEMP%` & `C:\Windows\Temp`, stops/disables `SysMain`/`Superfetch`, activates High/Ultimate Performance plan, flushes DNS (`ipconfig /flushdns`), clears Windows Update cache |
| 🎮 Windows gaming | Enables hardware-accelerated GPU scheduling (HAGS, `HwSchMode=2`) and disables Game DVR / Game Bar background recording to cut capture overhead and smooth frame times *(reboot required — see [FAQ](#-faq))* |
| 🍎 macOS | Clears `~/Library/Caches` & `/Library/Caches`, flushes DNS (`dscacheutil`, `mDNSResponder`), purges inactive memory (`purge`) |
| 🐧 Linux | Cleans `/tmp`, releases kernel memory caches (`drop_caches`), auto-detects the package manager and cleans its cache (`apt clean`, `dnf clean all`, `pacman -Sc`, `zypper clean`, `apk cache clean`) |

**🎯 Optimization profiles** — pick the kind of tune-up you want: Full, Gaming, AI/ML, Studio/Work, or Cleanup-only.

**📊 Performance benchmark** — lightweight CPU / RAM / disk stress tests (psutil-backed) with a comparative trend table, perfect for measuring the effect of your optimization.

**🌐 i18n engine** — 10 complete languages, **zero missing keys** (enforced by tests), automatic locale detection, on-the-fly switching, RTL-aware layout for Arabic.

**🛡️ Zero-crash policy** — every hardware query and OS command is wrapped in `try/except`; unreadable attributes degrade gracefully to `N/A` / `Access Denied` instead of crashing.

**⚡ Rich terminal UI** — tables, panels, spinners, ASCII banner, color-coded statuses.

---

## 🌍 Supported Languages

| # | Code | Language | Direction |
|---|------|----------|-----------|
| 1 | `it` | 🇮🇹 Italiano | LTR |
| 2 | `en` | 🇬🇧 English | LTR |
| 3 | `es` | 🇪🇸 Español | LTR |
| 4 | `fr` | 🇫🇷 Français | LTR |
| 5 | `de` | 🇩🇪 Deutsch | LTR |
| 6 | `pt` | 🇵🇹 Português | LTR |
| 7 | `ru` | 🇷🇺 Русский | LTR |
| 8 | `zh` | 🇨🇳 中文 (Simplified) | LTR |
| 9 | `ja` | 🇯🇵 日本語 | LTR |
| 10 | `ar` | 🇸🇦 العربية | RTL |

**Detection flow:** on startup the host locale is detected automatically and used as the default → you can switch at any time from the menu. Unknown locales and any missing key fall back to English.

---

## 📦 Installation

**Prerequisite:** [Python 3.8+](https://www.python.org/downloads/) on your system.

### ⚡ Quick install from GitHub

```bash
pip install git+https://github.com/Leo-Galli/sys-opt.git
sys-opt              # interactive menu
```

> If `pip` is not on your PATH, use `python -m pip` / `python3 -m pip`. If you run into the Linux `externally-managed-environment` error, use a virtual environment (see below).

### 🐧 Linux

**Debian / Ubuntu:**

```bash
sudo apt update
sudo apt install -y python3 python3-pip python3-venv git
git clone https://github.com/Leo-Galli/sys-opt.git
cd sys-opt
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python -m sys_opt
```

**Fedora / RHEL:**

```bash
sudo dnf install -y python3 python3-pip git
git clone https://github.com/Leo-Galli/sys-opt.git
cd sys-opt
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python -m sys_opt
```

**Arch Linux:**

```bash
sudo pacman -S --needed python python-pip git
git clone https://github.com/Leo-Galli/sys-opt.git
cd sys-opt
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python -m sys_opt
```

**openSUSE:**

```bash
sudo zypper install -y python3 python3-pip git
git clone https://github.com/Leo-Galli/sys-opt.git
cd sys-opt
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python -m sys_opt
```

> 💡 A virtual environment (`.venv`) is **recommended** on modern distros that enable PEP 668 (`externally-managed-environment`), and it keeps your system Python clean.

### 🍎 macOS

```bash
# 1. Install Command Line Tools (opens a GUI prompt the first time)
xcode-select --install

# 2. Clone and install
git clone https://github.com/Leo-Galli/sys-opt.git
cd sys-opt
python3 -m pip install -r requirements.txt

# 3. Run
python3 -m sys_opt
```

> Alternative: `brew install python` (if you use [Homebrew](https://brew.sh/)) then repeat steps 2–3.

### 🪟 Windows

1. **Install Python** from [python.org](https://www.python.org/downloads/) → during setup, tick **“Add python.exe to PATH”**.
2. Open **PowerShell** (or Windows Terminal) and verify:

   ```powershell
   py --version
   ```

3. Clone and install:

   ```powershell
   git clone https://github.com/Leo-Galli/sys-opt.git
   cd sys-opt
   py -m pip install -r requirements.txt
   ```

4. Run:

   ```powershell
   py -m sys_opt
   ```

> For **optimization**, open PowerShell **as Administrator** (right-click → *Run as administrator*) and run `py -m sys_opt --optimize` — see [Elevation](#-elevation).

---

## 🚀 Usage

### Interactive menu

```bash
python -m sys_opt        # or just: sys-opt  (after pip install)
```

```
 ███████╗██╗   ██╗███████╗      ██████╗ ██████╗ ████████╗
 ██╔════╝╚██╗ ██╔╝██╔════╝     ██╔═══██╗██╔═══██╗╚══██╔══╝
 ███████╗ ╚████╔╝ ███████╗     ██║   ██║██║   ██║   ██║
 ╚════██║  ╚██╔╝  ╚════██║     ██║   ██║██║   ██║   ██║
 ███████║   ██║   ███████║     ╚██████╔╝╚██████╔╝   ██║
 ╚══════╝   ╚═╝   ╚══════╝      ╚═════╝  ╚═════╝    ╚═╝ [1] 🔍 Inspect System Specs
 [2] 🚀 Run System Optimization
 [3] ⚡ Full Suite
 [4] 📊 Run Performance Benchmark
 [5] 🌐 Change Language
 [0] 🚪 Exit
```

### Non-interactive flags

| Command | What it does |
|---|---|
| `python -m sys_opt --inspect` | Print the full hardware report |
| `python -m sys_opt --inspect --json` | Emit the report as JSON (scripting) |
| `python -m sys_opt --optimize` | Run the system optimization |
| `python -m sys_opt --optimize --dry-run` | Preview every step, execute nothing |
| `python -m sys_opt --optimize --force` | Skip the elevation confirmation prompt |
| `python -m sys_opt --optimize --profile gaming` | Run a specific profile (see below) |
| `python -m sys_opt --suite` | Inspect **then** optimize |
| `python -m sys_opt --benchmark` | Run a light CPU / RAM / disk benchmark with a comparative table |
| `python -m sys_opt --benchmark --json` | Emit benchmark results as JSON (scripting) |
| `python -m sys_opt --language it --inspect` | Force a specific language (`it`, `en`, `es`, `fr`, `de`, `pt`, `ru`, `zh`, `ja`, `ar`) |
| `python -m sys_opt --list-languages` | List all supported languages |
| `python -m sys_opt --version` | Show the version |

### 🎯 Optimization profiles

Choose what kind of optimization to run — interactively from the menu, or with `--profile <name>`:

| Profile | What it runs | Best for |
|---|---|---|
| `all` · ⚡ Full | Every step for your OS | One-shot complete tune-up |
| `gaming` · 🎮 Gaming | Power plan, GPU scheduling (HAGS), Game DVR off, services, caches | Frame rate / FPS |
| `ai` · 🤖 AI / ML | High performance: power plan, services, caches, kernel memory release | Training & heavy workloads |
| `studio` · 💼 Studio / Work | Light & safe: temp files, DNS, update cache, services | Daily work, no side effects |
| `clean` · 🧹 Cleanup | Just temp files, caches and DNS — no power/service changes | Quick hygiene |

```bash
python -m sys_opt --optimize --profile gaming
python -m sys_opt --suite --profile studio
python -m sys_opt --optimize --profile ai --dry-run
```

### 📊 Performance benchmark

Runs a short, lightweight stress test and shows a comparative table — run it **before** optimizing to get a baseline, then again **after** to see the improvement:

```bash
python -m sys_opt --benchmark
python -m sys_opt --benchmark --json
```

| Measured | What it tests |
|---|---|
| CPU | Floating-point compute loop → millions of operations/sec (`M ops/s`) |
| RAM | Repeated buffer copies → memory bandwidth (`MB/s`) |
| Disk (write) | Writes a temp file with `fsync` → write speed (`MB/s`) |
| Disk (read) | Reads the temp file back → read speed (`MB/s`) |

Each row also shows a relative **trend bar** comparing it against the fastest measured component. All tests are zero-crash and clean up their temp files automatically.

### 🔐 Elevation

Optimization steps that touch system-wide settings need elevated privileges (**Administrator** on Windows, **sudo / root** on macOS & Linux). **Inspection works without them.**

| OS | How to run with elevation |
|---|---|
| 🪟 Windows | Open PowerShell / Terminal **as Administrator** |
| 🍎 macOS | Prefix with `sudo` (`sudo python3 -m sys_opt --optimize`) |
| 🐧 Linux | Prefix with `sudo` (`sudo python -m sys_opt --optimize`) |

When privileges are missing, `sys-opt` shows clear instructions and asks whether to continue; steps that require elevation are then reported as **SKIPPED** instead of failing.

### What each optimizer step does

**🪟 Windows 10/11 (7 steps):**

| Step | Detail | Elevation |
|---|---|---|
| Purge temporary files | Empties `%TEMP%` and `C:\Windows\Temp` (locked files skipped safely) | no |
| Disable background services | Stops and disables `SysMain` / `Superfetch` (frees RAM & disk I/O) | yes |
| High Performance power plan | Activates High Performance; creates Ultimate Performance if missing | no |
| Enable GPU scheduling (HAGS) | `HwSchMode=2` — offloads scheduling to the GPU, less CPU overhead in games (**reboot required**) | yes |
| Disable Game DVR / Game Bar | Removes background-recording overhead while gaming | no |
| Flush DNS cache | `ipconfig /flushdns` | no |
| Clear Windows Update cache | Empties `C:\Windows\SoftwareDistribution\Download` | yes |

**🍎 macOS (3 steps):**

| Step | Detail | Elevation |
|---|---|---|
| Clear system caches | `~/Library/Caches` and `/Library/Caches` | system part: yes |
| Flush DNS cache | `dscacheutil -flushcache` + `killall -HUP mDNSResponder` | no |
| Purge inactive memory | `purge` | yes |

**🐧 Linux (3 steps):**

| Step | Detail | Elevation |
|---|---|---|
| Clean `/tmp` | Best-effort removal of temporary files | no |
| Release kernel caches | Writes `3` to `/proc/sys/vm/drop_caches` | yes |
| Clean package-manager cache | Auto-detects: `apt clean` · `dnf clean all` · `pacman -Sc` · `zypper clean` · `apk cache clean` | yes |

---

## 🗂️ Project Structure

```
sys-opt/
├── .flake8
├── .gitignore
├── .github/workflows/
│   ├── ci.yml                  # lint + tests on Windows / macOS / Linux
│   ├── release.yml             # publish to PyPI on every v* tag
│   └── nightly-benchmark.yml   # nightly CPU/RAM/disk benchmark + report
├── .github/scripts/
│   └── update_benchmarks.py    # merge nightly results into benchmarks/
├── benchmarks/
│   ├── <os>.json               # full benchmark history per OS
│   └── report.md               # regenerated comparative report
├── LICENSE
├── README.md
├── requirements.txt
├── pyproject.toml
├── tests/
│   ├── test_i18n.py        # zero-missing-keys guarantee across 10 languages
│   ├── test_utils.py       # formatting helpers & safe subprocess
│   ├── test_inspector.py   # live inspection on the current host
│   └── test_optimizer.py   # dry-run optimizer safety + profile filtering
└── sys_opt/
    ├── __init__.py
    ├── __main__.py         # allows `python -m sys_opt`
    ├── main.py             # CLI flags + interactive menu + locale detection
    ├── inspector.py        # hardware & OS inspection (zero-crash)
    ├── optimizer.py        # multi-OS optimization engine + profiles
    ├── utils.py            # safe subprocess / elevation / formatting
    └── i18n/
        ├── __init__.py
        └── languages.py    # complete dictionaries for 10+ languages
```

---

## 🧪 Testing

```bash
python -m unittest discover -s tests -v
```

The suite (26 tests) asserts: identical key sets across all 10 languages, English fallback, formatting helpers, safe subprocess handling, live inspection on the current host, dry-run optimizer safety, profile-based step filtering, and benchmark measurements with JSON output.

**CI (GitHub Actions):** every push / pull request runs `actionlint` (workflow syntax) + `flake8` lint plus the full test suite on a **complete OS × Python matrix** — Ubuntu 22.04/24.04 (x86_64) & 24.04 (arm64), macOS 15 (Intel) & 14 (Apple Silicon), Windows Server 2022 & 2025, across Python **3.8 → 3.14** — plus an independent **packaging job per OS** (Linux, macOS, Windows) that builds the sdist/wheel, validates with `twine check` and smoke-tests a clean install, so a packaging failure on one OS never hides the others — see [.github/workflows/ci.yml](.github/workflows/ci.yml).

---

## 🩺 Troubleshooting

| Problem | Fix |
|---|---|
| `'sys-opt' is not recognized as a command` | Use `python -m sys_opt` / `py -m sys_opt`, or install with `pip install -e .` |
| `'pip' is not recognized` (Windows) | Use `py -m pip ...`; make sure Python was added to PATH |
| `error: externally-managed-environment` (Linux) | Create a venv: `python3 -m venv .venv && source .venv/bin/activate` |
| `Permission denied` during optimization | Run with elevation (see [Elevation](#-elevation)) |
| Steps show `SKIPPED (needs elevation)` | Relaunch with Administrator / sudo — that's expected behavior |
| Emoji look odd in the terminal | Use Windows Terminal, or run `chcp 65001`; `sys-opt` forces UTF-8 output |

---

## ❓ FAQ

**Is it safe?** It only cleans caches/temp files and adjusts documented Windows services, power plans and registry tweaks. It never touches personal documents, and every step reports its own success/failure.

**Does it need Administrator / sudo?** Only for the optimization steps marked as elevated. Inspection works everywhere.

**Do I need to reboot after optimizing?** The HAGS (GPU scheduling) step takes effect after a **reboot** — the tool tells you when that applies. To revert it, delete `HwSchMode` under `HKLM\SYSTEM\CurrentControlSet\Control\GraphicsDrivers` or set it back to `0`.

**Does it really improve FPS?** The gaming tweaks (HAGS, Game DVR off, High Performance plan) remove known sources of CPU/GPU overhead — the gains vary by game and hardware, and mostly show up on CPU-bound titles.

**Which languages are supported?** 10: Italian, English, Spanish, French, German, Portuguese, Russian, Chinese (Simplified), Japanese, Arabic (RTL).

**How do I change the language?** Menu → `[4] 🌐 Change Language`, or pass `--language <code>`.

**How do I choose what to optimize?** The menu asks for an **optimization profile** (Gaming, AI, Studio, Cleanup or Full) whenever you pick *Run System Optimization* or *Full Suite*; from the CLI use `--profile <name>`.

---

## 🌐 Quick Start Guides (10 languages)

Pick your language — every guide expands inline (click the flag):

| Flag | Language | Jump |
|---|---|---|
| 🇮🇹 | Italiano | [→ guide](#guide-it) |
| 🇬🇧 | English | [→ guide](#guide-en) |
| 🇪🇸 | Español | [→ guide](#guide-es) |
| 🇫🇷 | Français | [→ guide](#guide-fr) |
| 🇩🇪 | Deutsch | [→ guide](#guide-de) |
| 🇵🇹 | Português | [→ guide](#guide-pt) |
| 🇷🇺 | Русский | [→ guide](#guide-ru) |
| 🇨🇳 | 中文 | [→ guide](#guide-zh) |
| 🇯🇵 | 日本語 | [→ guide](#guide-ja) |
| 🇸🇦 | العربية | [→ guide](#guide-ar) |

<details id="guide-it">
<summary><b>🇮🇹 Italiano</b> — Guida rapida</summary>

```bash
git clone https://github.com/Leo-Galli/sys-opt.git
cd sys-opt
pip install -r requirements.txt        # Windows: py -m pip install -r requirements.txt
python -m sys_opt                      # apri il menu interattivo
python -m sys_opt --inspect            # mostra le specifiche hardware
python -m sys_opt --optimize           # ottimizza il sistema (da Amministratore / con sudo)
python -m sys_opt --optimize --dry-run # anteprima senza applicare nulla
python -m sys_opt --optimize --profile gaming  # profilo Gaming: tweak FPS (HAGS + Game DVR)
```

> 💡 L'ottimizzatore Windows include i tweak **FPS**: pianificazione GPU accelerata via hardware (HAGS) e disattivazione della registrazione in background di Game DVR — il riavvio applica le modifiche.

</details>

<details id="guide-en">
<summary><b>🇬🇧 English</b> — Quick start</summary>

```bash
git clone https://github.com/Leo-Galli/sys-opt.git
cd sys-opt
pip install -r requirements.txt
python -m sys_opt                      # open the interactive menu
python -m sys_opt --inspect            # show the hardware report
python -m sys_opt --optimize           # optimize the system (Administrator / sudo)
python -m sys_opt --optimize --dry-run # preview without applying anything
python -m sys_opt --optimize --profile gaming  # Gaming profile: FPS tweaks (HAGS + Game DVR)
```

> 💡 The Windows optimizer includes **FPS** tweaks: hardware-accelerated GPU scheduling (HAGS) and disabling Game DVR background recording — a reboot applies the changes.

</details>

<details id="guide-es">
<summary><b>🇪🇸 Español</b> — Guía rápida</summary>

```bash
git clone https://github.com/Leo-Galli/sys-opt.git
cd sys-opt
pip install -r requirements.txt
python -m sys_opt                      # abre el menú interactivo
python -m sys_opt --inspect            # muestra las especificaciones del hardware
python -m sys_opt --optimize           # optimiza el sistema (Administrador / sudo)
python -m sys_opt --optimize --dry-run # vista previa sin aplicar nada
python -m sys_opt --optimize --profile gaming  # perfil Gaming: mejoras FPS (HAGS + Game DVR)
```

> 💡 El optimizador de Windows incluye mejoras **FPS**: programación de GPU acelerada por hardware (HAGS) y desactivación de la grabación en segundo plano de Game DVR — un reinicio aplica los cambios.

</details>

<details id="guide-fr">
<summary><b>🇫🇷 Français</b> — Guide rapide</summary>

```bash
git clone https://github.com/Leo-Galli/sys-opt.git
cd sys-opt
pip install -r requirements.txt
python -m sys_opt                      # ouvre le menu interactif
python -m sys_opt --inspect            # affiche les spécifications matérielles
python -m sys_opt --optimize           # optimise le système (Administrateur / sudo)
python -m sys_opt --optimize --dry-run # aperçu sans rien appliquer
python -m sys_opt --optimize --profile gaming  # profil Gaming : réglages FPS (HAGS + Game DVR)
```

> 💡 L'optimiseur Windows inclut des réglages **FPS** : planification GPU accélérée par le matériel (HAGS) et désactivation de l'enregistrement en arrière-plan de Game DVR — un redémarrage applique les changements.

</details>

<details id="guide-de">
<summary><b>🇩🇪 Deutsch</b> — Schnellstart</summary>

```bash
git clone https://github.com/Leo-Galli/sys-opt.git
cd sys-opt
pip install -r requirements.txt
python -m sys_opt                      # interaktives Menü öffnen
python -m sys_opt --inspect            # Hardware-Report anzeigen
python -m sys_opt --optimize           # System optimieren (Administrator / sudo)
python -m sys_opt --optimize --dry-run # Vorschau ohne Änderungen
python -m sys_opt --optimize --profile gaming  # Gaming-Profil: FPS-Tweaks (HAGS + Game DVR)
```

> 💡 Der Windows-Optimierer enthält **FPS**-Tweaks: hardwarebeschleunigte GPU-Planung (HAGS) und Deaktivierung der Game-DVR-Hintergrundaufnahme — ein Neustart wendet die Änderungen an.

</details>

<details id="guide-pt">
<summary><b>🇵🇹 Português</b> — Guia rápido</summary>

```bash
git clone https://github.com/Leo-Galli/sys-opt.git
cd sys-opt
pip install -r requirements.txt
python -m sys_opt                      # abre o menu interativo
python -m sys_opt --inspect            # mostra as especificações do hardware
python -m sys_opt --optimize           # otimiza o sistema (Administrador / sudo)
python -m sys_opt --optimize --dry-run # pré-visualização sem aplicar nada
python -m sys_opt --optimize --profile gaming  # perfil Gaming: ajustes FPS (HAGS + Game DVR)
```

> 💡 O otimizador do Windows inclui ajustes de **FPS**: agendamento de GPU acelerado por hardware (HAGS) e desativação da gravação em segundo plano do Game DVR — um reinício aplica as alterações.

</details>

<details id="guide-ru">
<summary><b>🇷🇺 Русский</b> — Быстрый старт</summary>

```bash
git clone https://github.com/Leo-Galli/sys-opt.git
cd sys-opt
pip install -r requirements.txt
python -m sys_opt                      # открыть интерактивное меню
python -m sys_opt --inspect            # показать характеристики железа
python -m sys_opt --optimize           # оптимизировать систему (Администратор / sudo)
python -m sys_opt --optimize --dry-run # предпросмотр без применения
python -m sys_opt --optimize --profile gaming  # профиль Gaming: настройки FPS (HAGS + Game DVR)
```

> 💡 Оптимизатор Windows включает настройки **FPS**: аппаратное планирование GPU (HAGS) и отключение фоновой записи Game DVR — перезагрузка применяет изменения.

</details>

<details id="guide-zh">
<summary><b>🇨🇳 中文</b> — 快速入门</summary>

```bash
git clone https://github.com/Leo-Galli/sys-opt.git
cd sys-opt
pip install -r requirements.txt
python -m sys_opt                      # 打开交互式菜单
python -m sys_opt --inspect            # 显示硬件规格
python -m sys_opt --optimize           # 优化系统（管理员 / sudo）
python -m sys_opt --optimize --dry-run # 预览，不实际执行
python -m sys_opt --optimize --profile gaming  # 游戏配置：FPS 优化（HAGS + Game DVR）
```

> 💡 Windows 优化器包含 **FPS** 调整：硬件加速 GPU 计划 (HAGS) 和禁用 Game DVR 后台录制 — 重启后生效。

</details>

<details id="guide-ja">
<summary><b>🇯🇵 日本語</b> — クイックスタート</summary>

```bash
git clone https://github.com/Leo-Galli/sys-opt.git
cd sys-opt
pip install -r requirements.txt
python -m sys_opt                      # 対話式メニューを開く
python -m sys_opt --inspect            # ハードウェア情報を表示
python -m sys_opt --optimize           # システムを最適化（管理者 / sudo）
python -m sys_opt --optimize --dry-run # プレビュー（変更は適用しない）
python -m sys_opt --optimize --profile gaming  # ゲーミング設定：FPS調整（HAGS + Game DVR）
```

> 💡 Windows オプティマイザーには **FPS** 調整が含まれます：ハードウェアアクセラレーション GPU スケジューリング (HAGS) と Game DVR のバックグラウンド録画の無効化 — 再起動で変更が適用されます。

</details>

<details id="guide-ar">
<summary><b>🇸🇦 العربية</b> — دليل سريع (RTL)</summary>

<div dir="rtl">

```bash
git clone https://github.com/Leo-Galli/sys-opt.git
cd sys-opt
pip install -r requirements.txt
python -m sys_opt                      # افتح القائمة التفاعلية
python -m sys_opt --inspect            # اعرض مواصفات الجهاز
python -m sys_opt --optimize           # حسّن النظام (مدير / sudo)
python -m sys_opt --optimize --dry-run # معاينة دون تطبيق أي تغيير
python -m sys_opt --optimize --profile gaming  # ملف الألعاب: تحسينات FPS (HAGS + Game DVR)
```

> 💡 يتضمن مُحسِّن Windows تحسينات **FPS**: جدولة GPU المسرَّعة بالعتاد (HAGS) وتعطيل التسجيل الخلفي لـ Game DVR — أعد التشغيل لتطبيق التغييرات.

</div>

</details>

---

## 🚀 Releasing to PyPI

The package is published automatically by [GitHub Actions](.github/workflows/release.yml) whenever you push a **tag** matching `v*`:

```bash
git tag v1.1.0
# bump the version in pyproject.toml first, then:
git push origin v1.1.0
```

The workflow builds the sdist + wheel, validates them with `twine check`, and publishes using **trusted publishing (OIDC)** — no API token stored in the repo. To enable it, register the PyPI project **`sys-opt`** as a trusted publisher pointing at `Leo-Galli/sys-opt` (workflow `release.yml`, environment `release`). After the first release, the `PyPI` badges above light up and anyone can `pip install sys-opt`.

---

## 🌙 Nightly Benchmark

Every night at **03:00 UTC** (and on demand via **Actions → Nightly Benchmark → Run workflow**), [GitHub Actions](.github/workflows/nightly-benchmark.yml) runs the built-in `--benchmark` (light CPU / RAM / disk stress via `psutil`) on **one GitHub-hosted runner per OS**:

- 🐧 **Linux** — `ubuntu-24.04`
- 🍎 **macOS** — `macos-14` (Apple Silicon)
- 🪟 **Windows** — `windows-2022`

Each run is appended to the history file `benchmarks/<os>.json` (last 365 runs kept) and `benchmarks/report.md` is regenerated with a **comparative table of the latest run per OS** plus the recent history — so you can watch performance drift over time (e.g. after a Windows update or a driver change). The report is also printed into the Actions run summary.

**Run it manually:**

```bash
gh workflow run nightly-benchmark.yml
```

Because only `benchmarks/**` changes, the main CI matrix is automatically skipped for these commits (`paths-ignore`), so nightly runs never waste the 44 CI jobs.

---

## ⚠️ Disclaimer

Optimization modifies system settings and deletes temporary files. Use with care — the tool never touches personal documents, but it does clean caches and adjust services/power plans. Always run optimization with the required privileges and reboot when prompted.

## 📄 License

[MIT](LICENSE) © Leo-Galli
