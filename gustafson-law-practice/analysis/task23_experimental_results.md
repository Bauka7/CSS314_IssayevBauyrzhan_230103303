# Task 23. Data collection and regression

Actual run: 6 November 2026, Windows 11, Python 3.14.2, k=500000 midpoint evaluations per worker. All P=1..12 configurations were run five times each, for 60 measured pools and 60 matching serial references. Execution order was interleaved with seed 230103303. No timings were discarded. See raw `../benchmarks/results.csv`, configuration `../benchmarks/environment.json`, and full statistics `../benchmarks/summary.csv`.

For run i, S_i=T_serial_i(W(P))/T_parallel_i(W(P)). For each configuration report mean runtime, sample standard deviation (denominator n-1), mean S, and SE(S)=SD(S)/sqrt(5). Mean of paired ratios is used, not ratio of mean runtimes. Counts denote processes; the machine has 6 physical cores, not 12 independent physical cores.

| P | Mean parallel seconds | Sample SD seconds | Mean S | SE(S) |
|---:|---:|---:|---:|---:|
|1|0.324336|0.012699|0.205099|0.007264|
|2|0.345305|0.033980|0.373998|0.015489|
|3|0.373148|0.053270|0.531833|0.035290|
|4|0.523351|0.340527|0.658810|0.068512|
|5|0.414420|0.038656|0.831445|0.050080|
|6|0.449827|0.044582|0.888287|0.025793|
|7|0.492265|0.068242|0.929017|0.040444|
|8|0.590067|0.127124|0.985087|0.028399|
|9|0.691768|0.329650|1.002380|0.107350|
|10|0.707100|0.086429|0.974968|0.031678|
|11|0.650723|0.053309|1.162858|0.074193|
|12|0.809688|0.087757|1.004344|0.051276|

Fit S_j=P_j-alpha*(P_j-1) by minimizing sum_j (S_j-P_j+alpha*(P_j-1))^2 over configuration means. Differentiating gives alpha_hat=sum_j[(P_j-1)(P_j-S_j)]/sum_j[(P_j-1)^2]. Equal sample counts justify equal configuration weighting; heteroscedastic errors remain a limitation. P=1 contributes a residual but no information to the slope estimate.

Unconstrained OLS gives alpha_hat=1.0056894651. This is outside [0,1]; projecting to that interval gives alpha_observed=1.0000000000, the constrained least-squares optimum. Constrained RMSE=0.3455265353 and R^2=-0.5377054902. The JSON retains both estimates and every residual. A negative R^2 means the constrained law predicts these means worse than a constant fitted to their average. It is evidence against this one-parameter model here, not a measurement of literally 100% serial application code.

At P=1, ideal Gustafson demands S=1, whereas a spawned worker has startup cost absent from the direct serial reference. At higher P the pools also grow more expensive. These implementation costs violate the law's assumptions. The observed maximum mean S=1.162858 at P=11 is modest; it does not establish an optimum beyond the measured five-run uncertainty. Error bars show one SE, not a 95% confidence interval. Benchmark repetitions use newly created pools but are not guaranteed independent of host thermal or scheduler state.
