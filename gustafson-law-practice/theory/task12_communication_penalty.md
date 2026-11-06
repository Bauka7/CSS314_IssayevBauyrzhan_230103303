# Task 12. Explicit communication extension

Let a be useful serial-stage time, b useful parallel-stage time per processor, and C(P)>=0 extra critical-path communication absent from a serial run. Weak scaling supplies P*b useful parallel work. Then T_P=a+b+C(P), T_1(W(P))=a+P*b, and

S_C(P)=(a+P*b)/(a+b+C(P)).

Set alpha0=a/(a+b), c(P)=C(P)/(a+b). Therefore S_C=[P-alpha0(P-1)]/[1+c(P)], and E_C=[1-alpha0+alpha0/P]/[1+c(P)]. A consistent extension has C(1)=0. Examples: C(P)=lambda*log2(P) for a tree, or lambda*(sqrt(P)-1) for a growing critical path.

For either unbounded penalty and constant b, efficiency tends to zero. Speedup scales approximately as P/log P or sqrt(P), respectively, when alpha0<1. To maintain time, grow local useful work or overlap communication; that changes the workload schedule and must be documented.

One must not count extra communication as useful serial work in the numerator. If alpha and gamma denote serial and communication fractions of actual T_P, respectively, then S=alpha+P*(1-alpha-gamma). Simply using 1-alpha as useful parallel time would count communication as perfectly parallelizable useful work.
