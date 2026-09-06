# 📊 sys-opt Nightly Benchmark

Automated **CPU / RAM / disk** benchmarks (light stress via `psutil`) run every night on
**Linux, macOS and Windows** (GitHub-hosted runners). Each run is appended to
`benchmarks/<os>.json`; this report shows the latest run per OS and the recent history.

_Last update: 2026-09-06 07:32 UTC_

## Latest run per OS

| Metric | **macos-14** | **ubuntu-24.04** | **windows-2022** | Unit |
|---|---|---|---|---|
| CPU | 10.4 M ops/s | 7.0 M ops/s | 7.0 M ops/s |
| RAM | 21156 MB/s | 22321 MB/s | 23400 MB/s |
| Disk write | 1914 MB/s | 1263 MB/s | 123 MB/s |
| Disk read | 3146 MB/s | 7562 MB/s | 3118 MB/s |
| Elapsed | 1.2 s | 1.2 s | 1.3 s |
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
| 2026-08-24T03:50:38Z | 9.83  | 16653  | 1963  | 5172  | 1.2  |
| 2026-08-25T03:44:18Z | 8.81  | 15659  | 1237  | 1566  | 1.3  |
| 2026-08-26T03:50:15Z | 10.43  | 20462  | 1450  | 2156  | 1.2  |
| 2026-08-27T13:39:30Z | 7.37  | 16916  | 1207  | 6211  | 1.3  |
| 2026-08-28T14:49:57Z | 11.22  | 20835  | 3891  | 2292  | 1.2  |
| 2026-08-29T09:40:25Z | 7.54  | 17857  | 945  | 5213  | 1.3  |
| 2026-08-30T08:51:54Z | 10.51  | 21042  | 3873  | 9042  | 1.2  |
| 2026-08-31T09:15:06Z | 10.02  | 18790  | 1750  | 1952  | 1.3  |
| 2026-09-01T08:14:09Z | 7.72  | 13473  | 1628  | 3941  | 1.3  |
| 2026-09-02T07:33:15Z | 10.89  | 18892  | 4491  | 12306  | 1.2  |
| 2026-09-03T07:41:23Z | 7.75  | 16346  | 1993  | 1880  | 1.2  |
| 2026-09-04T07:39:07Z | 7.27  | 12999  | 1545  | 3622  | 1.2  |
| 2026-09-05T07:19:42Z | 10.83  | 22165  | 2785  | 10453  | 1.2  |
| 2026-09-06T07:32:40Z | 10.40  | 21156  | 1914  | 3146  | 1.2  |

### ubuntu-24.04

| Date (UTC) | CPU (M ops/s) | RAM (MB/s) | Write (MB/s) | Read (MB/s) | Elapsed (s) |
|---|---|---|---|---|---|
| 2026-08-24T03:50:38Z | 10.00  | 12806  | 153  | 5689  | 1.4  |
| 2026-08-25T03:44:18Z | 8.49  | 10113  | 1403  | 4880  | 1.2  |
| 2026-08-26T03:50:15Z | 7.35  | 18090  | 1887  | 7077  | 1.2  |
| 2026-08-27T13:39:30Z | 7.00  | 22654  | 1498  | 6131  | 1.1  |
| 2026-08-28T14:49:57Z | 6.99  | 18574  | 1072  | 5270  | 1.2  |
| 2026-08-29T09:40:25Z | 7.00  | 21477  | 1239  | 6391  | 1.2  |
| 2026-08-30T08:51:54Z | 7.41  | 18677  | 1880  | 7383  | 1.2  |
| 2026-08-31T09:15:06Z | 6.99  | 20165  | 1427  | 6438  | 1.2  |
| 2026-09-01T08:14:09Z | 6.90  | 20909  | 1428  | 7369  | 1.2  |
| 2026-09-02T07:33:15Z | 10.18  | 12720  | 81  | 5874  | 1.5  |
| 2026-09-03T07:41:23Z | 9.45  | 12544  | 39  | 4430  | 2.0  |
| 2026-09-04T07:39:07Z | 6.89  | 24370  | 1693  | 7563  | 1.1  |
| 2026-09-05T07:19:42Z | 7.02  | 22645  | 1217  | 6542  | 1.2  |
| 2026-09-06T07:32:40Z | 7.01  | 22321  | 1263  | 7562  | 1.2  |

### windows-2022

| Date (UTC) | CPU (M ops/s) | RAM (MB/s) | Write (MB/s) | Read (MB/s) | Elapsed (s) |
|---|---|---|---|---|---|
| 2026-08-24T03:50:38Z | 6.75  | 24286  | 123  | 3106  | 1.3  |
| 2026-08-25T03:44:18Z | 9.25  | 12720  | 2  | 1723  | 16.6  |
| 2026-08-26T03:50:15Z | 7.19  | 22184  | 83  | 3030  | 1.4  |
| 2026-08-27T13:39:30Z | 7.18  | 22265  | 160  | 3122  | 1.3  |
| 2026-08-28T14:49:57Z | 6.74  | 24600  | 91  | 2958  | 1.4  |
| 2026-08-29T09:40:25Z | 12.79  | 12494  | 114  | 2037  | 1.4  |
| 2026-08-30T08:51:54Z | 7.16  | 22179  | 81  | 2872  | 1.5  |
| 2026-08-31T09:15:06Z | 8.11  | 23251  | 110  | 3180  | 1.4  |
| 2026-09-01T08:14:09Z | 7.20  | 21855  | 112  | 3186  | 1.4  |
| 2026-09-02T07:33:15Z | 7.17  | 20805  | 77  | 2890  | 1.5  |
| 2026-09-03T07:41:23Z | 6.26  | 26250  | 97  | 3072  | 1.4  |
| 2026-09-04T07:39:07Z | 7.16  | 21089  | 102  | 2909  | 1.4  |
| 2026-09-05T07:19:42Z | 6.85  | 24338  | 151  | 3243  | 1.3  |
| 2026-09-06T07:32:40Z | 6.99  | 23400  | 123  | 3118  | 1.3  |

