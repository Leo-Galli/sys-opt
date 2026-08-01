<div align="center">

# 🛠️ sys-opt

**Universal Hardware Inspector & Multi-OS Optimizer**

> Inspect your hardware, tune your operating system, in your language.
> Ispeziona il tuo hardware, ottimizza il tuo sistema operativo, nella tua lingua.

[![Python](https://img.shields.io/badge/Python-3.8%2B-3776AB?logo=python&logoColor=white)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/License-MIT-blue.svg)](#-license)
[![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20macOS%20%7C%20Linux-lightgrey)](#-installation)
[![Languages](https://img.shields.io/badge/%F0%9F%8C%8D-10%20Languages-brightgreen)](#-supported-languages)
[![CLI](https://img.shields.io/badge/CLI-Rich%20Terminal%20UI-cyan)](#-usage)

**Repository:** [https://github.com/Leo-Galli/sys-opt](https://github.com/Leo-Galli/sys-opt)

</div>

---

`sys-opt` is a production-grade, **zero-crash** command-line tool that performs a deep **hardware & OS inspection** and a safe, **multi-OS optimization** — fully localized in **10 languages** and automatically adapted to your operating system. No configuration needed: install, run, done.

---

## 📑 Table of Contents

- [✨ Features](#-features)
- [🌍 Supported Languages](#-supported-languages)
- [📦 Installation](#-installation)
  - [🐧 Linux](#-linux)
  - [🍎 macOS](#-macos)
  - [🪟 Windows](#-windows)
- [🚀 Usage](#-usage)
  - [Interactive menu](#interactive-menu)
  - [Non-interactive flags](#non-interactive-flags)
  - [🔐 Elevation](#-elevation)
  - [What each optimizer step does](#what-each-optimizer-step-does)
- [🗂️ Project Structure](#-project-structure)
- [🧪 Testing](#-testing)
- [🩺 Troubleshooting](#-troubleshooting)
- [❓ FAQ](#-faq)
- [🇮🇹 Guida rapida in italiano](#-guida-rapida-in-italiano)
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

### Quick — from GitHub (all OS)

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
 ╚══════╝   ╚═╝   ╚══════╝      ╚═════╝  ╚═════╝    ╚═╝

[1] 🔍 Inspect System Specs
[2] 🚀 Run System Optimization
[3] ⚡ Full Suite
[4] 🌐 Change Language
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
├── .gitignore
├── README.md
├── requirements.txt
├── pyproject.toml
├── tests/
│   ├── test_i18n.py        # zero-missing-keys guarantee across 10 languages
│   ├── test_utils.py       # formatting helpers & safe subprocess
│   ├── test_inspector.py   # live inspection on the current host
│   └── test_optimizer.py   # dry-run optimizer safety
└── sys_opt/
    ├── __init__.py
    ├── __main__.py         # allows `python -m sys_opt`
    ├── main.py             # CLI flags + interactive menu + locale detection
    ├── inspector.py        # hardware & OS inspection (zero-crash)
    ├── optimizer.py        # multi-OS optimization engine
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

The suite (18 tests) asserts: identical key sets across all 10 languages, English fallback, formatting helpers, safe subprocess handling, live inspection on the current host, and dry-run optimizer safety.

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

## 🇮🇹 Guida rapida in italiano

```bash
git clone https://github.com/Leo-Galli/sys-opt.git
cd sys-opt
pip install -r requirements.txt        # (Windows: py -m pip install -r requirements.txt)
python -m sys_opt                      # apri il menu interattivo
python -m sys_opt --inspect            # mostra le specifiche hardware
python -m sys_opt --optimize           # ottimizza il sistema (da Amministratore / con sudo)
python -m sys_opt --optimize --dry-run # anteprima senza applicare nulla
```

L'ottimizzatore Windows include i tweak **FPS**: pianificazione GPU accelerata via hardware (HAGS) e disattivazione della registrazione in background di Game DVR — il riavvio applica le modifiche.

---

## ⚠️ Disclaimer

Optimization modifies system settings and deletes temporary files. Use with care — the tool never touches personal documents, but it does clean caches and adjust services/power plans. Always run optimization with the required privileges and reboot when prompted.

## 📄 License

[MIT](LICENSE) © Leo-Galli
