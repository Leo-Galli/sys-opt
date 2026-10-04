# 📊 sys-opt Nightly Benchmark

Automated **CPU / RAM / disk** benchmarks (light stress via `psutil`) run every night on
**Linux, macOS and Windows** (GitHub-hosted runners). Each run is appended to
`benchmarks/<os>.json`; this report shows the latest run per OS and the recent history.

_Last update: 2026-10-04 09:17 UTC_

## Latest run per OS

| Metric | **macos-14** | **ubuntu-24.04** | **windows-2022** | Unit |
|---|---|---|---|---|
| CPU | 9.0 M ops/s | 6.9 M ops/s | 7.1 M ops/s |
| RAM | 13934 MB/s | 23419 MB/s | 26881 MB/s |
| Disk write | 848 MB/s | 1543 MB/s | 121 MB/s |
| Disk read | 3956 MB/s | 7661 MB/s | 3630 MB/s |
| Elapsed | 1.3 s | 1.1 s | 1.3 s |
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
| 2026-09-21T08:31:01Z | 8.30  | 14053  | 990  | 6934  | 1.2  |
| 2026-09-22T08:11:44Z | 8.27  | 17436  | 1150  | 3551  | 1.2  |
| 2026-09-23T08:13:51Z | 10.96  | 22420  | 4187  | 13164  | 1.2  |
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

### ubuntu-24.04

| Date (UTC) | CPU (M ops/s) | RAM (MB/s) | Write (MB/s) | Read (MB/s) | Elapsed (s) |
|---|---|---|---|---|---|
| 2026-09-21T08:31:01Z | 8.89  | 10717  | 1438  | 5858  | 1.2  |
| 2026-09-22T08:11:44Z | 7.00  | 21479  | 1429  | 7031  | 1.2  |
| 2026-09-23T08:13:51Z | 7.02  | 22376  | 1550  | 7074  | 1.1  |
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

### windows-2022

| Date (UTC) | CPU (M ops/s) | RAM (MB/s) | Write (MB/s) | Read (MB/s) | Elapsed (s) |
|---|---|---|---|---|---|
| 2026-09-21T08:31:01Z | 7.21  | 22426  | 91  | 2996  | 1.4  |
| 2026-09-22T08:11:44Z | 8.62  | 9970  | 51  | 1748  | 2.1  |
| 2026-09-23T08:13:51Z | 7.19  | 23130  | 51  | 3088  | 1.7  |
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

