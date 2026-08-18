# 📊 sys-opt Nightly Benchmark

Automated **CPU / RAM / disk** benchmarks (light stress via `psutil`) run every night on
**Linux, macOS and Windows** (GitHub-hosted runners). Each run is appended to
`benchmarks/<os>.json`; this report shows the latest run per OS and the recent history.

_Last update: 2026-08-18 03:40 UTC_

## Latest run per OS

| Metric | **macos-14** | **ubuntu-24.04** | **windows-2022** | Unit |
|---|---|---|---|---|
| CPU | 7.6 M ops/s | 8.9 M ops/s | 9.0 M ops/s |
| RAM | 14749 MB/s | 9194 MB/s | 11628 MB/s |
| Disk write | 1093 MB/s | 135 MB/s | 90 MB/s |
| Disk read | 3410 MB/s | 5449 MB/s | 1746 MB/s |
| Elapsed | 1.3 s | 1.4 s | 1.5 s |
| **Overall verdict** | 🟢 Good | 🔴 Below average | 🔴 Below average |

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
| 2026-08-05T05:42:10Z | 8.89  | 16478  | 1864  | 1845  | 1.2  |
| 2026-08-06T05:44:09Z | 10.99  | 17603  | 1258  | 6268  | 1.2  |
| 2026-08-07T04:51:26Z | 10.58  | 21830  | 1058  | 1743  | 1.2  |
| 2026-08-08T04:08:33Z | 9.91  | 23077  | 2450  | 1818  | 1.2  |
| 2026-08-09T04:15:11Z | 9.94  | 22658  | 1619  | 10744  | 1.2  |
| 2026-08-10T04:26:34Z | 9.85  | 13788  | 1789  | 1808  | 1.2  |
| 2026-08-11T04:15:56Z | 9.67  | 20327  | 2757  | 11453  | 1.2  |
| 2026-08-12T04:44:48Z | 9.80  | 23396  | 1952  | 2031  | 1.2  |
| 2026-08-13T04:48:23Z | 10.36  | 16892  | 1808  | 9410  | 1.2  |
| 2026-08-14T04:45:21Z | 10.46  | 21391  | 1949  | 1667  | 1.2  |
| 2026-08-15T03:34:27Z | 10.30  | 16472  | 2213  | 10457  | 1.2  |
| 2026-08-16T03:43:41Z | 10.67  | 18051  | 1798  | 1954  | 1.2  |
| 2026-08-17T03:45:27Z | 11.00  | 20712  | 1999  | 5220  | 1.1  |
| 2026-08-18T03:40:14Z | 7.56  | 14749  | 1093  | 3410  | 1.3  |

### ubuntu-24.04

| Date (UTC) | CPU (M ops/s) | RAM (MB/s) | Write (MB/s) | Read (MB/s) | Elapsed (s) |
|---|---|---|---|---|---|
| 2026-08-05T05:42:10Z | 7.05  | 22684  | 1401  | 6799  | 1.2  |
| 2026-08-06T05:44:09Z | 7.16  | 17554  | 391  | 7702  | 1.2  |
| 2026-08-07T04:51:26Z | 6.97  | 22219  | 1410  | 6801  | 1.2  |
| 2026-08-08T04:08:33Z | 7.05  | 25970  | 1708  | 7724  | 1.1  |
| 2026-08-09T04:15:11Z | 5.78  | 20289  | 1452  | 7766  | 1.2  |
| 2026-08-10T04:26:34Z | 7.12  | 22445  | 1286  | 6555  | 1.2  |
| 2026-08-11T04:15:56Z | 7.37  | 17329  | 1863  | 8004  | 1.2  |
| 2026-08-12T04:44:48Z | 7.30  | 17610  | 2007  | 7987  | 1.2  |
| 2026-08-13T04:48:23Z | 12.40  | 24468  | 126  | 12311  | 1.4  |
| 2026-08-14T04:45:21Z | 7.33  | 19622  | 1893  | 7792  | 1.2  |
| 2026-08-15T03:34:27Z | 7.08  | 23093  | 1518  | 7839  | 1.1  |
| 2026-08-16T03:43:41Z | 6.95  | 22724  | 1358  | 6736  | 1.2  |
| 2026-08-17T03:45:27Z | 10.16  | 11933  | 160  | 5829  | 1.3  |
| 2026-08-18T03:40:14Z | 8.93  | 9194  | 135  | 5449  | 1.4  |

### windows-2022

| Date (UTC) | CPU (M ops/s) | RAM (MB/s) | Write (MB/s) | Read (MB/s) | Elapsed (s) |
|---|---|---|---|---|---|
| 2026-08-05T05:42:10Z | 6.78  | 19837  | 78  | 2815  | 1.5  |
| 2026-08-06T05:44:09Z | 6.29  | 23035  | 111  | 2841  | 1.4  |
| 2026-08-07T04:51:26Z | 6.87  | 19704  | 116  | 3039  | 1.4  |
| 2026-08-08T04:08:33Z | 6.82  | 20876  | 94  | 3520  | 1.4  |
| 2026-08-09T04:15:11Z | 7.17  | 21865  | 145  | 3508  | 1.3  |
| 2026-08-10T04:26:34Z | 6.75  | 22740  | 120  | 3227  | 1.3  |
| 2026-08-11T04:15:56Z | 6.84  | 19805  | 95  | 2900  | 1.4  |
| 2026-08-12T04:44:48Z | 11.80  | 12511  | 65  | 1936  | 1.6  |
| 2026-08-13T04:48:23Z | 6.83  | 23355  | 121  | 3044  | 1.3  |
| 2026-08-14T04:45:21Z | 6.84  | 21747  | 138  | 3101  | 1.3  |
| 2026-08-15T03:34:27Z | 6.84  | 19866  | 129  | 2997  | 1.3  |
| 2026-08-16T03:43:41Z | 6.87  | 24649  | 50  | 3486  | 1.7  |
| 2026-08-17T03:45:27Z | 6.86  | 20992  | 120  | 3255  | 1.3  |
| 2026-08-18T03:40:14Z | 9.04  | 11628  | 90  | 1746  | 1.5  |

