# 🛠️ sys-opt — Universal Hardware Inspector & Multi-OS Optimizer

> Inspect your hardware, tune your operating system, in your language. · Ispeziona il tuo hardware, ottimizza il tuo sistema operativo, nella tua lingua.

`sys-opt` is a production-grade, zero-crash CLI that performs a deep **hardware & OS inspection** and a safe **multi-OS optimization** — fully localized in **10 languages**, auto-detected from your system.

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
  - **🎮 FPS / gaming tweaks (Windows):** enable hardware-accelerated GPU scheduling (HAGS) and disable Game DVR / Game Bar background recording to cut capture overhead and smooth frame times
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

Requires **Python 3.8+**.

```bash
pip install -r requirements.txt
# or, install the package itself (adds the `sys-opt` command):
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
