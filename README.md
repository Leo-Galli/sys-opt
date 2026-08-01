# 🛠️ sys-opt — Universal Hardware Inspector & Multi-OS Optimizer

> Inspect your hardware, tune your operating system, in your language. · Ispeziona il tuo hardware, ottimizza il tuo sistema operativo, nella tua lingua.

`sys-opt` is a production-grade, zero-crash CLI that performs a deep **hardware & OS inspection** and a safe **multi-OS optimization** — fully localized in **10 languages**, auto-detected from your system.

---

## 🔗 GitHub & Quick Start

**Repository:** [github.com/Leo-Galli/sys-opt](https://github.com/Leo-Galli/sys-opt)

```bash
# 1. Clone
$ git clone https://github.com/Leo-Galli/sys-opt.git
$ cd sys-opt

# 2. Install dependencies
$ pip install -r requirements.txt

# 3. Run it!
$ python -m sys_opt
```

Or install the package directly from GitHub (adds the `sys-opt` command to your PATH):

```bash
$ pip install git+https://github.com/Leo-Galli/sys-opt.git
$ sys-opt --inspect
```

### 🇮🇹 Guida rapida

```bash
git clone https://github.com/Leo-Galli/sys-opt.git
cd sys-opt
pip install -r requirements.txt
python -m sys_opt                 # apri il menu interattivo
python -m sys_opt --optimize      # ottimizza il sistema (da Amministratore / sudo)
python -m sys_opt --inspect       # mostra le specifiche hardware
```

---

## ✨ Features

- **🔍 Hardware & OS Inspector** — clean, rich-formatted tables:
  - OS & Kernel: name, build, architecture, hostname, uptime
  - Motherboard / Machine: manufacturer, product model, serial number
  - CPU: model, physical cores, logical processors, base & current frequency
  - RAM: total, available, used, usage %, speed (MHz), module count
  - GPU: integrated & dedicated controllers, VRAM, driver version
  - Storage: physical drives (NVMe/SSD/HDD), partition layout, size, free space %
- **🚀 Multi-OS Optimizer** (elevation-aware):
  - **Windows 10/11:** purge `%TEMP%` & `C:\Windows\Temp`, stop/disable `SysMain`/`Superfetch`, activate High/Ultimate Performance plan, `ipconfig /flushdns`, clear Windows Update cache
  - **🎮 FPS / gaming tweaks (Windows):** enable hardware-accelerated GPU scheduling (HAGS) and disable Game DVR / Game Bar background recording to cut capture overhead and smooth frame times *(HAGS takes effect after a reboot; revert by deleting `HwSchMode` under `HKLM\SYSTEM\CurrentControlSet\Control\GraphicsDrivers` or setting it back to `0`)*
  - **macOS:** clear `~/Library/Caches` & `/Library/Caches`, flush DNS (`dscacheutil`, `mDNSResponder`), `purge` inactive memory
  - **Linux:** clean `/tmp`, release kernel memory caches (`drop_caches`), auto-detect package manager (`apt clean`, `dnf clean all`, `pacman -Sc`, `zypper clean`, `apk cache clean`)
- **🌐 i18n engine** with 10 languages, zero missing keys, automatic locale detection, on-the-fly switching (RTL-aware for Arabic)
- **🛡️ Zero-crash policy** — every hardware query and OS command is wrapped in `try/except`; unreadable attributes degrade to `N/A` / `Access Denied`
- **⚡ Rich terminal UI** — tables, panels, spinners, color-coded statuses

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

**Detection flow:** the host locale is detected on startup → defaults to it → the interactive menu lets you switch at any time. Unknown locales fall back to English; any missing key falls back to English at runtime.

## 📦 Installation

Requires **Python 3.8+**. Pick one of the three options below.

### Option A — Install directly from GitHub (recommended)

```bash
pip install git+https://github.com/Leo-Galli/sys-opt.git
```

This installs the package **and** adds the `sys-opt` command to your PATH:

```bash
sys-opt                 # interactive menu
sys-opt --inspect       # hardware report
sys-opt --optimize      # system optimization (elevation required)
```

### Option B — Clone & run from source

```bash
git clone https://github.com/Leo-Galli/sys-opt.git
cd sys-opt
pip install -r requirements.txt
python -m sys_opt
```

### Option C — Editable install (for development)

```bash
git clone https://github.com/Leo-Galli/sys-opt.git
cd sys-opt
pip install -e .
```

## 🚀 Usage

Run interactively and choose an action from the menu:

```bash
python -m sys_opt        # or just: sys-opt
```

```
[1] 🔍 Inspect System Specs
[2] 🚀 Run System Optimization
[3] ⚡ Full Suite
[4] 🌐 Change Language
[0] 🚪 Exit
```

### ▶️ Example session

```bash
$ python -m sys_opt

[1] 🔍 Inspect System Specs
[2] 🚀 Run System Optimization
[3] ⚡ Full Suite
[4] 🌐 Change Language
[0] 🚪 Exit
Select an action [0-4]: 1

┌──────────────────────────────────────────────┐
│ System Inspection                            │
└──────────────────────────────────────────────┘
Operating System & Kernel   Windows 11 · 10.0.26200 · AMD64
CPU                         6 cores / 12 threads
Memory (RAM)                13.74 GiB total · 5600 MHz
Graphics (GPU)              NVIDIA GeForce ...
Storage                     NVMe 512 GB · 1.23 TiB free
```

Non-interactive flags:

```bash
python -m sys_opt --inspect                 # print the hardware report
python -m sys_opt --inspect --json          # report as JSON (scripting)
python -m sys_opt --optimize                # run optimization (elevation required)
python -m sys_opt --optimize --dry-run      # preview steps, execute nothing
python -m sys_opt --optimize --force        # skip the elevation confirmation
python -m sys_opt --suite                   # inspect + optimize
python -m sys_opt --language it --inspect   # force a language
python -m sys_opt --list-languages          # list supported languages
```

### 🔐 Elevation

- Windows: run as **Administrator**
- macOS / Linux: run with **sudo** or as **root**

When privileges are missing the tool warns you, shows instructions, and asks whether to continue (steps that need elevation are then reported as *SKIPPED*).

## 🗂️ Project Structure

```
sys-opt/
├── .gitignore
├── README.md
├── requirements.txt
├── pyproject.toml
├── tests/
│   ├── test_i18n.py
│   ├── test_utils.py
│   ├── test_inspector.py
│   └── test_optimizer.py
└── sys_opt/
    ├── __init__.py
    ├── __main__.py
    ├── main.py        # CLI + interactive menu
    ├── inspector.py   # hardware & OS inspection
    ├── optimizer.py   # multi-OS optimization engine
    ├── utils.py       # safe subprocess / elevation / locale / formatting
    └── i18n/
        ├── __init__.py
        └── languages.py  # complete dictionaries for 10+ languages
```

## 🧪 Testing

```bash
python -m unittest discover -s tests -v
```

The suite asserts: identical key sets across all 10 languages (zero missing keys), English fallback, formatting helpers, safe subprocess handling, live inspection on the current host, and dry-run optimizer safety.

## ⚠️ Disclaimer

Optimization modifies system settings and deletes temporary files. Use with care — the tool never touches personal documents, but it does clean caches and adjust services/power plans.

## 📄 License

MIT
