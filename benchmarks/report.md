# 📊 sys-opt Nightly Benchmark

Automated **CPU / RAM / disk** benchmarks (light stress via `psutil`) run every night on
**Linux, macOS and Windows** (GitHub-hosted runners). Each run is appended to
`benchmarks/<os>.json`; this report shows the latest run per OS and the recent history.

_Last update: 2026-09-23 08:13 UTC_

## Latest run per OS

| Metric | **macos-14** | **ubuntu-24.04** | **windows-2022** | Unit |
|---|---|---|---|---|
| CPU | 11.0 M ops/s | 7.0 M ops/s | 7.2 M ops/s |
| RAM | 22420 MB/s | 22376 MB/s | 23130 MB/s |
| Disk write | 4187 MB/s | 1550 MB/s | 51 MB/s |
| Disk read | 13164 MB/s | 7074 MB/s | 3088 MB/s |
| Elapsed | 1.2 s | 1.1 s | 1.7 s |
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
| 2026-09-10T07:48:54Z | 8.78  | 13826  | 3065  | 8255  | 1.2  |
| 2026-09-11T07:42:49Z | 10.81  | 23267  | 1584  | 11858  | 1.1  |
| 2026-09-12T07:38:06Z | 10.28  | 19707  | 3293  | 10224  | 1.2  |
| 2026-09-13T07:56:30Z | 10.59  | 17509  | 2543  | 3291  | 1.2  |
| 2026-09-14T08:29:28Z | 6.83  | 10760  | 1205  | 3379  | 1.2  |
| 2026-09-15T08:19:48Z | 10.74  | 15626  | 2552  | 1458  | 1.2  |
| 2026-09-16T08:13:37Z | 9.57  | 13072  | 1167  | 4849  | 1.2  |
| 2026-09-17T08:20:05Z | 8.86  | 12289  | 1143  | 5944  | 1.3  |
| 2026-09-18T07:55:25Z | 8.32  | 14353  | 1576  | 3727  | 1.2  |
| 2026-09-19T07:45:33Z | 7.61  | 9506  | 930  | 5083  | 1.3  |
| 2026-09-20T08:14:16Z | 8.72  | 13399  | 1398  | 4903  | 1.2  |
| 2026-09-21T08:31:01Z | 8.30  | 14053  | 990  | 6934  | 1.2  |
| 2026-09-22T08:11:44Z | 8.27  | 17436  | 1150  | 3551  | 1.2  |
| 2026-09-23T08:13:51Z | 10.96  | 22420  | 4187  | 13164  | 1.2  |

### ubuntu-24.04

| Date (UTC) | CPU (M ops/s) | RAM (MB/s) | Write (MB/s) | Read (MB/s) | Elapsed (s) |
|---|---|---|---|---|---|
| 2026-09-10T07:48:54Z | 6.79  | 22341  | 1066  | 7759  | 1.2  |
| 2026-09-11T07:42:49Z | 6.98  | 23260  | 1238  | 7637  | 1.2  |
| 2026-09-12T07:38:06Z | 6.87  | 24184  | 1647  | 7537  | 1.1  |
| 2026-09-13T07:56:30Z | 7.45  | 18376  | 1646  | 7419  | 1.2  |
| 2026-09-14T08:29:28Z | 8.35  | 9077  | 1236  | 4570  | 1.2  |
| 2026-09-15T08:19:48Z | 6.86  | 18183  | 1632  | 7432  | 1.2  |
| 2026-09-16T08:13:37Z | 7.07  | 20155  | 1409  | 6996  | 1.2  |
| 2026-09-17T08:20:05Z | 7.42  | 17153  | 1868  | 7713  | 1.2  |
| 2026-09-18T07:55:25Z | 8.60  | 11469  | 1565  | 5870  | 1.2  |
| 2026-09-19T07:45:33Z | 12.45  | 25057  | 181  | 11773  | 1.3  |
| 2026-09-20T08:14:16Z | 7.21  | 16389  | 1640  | 8087  | 1.2  |
| 2026-09-21T08:31:01Z | 8.89  | 10717  | 1438  | 5858  | 1.2  |
| 2026-09-22T08:11:44Z | 7.00  | 21479  | 1429  | 7031  | 1.2  |
| 2026-09-23T08:13:51Z | 7.02  | 22376  | 1550  | 7074  | 1.1  |

### windows-2022

| Date (UTC) | CPU (M ops/s) | RAM (MB/s) | Write (MB/s) | Read (MB/s) | Elapsed (s) |
|---|---|---|---|---|---|
| 2026-09-10T07:48:54Z | 6.86  | 17348  | 86  | 2634  | 1.4  |
| 2026-09-11T07:42:49Z | 6.81  | 23382  | 70  | 3197  | 1.5  |
| 2026-09-12T07:38:06Z | 6.85  | 23326  | 76  | 3159  | 1.5  |
| 2026-09-13T07:56:30Z | 7.17  | 21363  | 99  | 3033  | 1.4  |
| 2026-09-14T08:29:28Z | 6.11  | 25888  | 82  | 1748  | 1.7  |
| 2026-09-15T08:19:48Z | 7.18  | 22203  | 84  | 3125  | 1.4  |
| 2026-09-16T08:13:37Z | 8.41  | 26629  | 73  | 3853  | 1.5  |
| 2026-09-17T08:20:05Z | 8.38  | 28888  | 127  | 3640  | 1.3  |
| 2026-09-18T07:55:25Z | 7.20  | 21332  | 78  | 3065  | 1.5  |
| 2026-09-19T07:45:33Z | 9.55  | 14862  | 122  | 1698  | 1.4  |
| 2026-09-20T08:14:16Z | 6.93  | 22230  | 102  | 2549  | 1.4  |
| 2026-09-21T08:31:01Z | 7.21  | 22426  | 91  | 2996  | 1.4  |
| 2026-09-22T08:11:44Z | 8.62  | 9970  | 51  | 1748  | 2.1  |
| 2026-09-23T08:13:51Z | 7.19  | 23130  | 51  | 3088  | 1.7  |

