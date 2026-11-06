# Task 22. Multiprocessing numerical workload

Python 3.10+ runs the benchmark without external packages. From the repository root:

```powershell
python gustafson-law-practice/benchmarks/weak_scale_bench/benchmark.py --k 500000 --runs 5
```

Default counts are every integer from 1 through `os.cpu_count()`, the host's visible logical hardware concurrency. Each process integrates 4/(1+x*x) over [0,1] using k midpoint samples. Total numerical operations grow as kP. Independent copies provide a balanced synthetic CPU workload and a known answer pi; they are not a higher-resolution combined quadrature.

Every configuration has five separately created process pools. Timing includes startup, dispatch, numerical work, reduction and pool shutdown. A paired serial execution performs the exact same P quadratures; scaled speedup is its measured duration divided by the parallel duration. This is not strong speedup T1(k)/TP(Pk), and no baseline is multiplied by P to manufacture a serial reference. All estimates are validated against pi and the serial output before saving.

Configurations are interleaved in deterministic shuffled order; serial/parallel measurement order alternates. No affinity, priority, frequency or power settings are changed. The workload is deliberately end-to-end: Windows spawn overhead may outweigh work and produce speedup below 1, including P=1. Such a result falsifies the simple fixed-time model for this implementation; it must not be hidden by removing timing samples.

Use `--counts 1 2 4 6 12 --k 2000000` for a separate larger-work experiment, choosing counts within your host maximum and a separate `--output` to preserve raw data. No compilation is required. `../environment.json` records the configuration and timing scope.
