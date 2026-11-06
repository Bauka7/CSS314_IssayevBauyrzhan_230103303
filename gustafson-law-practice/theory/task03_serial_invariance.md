# Task 03. Serial fraction and measurement frame

Let A be serial work and B parallelizable work for a particular problem, measured in one-core seconds. The one-core fraction is s=A/(A+B). On P cores the fraction is alpha=A/(A+B/P). Consequently:

alpha = P*s/[1+(P-1)*s], and s = alpha/[P-alpha*(P-1)].

Substituting this s into Amdahl's expression yields exactly P-alpha(P-1). There is no contradiction for a common workload and ideal execution model.

For a fixed workload, s stays fixed and alpha increases toward 1 as P grows (when A>0). For Gustafson's family, keep A and B/P constant, so B grows proportionally to P. Then alpha stays fixed while s(P)=alpha/[alpha+P(1-alpha)] tends to zero. The absolute serial time has not disappeared; its fraction of the growing serial reference has decreased.

Example: alpha=.004 at P=1024 gives S=1019.908 and s=.004/1019.908, about .000003922. Reusing .004 as Amdahl's one-core fraction would describe a different workload. Serial overhead that grows with P, such as a centralized output stage, still reduces scaling; changing the measurement frame does not remove it.
