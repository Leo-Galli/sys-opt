# 📊 sys-opt Nightly Benchmark

Automated **CPU / RAM / disk** benchmarks (light stress via `psutil`) run every night on
**Linux, macOS and Windows** (GitHub-hosted runners). Each run is appended to
`benchmarks/<os>.json`; this report shows the latest run per OS and the recent history.

_Last update: 2026-08-08 04:08 UTC_

## Latest run per OS

| Metric | **macos-14** | **ubuntu-24.04** | **windows-2022** | Unit |
|---|---|---|---|---|
| CPU | 9.9 M ops/s | 7.0 M ops/s | 6.8 M ops/s |
| RAM | 23077 MB/s | 25970 MB/s | 20876 MB/s |
| Disk write | 2450 MB/s | 1708 MB/s | 94 MB/s |
| Disk read | 1818 MB/s | 7724 MB/s | 3520 MB/s |
| Elapsed | 1.2 s | 1.1 s | 1.4 s |
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
| 2026-08-03T06:17:24Z | 9.69  | 13846  | 1708  | 7397  | 1.2  |
| 2026-08-04T05:43:30Z | 10.77  | 22564  | 4555  | 11719  | 1.1  |
| 2026-08-05T05:42:10Z | 8.89  | 16478  | 1864  | 1845  | 1.2  |
| 2026-08-06T05:44:09Z | 10.99  | 17603  | 1258  | 6268  | 1.2  |
| 2026-08-07T04:51:26Z | 10.58  | 21830  | 1058  | 1743  | 1.2  |
| 2026-08-08T04:08:33Z | 9.91  | 23077  | 2450  | 1818  | 1.2  |

### ubuntu-24.04

| Date (UTC) | CPU (M ops/s) | RAM (MB/s) | Write (MB/s) | Read (MB/s) | Elapsed (s) |
|---|---|---|---|---|---|
| 2026-08-02T05:52:39Z | 7.27  | 19646  | 1504  | 7547  | 1.2  |
| 2026-08-03T06:17:24Z | 9.50  | 20599  | 153  | 10522  | 1.3  |
| 2026-08-04T05:43:30Z | 6.98  | 23096  | 1310  | 7738  | 1.2  |
| 2026-08-05T05:42:10Z | 7.05  | 22684  | 1401  | 6799  | 1.2  |
| 2026-08-06T05:44:09Z | 7.16  | 17554  | 391  | 7702  | 1.2  |
| 2026-08-07T04:51:26Z | 6.97  | 22219  | 1410  | 6801  | 1.2  |
| 2026-08-08T04:08:33Z | 7.05  | 25970  | 1708  | 7724  | 1.1  |

### windows-2022

| Date (UTC) | CPU (M ops/s) | RAM (MB/s) | Write (MB/s) | Read (MB/s) | Elapsed (s) |
|---|---|---|---|---|---|
| 2026-08-02T05:52:39Z | 6.65  | 21894  | 87  | 3304  | 1.4  |
| 2026-08-03T06:17:24Z | 6.98  | 22664  | 84  | 3181  | 1.4  |
| 2026-08-04T05:43:30Z | 6.38  | 21206  | 123  | 2864  | 1.3  |
| 2026-08-05T05:42:10Z | 6.78  | 19837  | 78  | 2815  | 1.5  |
| 2026-08-06T05:44:09Z | 6.29  | 23035  | 111  | 2841  | 1.4  |
| 2026-08-07T04:51:26Z | 6.87  | 19704  | 116  | 3039  | 1.4  |
| 2026-08-08T04:08:33Z | 6.82  | 20876  | 94  | 3520  | 1.4  |

