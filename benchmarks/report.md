# 📊 sys-opt Nightly Benchmark

Automated **CPU / RAM / disk** benchmarks (light stress via `psutil`) run every night on
**Linux, macOS and Windows** (GitHub-hosted runners). Each run is appended to
`benchmarks/<os>.json`; this report shows the latest run per OS and the recent history.

_Last update: 2026-10-03 08:49 UTC_

## Latest run per OS

| Metric | **macos-14** | **ubuntu-24.04** | **windows-2022** | Unit |
|---|---|---|---|---|
| CPU | 8.7 M ops/s | 11.7 M ops/s | 7.1 M ops/s |
| RAM | 14649 MB/s | 21232 MB/s | 22596 MB/s |
| Disk write | 906 MB/s | 184 MB/s | 146 MB/s |
| Disk read | 5974 MB/s | 11330 MB/s | 3072 MB/s |
| Elapsed | 1.2 s | 1.3 s | 1.3 s |
| **Overall verdict** | 🟢 Good | 🟡 Average | 🔴 Below average |

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
| 2026-09-20T08:14:16Z | 8.72  | 13399  | 1398  | 4903  | 1.2  |
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

### ubuntu-24.04

| Date (UTC) | CPU (M ops/s) | RAM (MB/s) | Write (MB/s) | Read (MB/s) | Elapsed (s) |
|---|---|---|---|---|---|
| 2026-09-20T08:14:16Z | 7.21  | 16389  | 1640  | 8087  | 1.2  |
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

### windows-2022

| Date (UTC) | CPU (M ops/s) | RAM (MB/s) | Write (MB/s) | Read (MB/s) | Elapsed (s) |
|---|---|---|---|---|---|
| 2026-09-20T08:14:16Z | 6.93  | 22230  | 102  | 2549  | 1.4  |
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

