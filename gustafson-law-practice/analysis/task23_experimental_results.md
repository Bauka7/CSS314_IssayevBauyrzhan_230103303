# Task 23. Data collection and regression

Actual run: 6 November 2026, Windows 11, Python 3.14.2, k=500000 midpoint evaluations per worker. All P=1..12 configurations were run five times each, for 60 measured pools and 60 matching serial references. Execution order was interleaved with seed 230103303. No timings were discarded. See raw `../benchmarks/results.csv`, configuration `../benchmarks/environment.json`, and full statistics `../benchmarks/summary.csv`.

For run i, S_i=T_serial_i(W(P))/T_parallel_i(W(P)). For each configuration report mean runtime, sample standard deviation (denominator n-1), mean S, and SE(S)=SD(S)/sqrt(5). Mean of paired ratios is used, not ratio of mean runtimes. Counts denote processes; the machine has 6 physical cores, not 12 independent physical cores.

| P | Mean parallel seconds | Sample SD seconds | Mean S | SE(S) |
|---:|---:|---:|---:|---:|
|1|0.278660|0.008604|0.220770|0.002926|
|2|0.293764|0.013754|0.420676|0.009039|
|3|0.286987|0.014689|0.641389|0.014885|
|4|0.315726|0.039911|0.814819|0.021488|
|5|0.318855|0.030366|0.995059|0.056205|
|6|0.355237|0.042602|1.071814|0.051121|
|7|0.379592|0.019283|1.150017|0.033546|
|8|0.412971|0.031480|1.197251|0.040782|
|9|0.434255|0.032476|1.279881|0.040521|
|10|0.455341|0.008387|1.369425|0.012745|
|11|0.490982|0.034704|1.394750|0.025457|
|12|0.579338|0.093547|1.334167|0.090959|

Fit S_j=P_j-alpha*(P_j-1) by minimizing sum_j (S_j-P_j+alpha*(P_j-1))^2 over configuration means. Differentiating gives alpha_hat=sum_j[(P_j-1)(P_j-S_j)]/sum_j[(P_j-1)^2]. Equal sample counts justify equal configuration weighting; heteroscedastic errors remain a limitation. P=1 contributes a residual but no information to the slope estimate.

The latest repeated experiment gives unconstrained OLS alpha_hat=0.9724203696. It lies within [0,1], so the bounded estimate is identical. RMSE=0.3252854394 and R^2=0.2321441322. The JSON retains both estimates and every residual. The low R^2 and large low-P residuals indicate a poor one-parameter fit. This effective penalty is not a direct measurement that 97.24% of application code is serial. Runtime variation between experiments is expected; this table and the current CSV describe the latest run.

At P=1, ideal Gustafson demands S=1, whereas a spawned worker has startup cost absent from the direct serial reference. At higher P the pools also grow more expensive. These implementation costs violate the law's assumptions. The observed maximum mean S=1.394750 at P=11 is modest; it does not establish an optimum beyond the measured five-run uncertainty. Error bars show one SE, not a 95% confidence interval. Benchmark repetitions use newly created pools but are not guaranteed independent of host thermal or scheduler state.
