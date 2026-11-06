# Task 01. Fixed-size and fixed-time scaling

Let P denote processors, W useful work in single-core time units, and N a problem dimension. Amdahl (1967) keeps W and N fixed. With serial fraction s measured in a one-core execution, T(P)/T(1) = s+(1-s)/P. Hence S_A=1/[s+(1-s)/P]. As P tends to infinity, N stays N0 and S_A tends to 1/s for s>0. This answers a latency question: how quickly can we finish this particular problem?

Gustafson (1988) instead expands the parallel work within an approximately fixed parallel execution time. Normalize that time as alpha+(1-alpha)=1. Keeping serial time bounded and parallel work per processor fixed gives W(P)=alpha+P(1-alpha), and S_G=W(P). As P tends to infinity, work grows linearly, but dimension need not: if work is proportional to N^d, N is proportional to P^(1/d). Only for linear-work problems does N grow proportionally to P.

The physical distinction is resource allocation: strong scaling subdivides existing work more finely; weak scaling supplies additional work as resources grow. Fixed-time scaling assumes startup, communication, synchronization and imbalance remain bounded or are hidden. Memory capacity alone does not ensure this. Pure weak scaling W(P)=P W(1) and Gustafson's constant serial-stage construction differ by a constant intercept, though both have asymptotically linear work.

The laws are compatible accounting identities for different workload families, not conflicting physical limits. A finite application, fixed deadline, communication network or exhausted memory can prevent the fixed-time construction.
