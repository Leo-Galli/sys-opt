# -*- coding: utf-8 -*-
"""
Hardware & operating-system inspector.

Zero-crash policy: every hardware query is wrapped in try/except and degrades
to "N/A" / "Access Denied" instead of raising. Cross-platform: Windows,
macOS and Linux.
"""

import glob
import json
import os
import platform
import re
import shutil
import socket
import sys

try:
    import psutil
except Exception:  # pragma: no cover - optional dependency
    psutil = None

from rich import box
from rich.json import JSON
from rich.panel import Panel
from rich.table import Table

from .utils import format_bytes, format_freq, format_uptime, get_uptime, run_cmd


# --------------------------------------------------------------------------- #
# Parsing helpers
# --------------------------------------------------------------------------- #
def _parse_ps_blocks(text):
    """Parse PowerShell 'Format-List' output into a list of dict blocks."""
    blocks = []
    current = {}
    for line in (text or "").splitlines():
        stripped = line.strip()
        if not stripped:
            if current:
                blocks.append(current)
                current = {}
            continue
        if ":" in stripped:
            key, _, value = stripped.partition(":")
            current[key.strip().lower()] = value.strip()
    if current:
        blocks.append(current)
    return blocks


def _parse_colon_lines(text):
    """Parse 'Key: value' lines into a dict (last occurrence wins)."""
    result = {}
    for line in (text or "").splitlines():
        if ":" in line:
            key, _, value = line.partition(":")
            result[key.strip().lower()] = value.strip()
    return result


def _read_sysfs(path):
    """Read a /sys file; None when missing, 'ACCESS_DENIED' when unreadable."""
    if not os.path.exists(path):
        return None
    try:
        with open(path, "r", encoding="utf-8", errors="replace") as handle:
            value = handle.read().strip()
        return value or None
    except (PermissionError, OSError):
        return "ACCESS_DENIED"


# --------------------------------------------------------------------------- #
# OS
# --------------------------------------------------------------------------- #
def inspect_os_section():
    """Return OS & kernel rows as (i18n_key, value) pairs."""
    system = platform.system()
    name = system or "N/A"
    build = "N/A"
    if system == "Windows":
        try:
            release, ver, _csd, _ptype = platform.win32_ver()
            build_num = 0
            try:
                build_num = int(str(ver).split(".")[-1])
            except Exception:
                pass
            if build_num >= 22000:
                name = "Windows 11"
            elif release:
                name = "Windows %s" % release
            else:
                name = "Windows"
            build = ver or "N/A"
        except Exception:
            build = platform.version() or "N/A"
    elif system == "Linux":
        name = "Linux"
        try:
            with open("/etc/os-release", "r", encoding="utf-8", errors="replace") as handle:
                for line in handle:
                    if line.startswith("PRETTY_NAME="):
                        name = line.split("=", 1)[1].strip().strip('"')
                        break
        except Exception:
            pass
        build = platform.release() or "N/A"
    elif system == "Darwin":
        try:
            mac_version = platform.mac_ver()[0]
            name = "macOS %s" % mac_version if mac_version else "macOS"
        except Exception:
            name = "macOS"
        build = platform.release() or "N/A"
    return [
        ("label_os", name),
        ("label_build", build),
        ("label_arch", platform.machine() or "N/A"),
        ("label_hostname", socket.gethostname() or "N/A"),
        ("label_uptime", format_uptime(get_uptime())),
    ]


# --------------------------------------------------------------------------- #
# Motherboard
# --------------------------------------------------------------------------- #
def inspect_motherboard_section():
    """Return motherboard rows as (i18n_key, value) pairs."""
    try:
        if os.name == "nt":
            rc, out, _err = run_cmd(
                [
                    "powershell",
                    "-NoProfile",
                    "-NonInteractive",
                    "-Command",
                    "Get-CimInstance Win32_BaseBoard | Select-Object Manufacturer,Product,SerialNumber | Format-List",
                ],
                timeout=30,
            )
            parsed = _parse_ps_blocks(out)
            if parsed:
                block = parsed[0]
                return _mb_rows(
                    block.get("manufacturer"), block.get("product"), block.get("serialnumber")
                )
            rc, out, _err = run_cmd(
                ["wmic", "baseboard", "get", "Manufacturer,Product,SerialNumber"], timeout=30
            )
            values = _parse_wmic_row(out)
            return _mb_rows(*values)
        if sys.platform.startswith("linux"):
            vendor = _read_sysfs("/sys/class/dmi/id/board_vendor")
            product = _read_sysfs("/sys/class/dmi/id/board_name")
            serial = _read_sysfs("/sys/class/dmi/id/board_serial")
            if not vendor and not product:
                vendor = _read_sysfs("/sys/class/dmi/id/sys_vendor")
                product = _read_sysfs("/sys/class/dmi/id/product_name")
            return _mb_rows(vendor, product, serial)
        if sys.platform == "darwin":
            rc, out, _err = run_cmd(["system_profiler", "SPHardwareDataType"], timeout=40)
            parsed = _parse_colon_lines(out)
            model = parsed.get("model identifier") or parsed.get("model name")
            serial = parsed.get("serial number (system)") or parsed.get("serial")
            return _mb_rows("Apple Inc.", model, serial)
    except Exception:
        pass
    return _mb_rows(None, None, None)


