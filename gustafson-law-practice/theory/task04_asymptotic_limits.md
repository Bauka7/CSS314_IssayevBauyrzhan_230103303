# Task 04. Efficiency limits

For constant 0<=alpha<=1, E_G(P)=1-alpha+alpha/P. Since lim(P->infinity) 1/P=0, the sum rule gives lim E_G=1-alpha. Its derivative -alpha/P^2 is nonpositive: efficiency approaches the limit from above. Speedup still grows without bound when alpha<1; when alpha=1, speedup is 1 and efficiency tends to zero.

For constant s, E_A(P)=1/[P*s+1-s]. If s>0, the denominator diverges, so lim E_A=0. For s=0 exactly, E_A=1 at every P and the limit is 1. Thus a nonzero serial fraction produces very different efficiency limits under fixed work and growing work.

These statements require invariant fractions in their respective frames. If alpha=alpha(P), then E_G=1-alpha(P)+alpha(P)/P; for a convergent fraction the limit becomes 1-lim alpha(P). No universal positive limit follows when communication or serial processing grows unbounded relative to useful parallel time.
