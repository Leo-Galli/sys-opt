# 📊 sys-opt Nightly Benchmark

Automated **CPU / RAM / disk** benchmarks (light stress via `psutil`) run every night on
**Linux, macOS and Windows** (GitHub-hosted runners). Each run is appended to
`benchmarks/<os>.json`; this report shows the latest run per OS and the recent history.

_Last update: 2026-10-30 09:30 UTC_

## Latest run per OS

| Metric | **macos-14** | **ubuntu-24.04** | **windows-2022** | Unit |
|---|---|---|---|---|
| CPU | 11.6 M ops/s | 7.1 M ops/s | 9.8 M ops/s |
| RAM | 19975 MB/s | 22619 MB/s | 14887 MB/s |
| Disk write | 4302 MB/s | 1555 MB/s | 102 MB/s |
| Disk read | 13777 MB/s | 6966 MB/s | 1806 MB/s |
| Elapsed | 1.1 s | 1.2 s | 1.4 s |
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
| 2026-10-17T07:28:07Z | 8.42  | 11657  | 1090  | 8386  | 1.2  |
| 2026-10-18T07:43:09Z | 7.94  | 17780  | 815  | 4954  | 1.2  |
| 2026-10-19T08:25:20Z | 9.53  | 18787  | 1861  | 995  | 1.3  |
| 2026-10-20T08:07:53Z | 9.90  | 18711  | 1962  | 8308  | 1.2  |
| 2026-10-21T08:13:31Z | 10.88  | 22409  | 1256  | 2063  | 1.2  |
| 2026-10-22T08:15:04Z | 6.73  | 10138  | 1104  | 3808  | 1.3  |
| 2026-10-23T08:12:17Z | 7.40  | 15761  | 1928  | 7656  | 1.2  |
| 2026-10-24T07:50:40Z | 9.57  | 14499  | 1751  | 8821  | 1.2  |
| 2026-10-25T08:03:28Z | 11.04  | 17301  | 4754  | 2196  | 1.2  |
| 2026-10-26T08:26:35Z | 7.84  | 13002  | 1574  | 4088  | 1.2  |
| 2026-10-27T08:34:50Z | 9.16  | 12385  | 1106  | 4887  | 1.4  |
| 2026-10-28T09:14:54Z | 7.55  | 16401  | 1464  | 6639  | 1.2  |
| 2026-10-29T09:15:26Z | 9.64  | 20214  | 3742  | 11775  | 1.2  |
| 2026-10-30T09:30:46Z | 11.56  | 19975  | 4302  | 13777  | 1.1  |

### ubuntu-24.04

| Date (UTC) | CPU (M ops/s) | RAM (MB/s) | Write (MB/s) | Read (MB/s) | Elapsed (s) |
|---|---|---|---|---|---|
| 2026-10-17T07:28:07Z | 7.06  | 21122  | 1465  | 6796  | 1.2  |
| 2026-10-18T07:43:09Z | 9.62  | 10792  | 153  | 5748  | 1.4  |
| 2026-10-19T08:25:20Z | 7.01  | 24536  | 1314  | 7808  | 1.1  |
| 2026-10-20T08:07:53Z | 7.08  | 21586  | 1403  | 6586  | 1.2  |
| 2026-10-21T08:13:31Z | 7.00  | 21557  | 1582  | 7023  | 1.2  |
| 2026-10-22T08:15:04Z | 8.69  | 7035  | 136  | 5346  | 1.4  |
| 2026-10-23T08:12:17Z | 7.05  | 21344  | 1514  | 6857  | 1.1  |
| 2026-10-24T07:50:40Z | 6.87  | 26333  | 1359  | 7628  | 1.1  |
| 2026-10-25T08:03:28Z | 12.71  | 23884  | 179  | 11868  | 1.3  |
| 2026-10-26T08:26:35Z | 7.01  | 22323  | 1426  | 6879  | 1.1  |
| 2026-10-27T08:34:50Z | 12.24  | 24160  | 187  | 12889  | 1.3  |
| 2026-10-28T09:14:54Z | 12.73  | 10785  | 166  | 6893  | 1.4  |
| 2026-10-29T09:15:26Z | 12.40  | 23420  | 162  | 11106  | 1.4  |
| 2026-10-30T09:30:46Z | 7.10  | 22619  | 1555  | 6966  | 1.2  |

### windows-2022

| Date (UTC) | CPU (M ops/s) | RAM (MB/s) | Write (MB/s) | Read (MB/s) | Elapsed (s) |
|---|---|---|---|---|---|
| 2026-10-17T07:28:07Z | 9.09  | 10572  | 78  | 1718  | 1.5  |
| 2026-10-18T07:43:09Z | 8.76  | 28144  | 164  | 3821  | 1.2  |
| 2026-10-19T08:25:20Z | 6.84  | 25434  | 96  | 3120  | 1.4  |
| 2026-10-20T08:07:53Z | 7.16  | 21376  | 73  | 3089  | 1.5  |
| 2026-10-21T08:13:31Z | 6.36  | 20219  | 75  | 2678  | 1.5  |
| 2026-10-22T08:15:04Z | 6.74  | 22656  | 130  | 3107  | 1.3  |
| 2026-10-23T08:12:17Z | 6.80  | 20003  | 97  | 2968  | 1.4  |
| 2026-10-24T07:50:40Z | 6.30  | 26797  | 122  | 3154  | 1.3  |
| 2026-10-25T08:03:28Z | 6.86  | 22296  | 114  | 2968  | 1.3  |
| 2026-10-26T08:26:35Z | 9.12  | 14334  | 103  | 1804  | 1.4  |
| 2026-10-27T08:34:50Z | 6.80  | 22952  | 117  | 3069  | 1.3  |
| 2026-10-28T09:14:54Z | 6.94  | 22576  | 114  | 3179  | 1.3  |
| 2026-10-29T09:15:26Z | 10.64  | 36110  | 123  | 3423  | 1.3  |
| 2026-10-30T09:30:46Z | 9.76  | 14887  | 102  | 1806  | 1.4  |