def _parse_wmic_row(out):
    """Parse a single wmic CSV-ish line split on 2+ spaces."""
    for line in (out or "").splitlines():
        stripped = line.strip()
        if not stripped or stripped.lower().startswith("manufacturer"):
            continue
        parts = re.split(r"\s{2,}", stripped)
        if len(parts) >= 3:
            return parts[0], parts[1], parts[2]
    return None, None, None


def _mb_rows(manufacturer, product, serial):
    return [
        ("label_manufacturer", manufacturer),
        ("label_product", product),
        ("label_serial", serial),
    ]


# --------------------------------------------------------------------------- #
# CPU
# --------------------------------------------------------------------------- #
def inspect_cpu_section():
    """Return CPU rows as (i18n_key, value) pairs."""
    model = "N/A"
    try:
        model = _cpu_model()
    except Exception:
        pass
    cores = "N/A"
    threads = "N/A"
    base = "N/A"
    current = "N/A"
    if psutil is not None:
        try:
            logical = psutil.cpu_count(logical=True)
            physical = psutil.cpu_count(logical=False)
            threads = str(logical) if logical else "N/A"
            cores = str(physical) if physical else "N/A"
        except Exception:
            pass
        try:
            freq = psutil.cpu_freq()
            if freq:
                base = format_freq(freq.base * 1e6) if freq.base else "N/A"
                current = format_freq(freq.current * 1e6) if freq.current else "N/A"
        except Exception:
            pass
    else:
        try:
            threads = str(os.cpu_count()) if os.cpu_count() else "N/A"
        except Exception:
            pass
    return [
        ("label_model", model),
        ("label_cores", cores),
        ("label_threads", threads),
        ("label_base_freq", base),
        ("label_cur_freq", current),
    ]


def _cpu_model():
    try:
        if os.name == "nt":
            rc, out, _err = run_cmd(["wmic", "cpu", "get", "name"], timeout=20)
            if rc == 0:
                for line in out.splitlines():
                    stripped = line.strip()
                    if stripped and not stripped.lower().startswith("name"):
                        return stripped
            return platform.processor() or "N/A"
        if sys.platform == "darwin":
            rc, out, _err = run_cmd(["sysctl", "-n", "machdep.cpu.brand_string"], timeout=15)
            return out or platform.processor() or "N/A"
        with open("/proc/cpuinfo", "r", encoding="utf-8", errors="replace") as handle:
            for line in handle:
                if line.lower().startswith("model name"):
                    return line.split(":", 1)[1].strip()
        return platform.processor() or "N/A"
    except Exception:
        return "N/A"


# --------------------------------------------------------------------------- #
# RAM
# --------------------------------------------------------------------------- #
def inspect_ram_section():
    """Return RAM rows as (i18n_key, value) pairs."""
    total = available = used = percent = "N/A"
    if psutil is not None:
        try:
            vm = psutil.virtual_memory()
            total = format_bytes(vm.total)
            available = format_bytes(vm.available)
            used = format_bytes(vm.used)
            percent = "%.1f%%" % vm.percent
        except Exception:
            pass
    speed, slots = _ram_details()
    return [
        ("label_total", total),
        ("label_available", available),
        ("label_used", used),
        ("label_percent", percent),
        ("label_speed", speed),
        ("label_slots", slots),
    ]


