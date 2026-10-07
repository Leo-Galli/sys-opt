# 📊 sys-opt Nightly Benchmark

Automated **CPU / RAM / disk** benchmarks (light stress via `psutil`) run every night on
**Linux, macOS and Windows** (GitHub-hosted runners). Each run is appended to
`benchmarks/<os>.json`; this report shows the latest run per OS and the recent history.

_Last update: 2026-10-07 09:41 UTC_

## Latest run per OS

| Metric | **macos-14** | **ubuntu-24.04** | **windows-2022** | Unit |
|---|---|---|---|---|
| CPU | 9.6 M ops/s | 8.9 M ops/s | 7.2 M ops/s |
| RAM | 13777 MB/s | 19186 MB/s | 22612 MB/s |
| Disk write | 739 MB/s | 146 MB/s | 103 MB/s |
| Disk read | 4517 MB/s | 9781 MB/s | 3095 MB/s |
| Elapsed | 1.3 s | 1.3 s | 1.4 s |
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
| 2026-09-24T08:04:39Z | 7.07  | 12949  | 697  | 3256  | 1.3  |
| 2026-09-25T08:28:56Z | 9.55  | 15385  | 1540  | 8480  | 1.2  |
| 2026-09-26T08:15:44Z | 10.70  | 19327  | 2066  | 7540  | 1.2  |
| 2026-09-27T08:52:44Z | 10.32  | 14771  | 2258  | 9841  | 1.2  |
| 2026-09-28T09:17:27Z | 8.68  | 15481  | 1079  | 8357  | 1.2  |
| 2026-09-29T09:24:54Z | 7.10  | 11062  | 920  | 3385  | 1.3  |
| 2026-09-30T09:14:57Z | 9.41  | 15045  | 1548  | 8548  | 1.2  |
| 2026-10-01T09:42:50Z | 9.13  | 13916  | 2817  | 7817  | 1.2  |
| 2026-10-02T09:17:10Z | 8.73  | 11539  | 1353  | 4460  | 1.3  |
| 2026-10-03T08:49:00Z | 8.72  | 14649  | 906  | 5974  | 1.2  |
| 2026-10-04T09:17:35Z | 8.96  | 13934  | 848  | 3956  | 1.3  |
| 2026-10-05T09:56:35Z | 9.42  | 17628  | 1865  | 11336  | 1.2  |
| 2026-10-06T09:43:13Z | 9.10  | 13274  | 808  | 1421  | 1.2  |
| 2026-10-07T09:41:30Z | 9.55  | 13777  | 739  | 4517  | 1.3  |

### ubuntu-24.04

| Date (UTC) | CPU (M ops/s) | RAM (MB/s) | Write (MB/s) | Read (MB/s) | Elapsed (s) |
|---|---|---|---|---|---|
| 2026-09-24T08:04:39Z | 6.68  | 23319  | 1525  | 8237  | 1.1  |
| 2026-09-25T08:28:56Z | 6.94  | 22669  | 1226  | 8175  | 1.2  |
| 2026-09-26T08:15:44Z | 8.34  | 12525  | 1529  | 6917  | 1.2  |
| 2026-09-27T08:52:44Z | 6.95  | 23853  | 1531  | 8433  | 1.1  |
| 2026-09-28T09:17:27Z | 6.96  | 20639  | 1315  | 7573  | 1.2  |
| 2026-09-29T09:24:54Z | 6.73  | 20747  | 62  | 7355  | 1.6  |
| 2026-09-30T09:14:57Z | 7.04  | 25024  | 1568  | 7064  | 1.1  |
| 2026-10-01T09:42:50Z | 7.07  | 18482  | 1600  | 6571  | 1.2  |
| 2026-10-02T09:17:10Z | 13.25  | 25002  | 186  | 12016  | 1.3  |
| 2026-10-03T08:49:00Z | 11.71  | 21232  | 184  | 11330  | 1.3  |
| 2026-10-04T09:17:35Z | 6.94  | 23419  | 1543  | 7661  | 1.1  |
| 2026-10-05T09:56:35Z | 8.92  | 8890  | 159  | 6336  | 1.4  |
| 2026-10-06T09:43:13Z | 6.99  | 24496  | 1544  | 7156  | 1.1  |
| 2026-10-07T09:41:30Z | 8.89  | 19186  | 146  | 9781  | 1.3  |

### windows-2022

| Date (UTC) | CPU (M ops/s) | RAM (MB/s) | Write (MB/s) | Read (MB/s) | Elapsed (s) |
|---|---|---|---|---|---|
| 2026-09-24T08:04:39Z | 6.74  | 22889  | 104  | 2932  | 1.4  |
| 2026-09-25T08:28:56Z | 6.35  | 24007  | 126  | 2930  | 1.3  |
| 2026-09-26T08:15:44Z | 11.36  | 35834  | 58  | 3633  | 1.6  |
| 2026-09-27T08:52:44Z | 7.22  | 24142  | 118  | 3076  | 1.3  |
| 2026-09-28T09:17:27Z | 8.69  | 26216  | 89  | 3489  | 1.4  |
| 2026-09-29T09:24:54Z | 7.18  | 18987  | 106  | 2968  | 1.4  |
| 2026-09-30T09:14:57Z | 9.18  | 10215  | 74  | 1747  | 1.6  |
| 2026-10-01T09:42:50Z | 7.16  | 21919  | 90  | 2805  | 1.4  |
| 2026-10-02T09:17:10Z | 8.74  | 26156  | 63  | 3552  | 1.6  |
| 2026-10-03T08:49:00Z | 7.13  | 22596  | 146  | 3072  | 1.3  |
| 2026-10-04T09:17:35Z | 7.13  | 26881  | 121  | 3630  | 1.3  |
| 2026-10-05T09:56:35Z | 6.79  | 25798  | 116  | 2996  | 1.3  |
| 2026-10-06T09:43:13Z | 10.60  | 15206  | 55  | 1867  | 1.7  |
| 2026-10-07T09:41:30Z | 7.20  | 22612  | 103  | 3095  | 1.4  |

