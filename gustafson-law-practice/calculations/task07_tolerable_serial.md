# Task 07. Maximum serial overhead

8192-alpha*(8192-1)>=7500. Subtract 7500 and rearrange with positive denominator 8191:

alpha <= (8192-7500)/8191 = 692/8191 = 0.08448296911244048.

Thus alpha_max is approximately 8.448296911244048% of the parallel runtime. At equality S=7500 and E=7500/8192=.91552734375, or 91.552734375%. Any increase in alpha reduces speedup because dS/dalpha=-8191. This is an elapsed-time fraction, not a tolerance on single-core code coverage or memory use.