def _ram_details():
    """Return (speed, module-count) as strings, best effort."""
    try:
        if os.name == "nt":
            rc, out, _err = run_cmd(
                [
                    "powershell",
                    "-NoProfile",
                    "-NonInteractive",
                    "-Command",
                    "Get-CimInstance Win32_PhysicalMemory | Select-Object Speed,DeviceLocator | Format-List",
                ],
                timeout=30,
            )
            speed = "N/A"
            slots = 0
            if rc == 0:
                for block in _parse_ps_blocks(out):
                    raw = block.get("speed")
                    if raw and str(raw).isdigit() and int(raw) > 0:
                        speed = "%d MHz" % int(raw)
                    if block.get("devicelocator"):
                        slots += 1
            return speed, (str(slots) if slots else "N/A")
        if sys.platform == "darwin":
            rc, out, _err = run_cmd(["system_profiler", "SPMemoryDataType"], timeout=40)
            parsed = _parse_colon_lines(out)
            speed = parsed.get("speed") or "N/A"
            slots = parsed.get("number of memory slots") or "N/A"
            return speed, slots
        if sys.platform.startswith("linux"):
            rc, out, _err = run_cmd(["dmidecode", "-t", "memory"], timeout=20)
            speed = "N/A"
            count = 0
            for line in out.splitlines():
                stripped = line.strip()
                if stripped.startswith("Memory Device"):
                    count += 1
                if stripped.lower().startswith("speed:"):
                    val = stripped.split(":", 1)[1].strip()
                    if val and val.lower() != "unknown":
                        speed = val
            return speed, (str(count) if count else "N/A")
    except Exception:
        pass
    return "N/A", "N/A"


# --------------------------------------------------------------------------- #
# GPU
# --------------------------------------------------------------------------- #
def inspect_gpu():
    """Return a list of dicts: {name, vram, driver}."""
    items = []
    try:
        if os.name == "nt":
            items = _gpu_windows()
        elif sys.platform == "darwin":
            items = _gpu_macos()
        elif sys.platform.startswith("linux"):
            items = _gpu_linux()
    except Exception:
        items = []
    if not items:
        items = [{"name": "N/A", "vram": "N/A", "driver": "N/A"}]
    return items


def _gpu_windows():
    items = []
    rc, out, _err = run_cmd(
        [
            "powershell",
            "-NoProfile",
            "-NonInteractive",
            "-Command",
            "Get-CimInstance Win32_VideoController | Select-Object Name,AdapterRAM,DriverVersion | Format-List",
        ],
        timeout=30,
    )
    for block in _parse_ps_blocks(out):
        name = block.get("name")
        if not name:
            continue
        vram_raw = block.get("adapterram", "")
        vram = "N/A"
        if str(vram_raw).isdigit() and int(vram_raw) > 0:
            vram = format_bytes(int(vram_raw))
        items.append(
            {"name": name, "vram": vram, "driver": block.get("driverversion") or "N/A"}
        )
    if not items:
        rc, out, _err = run_cmd(
            ["wmic", "path", "win32_VideoController", "get", "Name,AdapterRAM,DriverVersion"],
            timeout=30,
        )
        for line in out.splitlines():
            stripped = line.strip()
            if not stripped or stripped.lower().startswith("name"):
                continue
            tokens = stripped.split()
            if len(tokens) >= 2:
                driver = tokens[-1]
                vram_raw = tokens[-2]
                vram = "N/A"
                if vram_raw.isdigit() and int(vram_raw) > 0:
                    vram = format_bytes(int(vram_raw))
                items.append({"name": " ".join(tokens[:-2]), "vram": vram, "driver": driver})
    return items


def _gpu_linux():
    items = []
    rc, out, _err = run_cmd(["lspci", "-nn"], timeout=20)
    for line in out.splitlines():
        if re.search(r"(vga compatible|3d controller|display controller)", line, re.I):
            match = re.match(r"([0-9a-f:.]+)\s+(.*)", line.strip())
            if not match:
                continue
            address, name = match.group(1), match.group(2)
            driver = "N/A"
            rc2, out2, _err2 = run_cmd(["lspci", "-k", "-s", address], timeout=20)
            for sub in out2.splitlines():
                if "Kernel driver in use" in sub:
                    driver = sub.split(":", 1)[1].strip()
                    break
            items.append({"name": name, "vram": "N/A", "driver": driver})
    return items


