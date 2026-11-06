# Task 09. Three-phase workload

Assume disk I/O/broadcast and boundary synchronization are fully non-overlapped overhead on the critical path. Then alpha=.02+.06=.08 and useful parallel fraction=.92.

| P | Serial/overhead | Parallel | S=.08+.92P | E |
|---:|---:|---:|---:|---:|
|512|8%|92%|471.12|0.92015625|
|2048|8%|92%|1884.24|0.9200390625|

This is a conservative effective-serial interpretation. Boundary communication is not intrinsically serial useful work. If part overlaps computation, only its exposed critical-path time belongs in the penalty. If it grows with P, alpha must be remeasured, and these fixed-fraction projections become optimistic. Communication that does not exist in a sequential implementation should be accounted for explicitly as in Task 12, rather than counted as useful serial work in a speedup numerator.
