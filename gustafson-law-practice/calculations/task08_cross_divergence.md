# Task 08. Comparing numeric predictions

With s=.08 and P=128, S_A=1/[.08+.92/128]=1/.0871875=3200/279=11.46953405.

With parallel-machine alpha=.08, S_G=128-.08*127=117.84. Their difference is 106.37046595 and ratio S_G/S_A=10.274175. Taking Amdahl as baseline, discrepancy is 100*(S_G-S_A)/S_A=927.4175%. Relative to Gustafson it is about 90.26685841%; the denominator must always be stated.

The first calculation keeps the original problem fixed; the second constructs a larger problem. For the latter, the matching one-core fraction is .08/117.84, not .08. Amdahl tends to 12.5 while Gustafson grows as .92P, so their numeric gap grows. Under the same numeric nonzero fraction they coincide at P=1; there is no additional positive-P cross-over (apart from degenerate fractions 0 or 1). Comparing different workload assumptions cannot demonstrate one model being experimentally wrong.
