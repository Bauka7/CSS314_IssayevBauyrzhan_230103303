# Task 16. GEMM dimension growth

For ideal balanced dense GEMM, useful compute time is K*N^3/P. Equating to the one-processor baseline K*N0^3 yields N(P)=N0*P^(1/3). Work then grows P-fold while aggregate matrix storage grows P^(2/3). Memory per worker is proportional to P^(-1/3) with ideal distributed storage. This differs from filling all available memory, which would give N~sqrt(P) and compute time ~sqrt(P).

| P | N/N0 | N for N0=256 | Aggregate memory / baseline |
|---:|---:|---:|---:|
|1|1|256|1|
|8|2|512|4|
|64|4|1024|16|
|512|8|2048|64|
|4096|16|4096|256|

Targets use exact cube processor counts to avoid rounding. At other P choose a nearby integer dimension and report realized work. Distribution, matrix initialization, collectives and communication may prevent the ideal fixed-time scaling, even when the compute exponent is correct.
