# 📊 sys-opt Nightly Benchmark

Automated **CPU / RAM / disk** benchmarks (light stress via `psutil`) run every night on
**Linux, macOS and Windows** (GitHub-hosted runners). Each run is appended to
`benchmarks/<os>.json`; this report shows the latest run per OS and the recent history.

_Last update: 2026-08-02 05:52 UTC_

## Latest run per OS

| Metric | **macos-14** | **ubuntu-24.04** | **windows-2022** | Unit |
|---|---|---|---|---|
| CPU | 10.6 M ops/s | 7.3 M ops/s | 6.7 M ops/s |
| RAM | 20518 MB/s | 19646 MB/s | 21894 MB/s |
| Disk write | 2050 MB/s | 1504 MB/s | 87 MB/s |
| Disk read | 2273 MB/s | 7547 MB/s | 3304 MB/s |
| Elapsed | 1.2 s | 1.2 s | 1.4 s |
| **Overall verdict** | 🟢 Excellent | 🟢 Good | 🔴 Below average |

## How to read these numbers

| Metric | Meaning | Higher is |
|---|---|---|
| **CPU** | Floating-point operations per second (light compute loop) | better |
| **RAM** | Memory bandwidth measured with repeated buffer copies | better |
| **Disk write / read** | Sequential temp-file write/read speed (fsync included) | better |
| **Elapsed** | Total time the whole benchmark took | lower is better |

The **overall verdict** is the *lowest* tier among the measured
components: a machine is only as fast as its weakest part. Expect
realistic numbers on a GitHub-hosted runner to land in the
**Average** band — that is the baseline.

Run `python -m sys_opt --benchmark` on your own machine **before**
optimizing to get a baseline, then again **after** to measure the
improvement.

## Recent history

### macos-14

| Date (UTC) | CPU (M ops/s) | RAM (MB/s) | Write (MB/s) | Read (MB/s) | Elapsed (s) |
|---|---|---|---|---|---|
| 2026-08-02T05:52:39Z | 10.61  | 20518  | 2050  | 2273  | 1.2  |

### ubuntu-24.04

| Date (UTC) | CPU (M ops/s) | RAM (MB/s) | Write (MB/s) | Read (MB/s) | Elapsed (s) |
|---|---|---|---|---|---|
| 2026-08-02T05:52:39Z | 7.27  | 19646  | 1504  | 7547  | 1.2  |

### windows-2022

| Date (UTC) | CPU (M ops/s) | RAM (MB/s) | Write (MB/s) | Read (MB/s) | Elapsed (s) |
|---|---|---|---|---|---|
| 2026-08-02T05:52:39Z | 6.65  | 21894  | 87  | 3304  | 1.4  |

