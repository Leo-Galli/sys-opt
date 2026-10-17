# 📊 sys-opt Nightly Benchmark

Automated **CPU / RAM / disk** benchmarks (light stress via `psutil`) run every night on
**Linux, macOS and Windows** (GitHub-hosted runners). Each run is appended to
`benchmarks/<os>.json`; this report shows the latest run per OS and the recent history.

_Last update: 2026-10-17 07:28 UTC_

## Latest run per OS

| Metric | **macos-14** | **ubuntu-24.04** | **windows-2022** | Unit |
|---|---|---|---|---|
| CPU | 8.4 M ops/s | 7.1 M ops/s | 9.1 M ops/s |
| RAM | 11657 MB/s | 21122 MB/s | 10572 MB/s |
| Disk write | 1090 MB/s | 1465 MB/s | 78 MB/s |
| Disk read | 8386 MB/s | 6796 MB/s | 1718 MB/s |
| Elapsed | 1.2 s | 1.2 s | 1.5 s |
| **Overall verdict** | 🟢 Good | 🟢 Good | 🔴 Below average |

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
| 2026-10-04T09:17:35Z | 8.96  | 13934  | 848  | 3956  | 1.3  |
| 2026-10-05T09:56:35Z | 9.42  | 17628  | 1865  | 11336  | 1.2  |
| 2026-10-06T09:43:13Z | 9.10  | 13274  | 808  | 1421  | 1.2  |
| 2026-10-07T09:41:30Z | 9.55  | 13777  | 739  | 4517  | 1.3  |
| 2026-10-08T09:51:56Z | 9.88  | 18944  | 2222  | 9132  | 1.1  |
| 2026-10-09T09:56:00Z | 9.53  | 16142  | 1326  | 6560  | 1.2  |
| 2026-10-10T09:19:40Z | 6.97  | 11100  | 1209  | 4201  | 1.3  |
| 2026-10-11T09:36:44Z | 8.55  | 10678  | 2466  | 8664  | 1.3  |
| 2026-10-12T10:08:22Z | 9.06  | 12190  | 1477  | 1391  | 1.2  |
| 2026-10-13T10:01:54Z | 10.03  | 14066  | 1768  | 4926  | 1.2  |
| 2026-10-14T08:19:51Z | 7.91  | 12428  | 683  | 5283  | 1.3  |
| 2026-10-15T07:56:51Z | 8.31  | 10981  | 708  | 6583  | 1.3  |
| 2026-10-16T07:50:48Z | 9.35  | 12928  | 3473  | 1988  | 1.2  |
| 2026-10-17T07:28:07Z | 8.42  | 11657  | 1090  | 8386  | 1.2  |

### ubuntu-24.04

| Date (UTC) | CPU (M ops/s) | RAM (MB/s) | Write (MB/s) | Read (MB/s) | Elapsed (s) |
|---|---|---|---|---|---|
| 2026-10-04T09:17:35Z | 6.94  | 23419  | 1543  | 7661  | 1.1  |
| 2026-10-05T09:56:35Z | 8.92  | 8890  | 159  | 6336  | 1.4  |
| 2026-10-06T09:43:13Z | 6.99  | 24496  | 1544  | 7156  | 1.1  |
| 2026-10-07T09:41:30Z | 8.89  | 19186  | 146  | 9781  | 1.3  |
| 2026-10-08T09:51:56Z | 12.37  | 25084  | 185  | 11625  | 1.3  |
| 2026-10-09T09:56:00Z | 6.93  | 22769  | 1489  | 7122  | 1.2  |
| 2026-10-10T09:19:40Z | 7.08  | 21520  | 1208  | 6401  | 1.2  |
| 2026-10-11T09:36:44Z | 6.96  | 23635  | 1486  | 7374  | 1.2  |
| 2026-10-12T10:08:22Z | 7.04  | 22391  | 1473  | 6484  | 1.1  |
| 2026-10-13T10:01:54Z | 8.31  | 20483  | 148  | 9199  | 1.3  |
| 2026-10-14T08:19:51Z | 6.95  | 19786  | 1227  | 6077  | 1.2  |
| 2026-10-15T07:56:51Z | 6.93  | 22810  | 1320  | 7716  | 1.2  |
| 2026-10-16T07:50:48Z | 6.96  | 20318  | 1665  | 7672  | 1.2  |
| 2026-10-17T07:28:07Z | 7.06  | 21122  | 1465  | 6796  | 1.2  |

### windows-2022

| Date (UTC) | CPU (M ops/s) | RAM (MB/s) | Write (MB/s) | Read (MB/s) | Elapsed (s) |
|---|---|---|---|---|---|
| 2026-10-04T09:17:35Z | 7.13  | 26881  | 121  | 3630  | 1.3  |
| 2026-10-05T09:56:35Z | 6.79  | 25798  | 116  | 2996  | 1.3  |
| 2026-10-06T09:43:13Z | 10.60  | 15206  | 55  | 1867  | 1.7  |
| 2026-10-07T09:41:30Z | 7.20  | 22612  | 103  | 3095  | 1.4  |
| 2026-10-08T09:51:56Z | 6.85  | 21123  | 102  | 1958  | 1.4  |
| 2026-10-09T09:56:00Z | 8.06  | 24156  | 104  | 3505  | 1.4  |
| 2026-10-10T09:19:40Z | 5.77  | 22658  | 109  | 3457  | 1.4  |
| 2026-10-11T09:36:44Z | 9.01  | 12959  | 62  | 1671  | 1.6  |
| 2026-10-12T10:08:22Z | 6.49  | 26797  | 108  | 3079  | 1.4  |
| 2026-10-13T10:01:54Z | 8.19  | 23741  | 65  | 3563  | 1.6  |
| 2026-10-14T08:19:51Z | 10.76  | 33139  | 134  | 3802  | 1.3  |
| 2026-10-15T07:56:51Z | 7.06  | 21746  | 126  | 3051  | 1.3  |
| 2026-10-16T07:50:48Z | 5.69  | 22210  | 131  | 3092  | 1.3  |
| 2026-10-17T07:28:07Z | 9.09  | 10572  | 78  | 1718  | 1.5  |

