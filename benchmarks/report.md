# 📊 sys-opt Nightly Benchmark

Automated **CPU / RAM / disk** benchmarks (light stress via `psutil`) run every night on
**Linux, macOS and Windows** (GitHub-hosted runners). Each run is appended to
`benchmarks/<os>.json`; this report shows the latest run per OS and the recent history.

_Last update: 2026-08-30 08:51 UTC_

## Latest run per OS

| Metric | **macos-14** | **ubuntu-24.04** | **windows-2022** | Unit |
|---|---|---|---|---|
| CPU | 10.5 M ops/s | 7.4 M ops/s | 7.2 M ops/s |
| RAM | 21042 MB/s | 18677 MB/s | 22179 MB/s |
| Disk write | 3873 MB/s | 1880 MB/s | 81 MB/s |
| Disk read | 9042 MB/s | 7383 MB/s | 2872 MB/s |
| Elapsed | 1.2 s | 1.2 s | 1.5 s |
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
| 2026-08-17T03:45:27Z | 11.00  | 20712  | 1999  | 5220  | 1.1  |
| 2026-08-18T03:40:14Z | 7.56  | 14749  | 1093  | 3410  | 1.3  |
| 2026-08-19T03:42:25Z | 7.39  | 14298  | 1254  | 9066  | 1.3  |
| 2026-08-20T03:42:02Z | 9.09  | 17037  | 1401  | 2163  | 1.2  |
| 2026-08-21T03:46:21Z | 10.24  | 21501  | 1282  | 2035  | 1.3  |
| 2026-08-22T03:37:39Z | 10.25  | 22949  | 4157  | 10086  | 1.2  |
| 2026-08-23T03:45:49Z | 10.38  | 25021  | 1379  | 2039  | 1.2  |
| 2026-08-24T03:50:38Z | 9.83  | 16653  | 1963  | 5172  | 1.2  |
| 2026-08-25T03:44:18Z | 8.81  | 15659  | 1237  | 1566  | 1.3  |
| 2026-08-26T03:50:15Z | 10.43  | 20462  | 1450  | 2156  | 1.2  |
| 2026-08-27T13:39:30Z | 7.37  | 16916  | 1207  | 6211  | 1.3  |
| 2026-08-28T14:49:57Z | 11.22  | 20835  | 3891  | 2292  | 1.2  |
| 2026-08-29T09:40:25Z | 7.54  | 17857  | 945  | 5213  | 1.3  |
| 2026-08-30T08:51:54Z | 10.51  | 21042  | 3873  | 9042  | 1.2  |

### ubuntu-24.04

| Date (UTC) | CPU (M ops/s) | RAM (MB/s) | Write (MB/s) | Read (MB/s) | Elapsed (s) |
|---|---|---|---|---|---|
| 2026-08-17T03:45:27Z | 10.16  | 11933  | 160  | 5829  | 1.3  |
| 2026-08-18T03:40:14Z | 8.93  | 9194  | 135  | 5449  | 1.4  |
| 2026-08-19T03:42:25Z | 9.34  | 20015  | 200  | 9660  | 1.3  |
| 2026-08-20T03:42:02Z | 7.11  | 23978  | 1505  | 7238  | 1.1  |
| 2026-08-21T03:46:21Z | 6.99  | 22100  | 1464  | 7195  | 1.1  |
| 2026-08-22T03:37:39Z | 8.53  | 7959  | 140  | 5521  | 1.4  |
| 2026-08-23T03:45:49Z | 7.39  | 18548  | 1900  | 7464  | 1.2  |
| 2026-08-24T03:50:38Z | 10.00  | 12806  | 153  | 5689  | 1.4  |
| 2026-08-25T03:44:18Z | 8.49  | 10113  | 1403  | 4880  | 1.2  |
| 2026-08-26T03:50:15Z | 7.35  | 18090  | 1887  | 7077  | 1.2  |
| 2026-08-27T13:39:30Z | 7.00  | 22654  | 1498  | 6131  | 1.1  |
| 2026-08-28T14:49:57Z | 6.99  | 18574  | 1072  | 5270  | 1.2  |
| 2026-08-29T09:40:25Z | 7.00  | 21477  | 1239  | 6391  | 1.2  |
| 2026-08-30T08:51:54Z | 7.41  | 18677  | 1880  | 7383  | 1.2  |

### windows-2022

| Date (UTC) | CPU (M ops/s) | RAM (MB/s) | Write (MB/s) | Read (MB/s) | Elapsed (s) |
|---|---|---|---|---|---|
| 2026-08-17T03:45:27Z | 6.86  | 20992  | 120  | 3255  | 1.3  |
| 2026-08-18T03:40:14Z | 9.04  | 11628  | 90  | 1746  | 1.5  |
| 2026-08-19T03:42:25Z | 12.79  | 12519  | 91  | 2065  | 1.5  |
| 2026-08-20T03:42:02Z | 6.81  | 20109  | 111  | 2842  | 1.4  |
| 2026-08-21T03:46:21Z | 6.65  | 23035  | 88  | 3134  | 1.7  |
| 2026-08-22T03:37:39Z | 7.21  | 19474  | 108  | 3047  | 1.4  |
| 2026-08-23T03:45:49Z | 7.14  | 20602  | 130  | 3052  | 1.3  |
| 2026-08-24T03:50:38Z | 6.75  | 24286  | 123  | 3106  | 1.3  |
| 2026-08-25T03:44:18Z | 9.25  | 12720  | 2  | 1723  | 16.6  |
| 2026-08-26T03:50:15Z | 7.19  | 22184  | 83  | 3030  | 1.4  |
| 2026-08-27T13:39:30Z | 7.18  | 22265  | 160  | 3122  | 1.3  |
| 2026-08-28T14:49:57Z | 6.74  | 24600  | 91  | 2958  | 1.4  |
| 2026-08-29T09:40:25Z | 12.79  | 12494  | 114  | 2037  | 1.4  |
| 2026-08-30T08:51:54Z | 7.16  | 22179  | 81  | 2872  | 1.5  |

