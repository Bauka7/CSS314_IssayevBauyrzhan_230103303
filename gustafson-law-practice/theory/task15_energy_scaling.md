# Task 15. Energy at a fixed runtime

Interpret P_idle as static power per powered node and P_active as additional dynamic power while computing. Let runtime be T, alpha*T be a one-node serial stage, and (1-alpha)*T a stage with P active nodes. Powered nodes do not shut off during the serial stage. Active processor-time is [alpha+P(1-alpha)]T=S_G*T.

Energy E_P = P*P_idle*T + P_active*T*[alpha+P(1-alpha)]. Average power is the same expression divided by T. At one node and identical T, E_1=(P_idle+P_active)*T, so E_P/E_1=[P*P_idle+S_G*P_active]/[P_idle+P_active]. Both generally grow with P, even at good efficiency, because more work is completed.

Example: idle=20 W, incremental active=80 W, alpha=.04, P=64, T=10 s. S=61.48, E_64=(1280+4918.4)*10=61984 J. E_1=1000 J. Energy ratio=61.984, useful-work ratio=61.48, hence energy per unit work is 61.984/61.48=1.00819779 times the one-node value.

This equal-time comparison uses different problem sizes. Executing the same expanded work sequentially takes S_G*T, hence E_serial_same_work=(P_idle+P_active)*S_G*T. Comparing this with E_P isolates energy-to-solution. If P_active instead denotes total active power, replace incremental dynamic power by P_active-P_idle. Network, cooling, DVFS and power-gating are outside this simple model.
