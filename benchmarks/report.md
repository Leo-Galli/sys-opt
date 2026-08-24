# 📊 sys-opt Nightly Benchmark

Automated **CPU / RAM / disk** benchmarks (light stress via `psutil`) run every night on
**Linux, macOS and Windows** (GitHub-hosted runners). Each run is appended to
`benchmarks/<os>.json`; this report shows the latest run per OS and the recent history.

_Last update: 2026-08-24 03:50 UTC_

## Latest run per OS

| Metric | **macos-14** | **ubuntu-24.04** | **windows-2022** | Unit |
|---|---|---|---|---|
| CPU | 9.8 M ops/s | 10.0 M ops/s | 6.8 M ops/s |
| RAM | 16653 MB/s | 12806 MB/s | 24286 MB/s |
| Disk write | 1963 MB/s | 153 MB/s | 123 MB/s |
| Disk read | 5172 MB/s | 5689 MB/s | 3106 MB/s |
| Elapsed | 1.2 s | 1.4 s | 1.3 s |
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
| 2026-08-11T04:15:56Z | 9.67  | 20327  | 2757  | 11453  | 1.2  |
| 2026-08-12T04:44:48Z | 9.80  | 23396  | 1952  | 2031  | 1.2  |
| 2026-08-13T04:48:23Z | 10.36  | 16892  | 1808  | 9410  | 1.2  |
| 2026-08-14T04:45:21Z | 10.46  | 21391  | 1949  | 1667  | 1.2  |
| 2026-08-15T03:34:27Z | 10.30  | 16472  | 2213  | 10457  | 1.2  |
| 2026-08-16T03:43:41Z | 10.67  | 18051  | 1798  | 1954  | 1.2  |
| 2026-08-17T03:45:27Z | 11.00  | 20712  | 1999  | 5220  | 1.1  |
| 2026-08-18T03:40:14Z | 7.56  | 14749  | 1093  | 3410  | 1.3  |
| 2026-08-19T03:42:25Z | 7.39  | 14298  | 1254  | 9066  | 1.3  |
| 2026-08-20T03:42:02Z | 9.09  | 17037  | 1401  | 2163  | 1.2  |
| 2026-08-21T03:46:21Z | 10.24  | 21501  | 1282  | 2035  | 1.3  |
| 2026-08-22T03:37:39Z | 10.25  | 22949  | 4157  | 10086  | 1.2  |
| 2026-08-23T03:45:49Z | 10.38  | 25021  | 1379  | 2039  | 1.2  |
| 2026-08-24T03:50:38Z | 9.83  | 16653  | 1963  | 5172  | 1.2  |

### ubuntu-24.04

| Date (UTC) | CPU (M ops/s) | RAM (MB/s) | Write (MB/s) | Read (MB/s) | Elapsed (s) |
|---|---|---|---|---|---|
| 2026-08-11T04:15:56Z | 7.37  | 17329  | 1863  | 8004  | 1.2  |
| 2026-08-12T04:44:48Z | 7.30  | 17610  | 2007  | 7987  | 1.2  |
| 2026-08-13T04:48:23Z | 12.40  | 24468  | 126  | 12311  | 1.4  |
| 2026-08-14T04:45:21Z | 7.33  | 19622  | 1893  | 7792  | 1.2  |
| 2026-08-15T03:34:27Z | 7.08  | 23093  | 1518  | 7839  | 1.1  |
| 2026-08-16T03:43:41Z | 6.95  | 22724  | 1358  | 6736  | 1.2  |
| 2026-08-17T03:45:27Z | 10.16  | 11933  | 160  | 5829  | 1.3  |
| 2026-08-18T03:40:14Z | 8.93  | 9194  | 135  | 5449  | 1.4  |
| 2026-08-19T03:42:25Z | 9.34  | 20015  | 200  | 9660  | 1.3  |
| 2026-08-20T03:42:02Z | 7.11  | 23978  | 1505  | 7238  | 1.1  |
| 2026-08-21T03:46:21Z | 6.99  | 22100  | 1464  | 7195  | 1.1  |
| 2026-08-22T03:37:39Z | 8.53  | 7959  | 140  | 5521  | 1.4  |
| 2026-08-23T03:45:49Z | 7.39  | 18548  | 1900  | 7464  | 1.2  |
| 2026-08-24T03:50:38Z | 10.00  | 12806  | 153  | 5689  | 1.4  |

### windows-2022

| Date (UTC) | CPU (M ops/s) | RAM (MB/s) | Write (MB/s) | Read (MB/s) | Elapsed (s) |
|---|---|---|---|---|---|
| 2026-08-11T04:15:56Z | 6.84  | 19805  | 95  | 2900  | 1.4  |
| 2026-08-12T04:44:48Z | 11.80  | 12511  | 65  | 1936  | 1.6  |
| 2026-08-13T04:48:23Z | 6.83  | 23355  | 121  | 3044  | 1.3  |
| 2026-08-14T04:45:21Z | 6.84  | 21747  | 138  | 3101  | 1.3  |
| 2026-08-15T03:34:27Z | 6.84  | 19866  | 129  | 2997  | 1.3  |
| 2026-08-16T03:43:41Z | 6.87  | 24649  | 50  | 3486  | 1.7  |
| 2026-08-17T03:45:27Z | 6.86  | 20992  | 120  | 3255  | 1.3  |
| 2026-08-18T03:40:14Z | 9.04  | 11628  | 90  | 1746  | 1.5  |
| 2026-08-19T03:42:25Z | 12.79  | 12519  | 91  | 2065  | 1.5  |
| 2026-08-20T03:42:02Z | 6.81  | 20109  | 111  | 2842  | 1.4  |
| 2026-08-21T03:46:21Z | 6.65  | 23035  | 88  | 3134  | 1.7  |
| 2026-08-22T03:37:39Z | 7.21  | 19474  | 108  | 3047  | 1.4  |
| 2026-08-23T03:45:49Z | 7.14  | 20602  | 130  | 3052  | 1.3  |
| 2026-08-24T03:50:38Z | 6.75  | 24286  | 123  | 3106  | 1.3  |

