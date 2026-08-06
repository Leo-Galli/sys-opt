# 📊 sys-opt Nightly Benchmark

Automated **CPU / RAM / disk** benchmarks (light stress via `psutil`) run every night on
**Linux, macOS and Windows** (GitHub-hosted runners). Each run is appended to
`benchmarks/<os>.json`; this report shows the latest run per OS and the recent history.

_Last update: 2026-08-06 05:44 UTC_

## Latest run per OS

| Metric | **macos-14** | **ubuntu-24.04** | **windows-2022** | Unit |
|---|---|---|---|---|
| CPU | 11.0 M ops/s | 7.2 M ops/s | 6.3 M ops/s |
| RAM | 17603 MB/s | 17554 MB/s | 23035 MB/s |
| Disk write | 1258 MB/s | 391 MB/s | 111 MB/s |
| Disk read | 6268 MB/s | 7702 MB/s | 2841 MB/s |
| Elapsed | 1.2 s | 1.2 s | 1.4 s |
| **Overall verdict** | 🟢 Excellent | 🟡 Average | 🔴 Below average |

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

### ubuntu-24.04

| Date (UTC) | CPU (M ops/s) | RAM (MB/s) | Write (MB/s) | Read (MB/s) | Elapsed (s) |
|---|---|---|---|---|---|
| 2026-08-02T05:52:39Z | 7.27  | 19646  | 1504  | 7547  | 1.2  |
| 2026-08-03T06:17:24Z | 9.50  | 20599  | 153  | 10522  | 1.3  |
| 2026-08-04T05:43:30Z | 6.98  | 23096  | 1310  | 7738  | 1.2  |
| 2026-08-05T05:42:10Z | 7.05  | 22684  | 1401  | 6799  | 1.2  |
| 2026-08-06T05:44:09Z | 7.16  | 17554  | 391  | 7702  | 1.2  |

### windows-2022

| Date (UTC) | CPU (M ops/s) | RAM (MB/s) | Write (MB/s) | Read (MB/s) | Elapsed (s) |
|---|---|---|---|---|---|
| 2026-08-02T05:52:39Z | 6.65  | 21894  | 87  | 3304  | 1.4  |
| 2026-08-03T06:17:24Z | 6.98  | 22664  | 84  | 3181  | 1.4  |
| 2026-08-04T05:43:30Z | 6.38  | 21206  | 123  | 2864  | 1.3  |
| 2026-08-05T05:42:10Z | 6.78  | 19837  | 78  | 2815  | 1.5  |
| 2026-08-06T05:44:09Z | 6.29  | 23035  | 111  | 2841  | 1.4  |