def _gpu_macos():
    items = []
    rc, out, _err = run_cmd(["system_profiler", "SPDisplaysDataType"], timeout=40)
    parsed = _parse_colon_lines(out)
    chipset = parsed.get("chipset model") or parsed.get("chipset")
    vendor = parsed.get("vendor")
    vram = parsed.get("vram (total)")
    metal = parsed.get("metal")
    if chipset or vendor:
        parts = [p for p in (vendor, metal and "Metal %s" % metal) if p]
        driver = " · ".join(parts) or "N/A"
        items.append({"name": chipset or vendor or "N/A", "vram": vram or "N/A", "driver": driver})
    return items


# --------------------------------------------------------------------------- #
# Storage
# --------------------------------------------------------------------------- #
def inspect_storage(t):
    """Return {'drives': [...], 'partitions': [...]} with localized interfaces."""
    return {"drives": _physical_drives(t), "partitions": _partitions()}


def _partitions():
    parts = []
    if psutil is not None:
        try:
            for part in psutil.disk_partitions(all=False):
                mount = part.mountpoint
                fs = part.fstype or "?"
                try:
                    usage = psutil.disk_usage(mount)
                    total = format_bytes(usage.total)
                    free = format_bytes(usage.free)
                    percent = "%.1f%%" % (100.0 - usage.percent)
                except Exception:
                    total = free = percent = "N/A"
                parts.append([mount, fs, total, free, percent])
        except Exception:
            pass
    else:
        try:
            usage = shutil.disk_usage(os.getcwd())
            parts.append(
                [
                    os.getcwd(),
                    "?",
                    format_bytes(usage.total),
                    format_bytes(usage.free),
                    "N/A",
                ]
            )
        except Exception:
            pass
    return parts


def _map_interface(t, media, bus):
    media = (media or "").lower()
    bus = (bus or "").lower()
    if "nvme" in bus:
        return t("disk_nvme")
    if media == "ssd":
        return t("disk_ssd")
    if media == "hdd":
        return t("disk_hdd")
    if bus:
        return bus.upper()
    return t("unknown")


def _physical_drives(t):
    """Return physical drive rows: [name, interface, total]."""
    drives = []
    try:
        if os.name == "nt":
            rc, out, _err = run_cmd(
                [
                    "powershell",
                    "-NoProfile",
                    "-NonInteractive",
                    "-Command",
                    "Get-PhysicalDisk | Select-Object FriendlyName,MediaType,BusType,"
                    "@{N='SizeGB';E={[math]::Round($_.Size/1GB,1)}} | Format-List",
                ],
                timeout=30,
            )
            if rc == 0:
                for block in _parse_ps_blocks(out):
                    name = block.get("friendlyname")
                    if not name:
                        continue
                    size_gb = block.get("sizegb")
                    total = (
                        format_bytes(float(size_gb) * 1e9)
                        if _is_number(size_gb)
                        else "N/A"
                    )
                    drives.append(
                        {
                            "name": name,
                            "interface": _map_interface(
                                t, block.get("mediatype"), block.get("bustype")
                            ),
                            "total": total,
                        }
                    )
            if not drives:
                rc, out, _err = run_cmd(
                    [
                        "powershell",
                        "-NoProfile",
                        "-NonInteractive",
                        "-Command",
                        "Get-CimInstance Win32_DiskDrive | Select-Object Model,InterfaceType,"
                        "@{N='SizeGB';E={[math]::Round($_.Size/1GB,1)}} | Format-List",
                    ],
                    timeout=30,
                )
                for block in _parse_ps_blocks(out):
                    name = block.get("model")
                    if not name:
                        continue
                    size_gb = block.get("sizegb")
                    total = (
                        format_bytes(float(size_gb) * 1e9)
                        if _is_number(size_gb)
                        else "N/A"
                    )
                    drives.append(
                        {
                            "name": name,
                            "interface": _map_interface(t, "", block.get("interfacetype")),
                            "total": total,
                        }
                    )
        elif sys.platform == "darwin":
            rc, out, _err = run_cmd(
                ["system_profiler", "SPSerialATADataType", "SPNVMeDataType"], timeout=40
            )
            parsed = _parse_colon_lines(out)
            model = parsed.get("model") or parsed.get("device model")
            protocol = parsed.get("protocol") or "N/A"
            if model:
                interface = (
                    t("disk_nvme")
                    if "nvme" in protocol.lower()
                    else (protocol.upper() if protocol != "N/A" else t("unknown"))
                )
                drives.append({"name": model, "interface": interface, "total": "N/A"})
        elif sys.platform.startswith("linux"):
            for entry in sorted(glob.glob("/sys/block/*")):
                name = os.path.basename(entry)
                if not name or name.startswith(("loop", "ram", "sr", "fd", "zram")):
                    continue
                size = _read_sysfs(os.path.join(entry, "size"))
                rota = _read_sysfs(os.path.join(entry, "queue", "rotational"))
                if name.startswith("nvme"):
                    interface = t("disk_nvme")
                elif rota == "0":
                    interface = t("disk_ssd")
                elif rota == "1":
                    interface = t("disk_hdd")
                else:
                    interface = t("unknown")
                total = (
                    format_bytes(int(size) * 512)
                    if size and str(size).isdigit()
                    else "N/A"
                )
                drives.append({"name": name, "interface": interface, "total": total})
    except Exception:
        pass
    return drives


