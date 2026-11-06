# Task 11. Memory-bounded scaling

Sun and Ni's framework treats memory capacity as the constraint that selects the expanded workload. It generalizes the fixed-size and fixed-time choices. Their analysis includes communication and workload allocation; the simple model below deliberately omits those effects.

Let a be fixed serial work, b baseline parallel work, and G(P) the growth of parallel work enabled by aggregate memory. Then

S_M(P) = [a+b*G(P)]/[a+b*G(P)/P].

G(P)=1 gives fixed-size Amdahl with s=a/(a+b). G(P)=P keeps parallel runtime b constant and gives Gustafson with alpha=a/(a+b). If work is proportional to memory^q and memory grows P-fold, then G(P)=P^q. For dense GEMM, memory ~N^2 and work ~N^3, so q=3/2; parallel time then grows as P^(1/2), rather than staying fixed.

For a,b>0 and P>1, S_M increases with G. Therefore G<P yields less speedup than the Gustafson choice with the same baseline a,b: memory limits, replication or non-growing input can make Gustafson optimistic. G>P can produce higher speedup than that baseline curve by better amortizing fixed serial work, while still remaining at or below P. This is speedup of the expanded workload, not superlinear speedup and not proof of a fixed runtime. Communication can erase the gain. Throughput must specify units of work per second when workloads differ.

Primary source: [Sun and Ni, Scalable Problems and Memory-Bounded Speedup, JPDC 19, 1993](https://www.cs.iit.edu/~scs/psfiles/Sun_and_Ni_JPDC1993.pdf).
