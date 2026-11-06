# Task 19. Monte Carlo and reductions

With k independent paths per rank, useful total work is kP and local path time b is approximately constant. Nonzero alpha arises from input parsing, path parameter setup, PRNG stream assignment, aggregation and output. Counter-based streams keyed by (global path ID, timestep) or validated disjoint substreams avoid a centralized random-number server; arbitrary nearby seeds alone do not prove independence.

A binary reduction of a fixed-size sum has ceil(log2 P) stages. Let exposed latency per stage be lambda and fixed serial stage a. Then C(P)=lambda*ceil(log2 P), T_P=a+b+C(P), and useful scaled speedup is [a+Pb]/[a+b+C(P)]. A naive centralized reduction may instead incur Theta(P) latency. Neither is an infinitely constant overhead.

Numerical example: a=.01 s, b=1 s, lambda=.001 s, P=1024. C=.010 s, T_P=1.020 s, T_1=1024.01 s; speedup=1003.93137, efficiency=.98040173. Without the reduction penalty speedup=1013.87129. An output file per path can dominate much more than this reduction.

Independent paths improve estimator uncertainty as 1/sqrt(kP) for finite-variance samples; this is a statistical benefit of increased work, not additional runtime speedup. Use compensated or stable reductions if reproducibility matters. The submitted benchmark repeats deterministic quadratures as a synthetic workload, not as independent statistical Monte Carlo samples.
