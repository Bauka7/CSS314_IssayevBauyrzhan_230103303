# Task 02. Deriving scaled speedup

1. Measure the runtime on P identical processors and normalize it to T_P=s+p=1. Here s is the fraction of elapsed parallel-machine time spent in a serial stage; p is the elapsed parallel stage, not its aggregate processor work.
2. Assume the serial stage uses one processor and the parallel stage keeps all P processors fully busy. Ignore communication, replication and changes in instruction rate.
3. On one processor, the same serial stage still takes s time units.
4. The parallel stage contains P*p processor-time units of useful work. Executing this identical scaled workload sequentially takes P*p time units.
5. Thus T_1(W(P))=s+P*p and S(P)=T_1(W(P))/T_P=(s+P*p)/(s+p)=s+P*p.
6. Write alpha=s, p=1-alpha. Then S(P)=alpha+P(1-alpha)=P-alpha(P-1).
7. E(P)=S(P)/P=1-alpha+alpha/P. Checks: S(1)=1; alpha=0 gives P; alpha=1 gives 1. For 0<=alpha<=1, 1<=S<=P.

The numerator always refers to the same scaled workload as the denominator. Dividing the original small workload runtime by the large workload runtime would not be scaled speedup.
