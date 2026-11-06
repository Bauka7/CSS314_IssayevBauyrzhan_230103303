# Task 06. Parametric table: alpha = 0.04

S(P)=P-.04(P-1)=.96P+.04; E(P)=.96+.04/P.

| P | S(P) | E(P) | Efficiency % |
|---:|---:|---:|---:|
|16|15.40|0.9625|96.250000|
|64|61.48|0.960625|96.062500|
|256|245.80|0.96015625|96.015625|
|1024|983.08|0.9600390625|96.00390625|
|4096|3932.20|0.960009765625|96.0009765625|
|16384|15728.68|0.96000244140625|96.000244140625|

Example log: S(256)=256-.04*255=245.8; E=245.8/256=.96015625. Efficiency falls monotonically toward 96%, by only about .249756 percentage points over this table. The bounded loss assumes constant alpha, not a growing network penalty. Full machine-readable logs for every integer P through 65536, including alpha=.04, are in `../benchmarks/simulator.csv`.
