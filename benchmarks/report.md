# 📊 sys-opt Nightly Benchmark

Automated **CPU / RAM / disk** benchmarks (light stress via `psutil`) run every night on
**Linux, macOS and Windows** (GitHub-hosted runners). Each run is appended to
`benchmarks/<os>.json`; this report shows the latest run per OS and the recent history.

_Last update: 2026-10-25 08:03 UTC_

## Latest run per OS

| Metric | **macos-14** | **ubuntu-24.04** | **windows-2022** | Unit |
|---|---|---|---|---|
| CPU | 11.0 M ops/s | 12.7 M ops/s | 6.9 M ops/s |
| RAM | 17301 MB/s | 23884 MB/s | 22296 MB/s |
| Disk write | 4754 MB/s | 179 MB/s | 114 MB/s |
| Disk read | 2196 MB/s | 11868 MB/s | 2968 MB/s |
| Elapsed | 1.2 s | 1.3 s | 1.3 s |
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
| 2026-10-12T10:08:22Z | 9.06  | 12190  | 1477  | 1391  | 1.2  |
| 2026-10-13T10:01:54Z | 10.03  | 14066  | 1768  | 4926  | 1.2  |
| 2026-10-14T08:19:51Z | 7.91  | 12428  | 683  | 5283  | 1.3  |
| 2026-10-15T07:56:51Z | 8.31  | 10981  | 708  | 6583  | 1.3  |
| 2026-10-16T07:50:48Z | 9.35  | 12928  | 3473  | 1988  | 1.2  |
| 2026-10-17T07:28:07Z | 8.42  | 11657  | 1090  | 8386  | 1.2  |
| 2026-10-18T07:43:09Z | 7.94  | 17780  | 815  | 4954  | 1.2  |
| 2026-10-19T08:25:20Z | 9.53  | 18787  | 1861  | 995  | 1.3  |
| 2026-10-20T08:07:53Z | 9.90  | 18711  | 1962  | 8308  | 1.2  |
| 2026-10-21T08:13:31Z | 10.88  | 22409  | 1256  | 2063  | 1.2  |
| 2026-10-22T08:15:04Z | 6.73  | 10138  | 1104  | 3808  | 1.3  |
| 2026-10-23T08:12:17Z | 7.40  | 15761  | 1928  | 7656  | 1.2  |
| 2026-10-24T07:50:40Z | 9.57  | 14499  | 1751  | 8821  | 1.2  |
| 2026-10-25T08:03:28Z | 11.04  | 17301  | 4754  | 2196  | 1.2  |

### ubuntu-24.04

| Date (UTC) | CPU (M ops/s) | RAM (MB/s) | Write (MB/s) | Read (MB/s) | Elapsed (s) |
|---|---|---|---|---|---|
| 2026-10-12T10:08:22Z | 7.04  | 22391  | 1473  | 6484  | 1.1  |
| 2026-10-13T10:01:54Z | 8.31  | 20483  | 148  | 9199  | 1.3  |
| 2026-10-14T08:19:51Z | 6.95  | 19786  | 1227  | 6077  | 1.2  |
| 2026-10-15T07:56:51Z | 6.93  | 22810  | 1320  | 7716  | 1.2  |
| 2026-10-16T07:50:48Z | 6.96  | 20318  | 1665  | 7672  | 1.2  |
| 2026-10-17T07:28:07Z | 7.06  | 21122  | 1465  | 6796  | 1.2  |
| 2026-10-18T07:43:09Z | 9.62  | 10792  | 153  | 5748  | 1.4  |
| 2026-10-19T08:25:20Z | 7.01  | 24536  | 1314  | 7808  | 1.1  |
| 2026-10-20T08:07:53Z | 7.08  | 21586  | 1403  | 6586  | 1.2  |
| 2026-10-21T08:13:31Z | 7.00  | 21557  | 1582  | 7023  | 1.2  |
| 2026-10-22T08:15:04Z | 8.69  | 7035  | 136  | 5346  | 1.4  |
| 2026-10-23T08:12:17Z | 7.05  | 21344  | 1514  | 6857  | 1.1  |
| 2026-10-24T07:50:40Z | 6.87  | 26333  | 1359  | 7628  | 1.1  |
| 2026-10-25T08:03:28Z | 12.71  | 23884  | 179  | 11868  | 1.3  |

### windows-2022

| Date (UTC) | CPU (M ops/s) | RAM (MB/s) | Write (MB/s) | Read (MB/s) | Elapsed (s) |
|---|---|---|---|---|---|
| 2026-10-12T10:08:22Z | 6.49  | 26797  | 108  | 3079  | 1.4  |
| 2026-10-13T10:01:54Z | 8.19  | 23741  | 65  | 3563  | 1.6  |
| 2026-10-14T08:19:51Z | 10.76  | 33139  | 134  | 3802  | 1.3  |
| 2026-10-15T07:56:51Z | 7.06  | 21746  | 126  | 3051  | 1.3  |
| 2026-10-16T07:50:48Z | 5.69  | 22210  | 131  | 3092  | 1.3  |
| 2026-10-17T07:28:07Z | 9.09  | 10572  | 78  | 1718  | 1.5  |
| 2026-10-18T07:43:09Z | 8.76  | 28144  | 164  | 3821  | 1.2  |
| 2026-10-19T08:25:20Z | 6.84  | 25434  | 96  | 3120  | 1.4  |
| 2026-10-20T08:07:53Z | 7.16  | 21376  | 73  | 3089  | 1.5  |
| 2026-10-21T08:13:31Z | 6.36  | 20219  | 75  | 2678  | 1.5  |
| 2026-10-22T08:15:04Z | 6.74  | 22656  | 130  | 3107  | 1.3  |
| 2026-10-23T08:12:17Z | 6.80  | 20003  | 97  | 2968  | 1.4  |
| 2026-10-24T07:50:40Z | 6.30  | 26797  | 122  | 3154  | 1.3  |
| 2026-10-25T08:03:28Z | 6.86  | 22296  | 114  | 2968  | 1.3  |

