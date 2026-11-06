# Task 24. Hardware audit and discrepancy

Audit collected with Windows CIM on 6 November 2026. The benchmark environment is recorded separately from the older lab's host profile, whose physical-core count is not used here.

| Property | Evidence / value |
|---|---|
|CPU|11th Gen Intel Core i5-11400H @ 2.70 GHz, CIM Win32_Processor|
|Cores / logical threads|6 / 12, CIM|
|L1 cache|Not exposed by the CIM query used; capacity and associativity not independently audited|
|L2 cache|7680 KiB aggregate reported by CIM (7.5 MiB)|
|L3 cache|12288 KiB reported by CIM (12 MiB)|
|Memory modules|2 x 8589934592 bytes = 16 GiB installed|
|Configured data rate|3200 reported for both modules|
|Module locations|Controller0-ChannelA-DIMM0; Controller1-ChannelA-DIMM0|
|OS-visible memory|16906080256 bytes|
|Memory channels|CPU supports at most 2; firmware locators indicate two controllers, but actual active interleave mode was not measured|
|OS / Python|Windows 11 build 26300; CPython 3.14.2, 64-bit AMD64|

The [Intel processor specification](https://www.intel.com/content/www/us/en/products/sku/213805/intel-core-i511400h-processor-12m-cache-up-to-4-50-ghz/specifications.html) confirms 6 cores, 12 threads, 12 MB shared cache and a maximum of 2 memory channels. These capabilities do not prove achieved memory bandwidth, active memory mode or frequency during the experiment. The audit does not invent missing L1 or memory-controller measurements.

Reproduce the local audit in PowerShell:

```powershell
Get-CimInstance Win32_Processor | Select-Object Name,NumberOfCores,NumberOfLogicalProcessors,L2CacheSize,L3CacheSize
Get-CimInstance Win32_PhysicalMemory | Select-Object Capacity,Speed,ConfiguredClockSpeed,DeviceLocator
Get-CimInstance Win32_ComputerSystem | Select-Object TotalPhysicalMemory
```

The [300 dpi plot](../plots/scaling_comparison.png) and [vector SVG](../plots/scaling_comparison.svg) show ideal linear speedup, the bounded OLS Gustafson fit, measured means with one-standard-error bars and Amdahl's curve with the same numeric alpha. The latest fit has alpha=0.9724203696; the theoretical curves are distinct but both far below ideal linear scaling. The comparison does not imply equal workloads under the two laws.

The most direct discrepancy is the end-to-end process overhead: one-worker mean speedup is .2208, already far below the model's fixed intercept. Spawning P interpreters, dispatching small jobs, collecting results and shutting down pools cost time absent from the sequential reference. The arithmetic workload has tiny live state, so this experiment cannot support a DRAM-bandwidth bottleneck diagnosis. CPython's GIL does not serialize arithmetic across these separate processes, although each process executes Python scalar operations.

Past 6 workers, logical threads share execution resources with sibling threads. This may limit incremental gains; the experiment does not measure instruction-level utilization. Larger speedup variation at P=12 could reflect scheduling and background load, but no attribution is proven. Mobile CPU boost and package thermal limits can change clock rates between serial and multicore work. Temperature, frequency, package energy and throttle flags were not collected, so thermal throttling is a possible explanation, not a measured event.

This is a single mobile CPU; there is no evidence of cross-socket NUMA penalties in these data. NUMA topology and placement were not instrumented. On multisocket hardware, first-touch allocation and remote memory traffic can increase C(P), and a dedicated NUMA audit would be needed. Neither NUMA nor throttling should be cited as an observed cause without counters. Reuse pools and increase k in a separately preserved follow-up experiment to distinguish steady-state arithmetic from end-to-end process costs.
