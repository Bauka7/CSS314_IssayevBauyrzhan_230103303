# Task 14. Isoeﬃciency

Let W=T_1 be useful work and T_o=P*T_P-W aggregate processor-time overhead. Then E=W/(W+T_o). At a target 0<E0<1, solving yields W=[E0/(1-E0)]*T_o.

For the ideal Gustafson family T_P=a+b, W=a+Pb and T_o=(P-1)*a. If a>0 is constant, overhead is Theta(P). The isoefficiency function is W=Theta(P): work must grow linearly to keep a fixed positive efficiency. Substituting W(P)=a+Pb gives E=b/(a+b)+a/[P(a+b)], which tends to the target b/(a+b), rather than staying exactly equal at finite P.

For exact E0 with fixed a, choose W=E0*a*(P-1)/(1-E0); the needed b(P)=(W-a)/P tends to E0*a/(1-E0). This construction requires W>=a and is meaningful for sufficiently large P. If a=0 and all other overhead is absent, E=1 for any adequate parallel workload; the nontrivial Theta(P) overhead argument no longer applies.

If communication C(P)=Theta(log P) is exposed, T_o contains P*C(P), so an otherwise similar model requires W=Omega(P log P). The law's fixed-local-work family then fails to maintain efficiency. Isoeﬃciency is a property of algorithm and machine together, not a guarantee supplied by the name of a scaling law.