def _is_number(value):
    try:
        float(value)
        return True
    except (TypeError, ValueError):
        return False


# --------------------------------------------------------------------------- #
# Rendering
# --------------------------------------------------------------------------- #
def _fmt(t, value):
    """Normalize a raw value to a localized display string."""
    if value is None or value == "":
        return t("na")
    if value == "ACCESS_DENIED":
        return t("access_denied")
    return str(value)


def collect(t):
    """Collect all inspection sections for rendering or JSON export.

    Returns a list of section dicts:
      {"type": "kv",    "title": str, "rows": [(i18n_key, value), ...]}
      {"type": "table", "title": str, "headers": [str, ...], "rows": [[str, ...], ...]}
    """
    gpu = inspect_gpu()
    storage = inspect_storage(t)
    sections = [
        {"type": "kv", "title": t("section_os"), "rows": inspect_os_section()},
        {"type": "kv", "title": t("section_motherboard"), "rows": inspect_motherboard_section()},
        {"type": "kv", "title": t("section_cpu"), "rows": inspect_cpu_section()},
        {"type": "kv", "title": t("section_ram"), "rows": inspect_ram_section()},
        {
            "type": "table",
            "title": t("section_gpu"),
            "headers": [t("label_name"), t("label_vram"), t("label_driver")],
            "rows": [
                [_fmt(t, g.get("name")), _fmt(t, g.get("vram")), _fmt(t, g.get("driver"))]
                for g in gpu
            ],
        },
        {
            "type": "table",
            "title": t("section_storage"),
            "headers": [t("label_name"), t("label_interface"), t("label_size")],
            "rows": [
                [d.get("name", "N/A"), d.get("interface", "N/A"), d.get("total", "N/A")]
                for d in storage["drives"]
            ],
        },
        {
            "type": "table",
            "title": t("section_partitions"),
            "headers": [
                t("label_mount"),
                t("label_fs"),
                t("label_size"),
                t("label_free"),
                t("label_percent"),
            ],
            "rows": storage["partitions"],
        },
    ]
    return sections


def to_dict(t, sections=None):
    """Flatten collected sections into a JSON-serializable dict."""
    sections = sections if sections is not None else collect(t)
    payload = {}
    for section in sections:
        if section["type"] == "kv":
            payload[section["title"]] = {t(key): _fmt(t, value) for key, value in section["rows"]}
        else:
            payload[section["title"]] = {"columns": section["headers"], "rows": section["rows"]}
    return payload


def run(console, t, as_json=False, rtl=False):
    """Render the full inspection report on the console."""
    sections = collect(t)
    if as_json:
        console.print(JSON(json.dumps(to_dict(t, sections), ensure_ascii=False, indent=2)))
        return
    justify = "right" if rtl else "left"
    console.print()
    console.print(
        Panel("[bold cyan]%s[/]" % t("inspect_header"), border_style="cyan")
    )
    for section in sections:
        if section["type"] == "kv":
            table = Table(
                title=section["title"],
                title_justify=justify,
                show_header=False,
                border_style="blue",
                box=box.SIMPLE_HEAD,
            )
            table.add_column(style="bold", no_wrap=True, justify=justify)
            table.add_column(justify=justify)
            for key, value in section["rows"]:
                table.add_row(t(key), _fmt(t, value))
        else:
            table = Table(
                title=section["title"],
                title_justify=justify,
                border_style="blue",
                box=box.SIMPLE_HEAD,
            )
            for header in section["headers"]:
                table.add_column(header, justify=justify)
            for row in section["rows"]:
                table.add_row(*[str(cell) for cell in row])
        console.print(table)
        console.print()
