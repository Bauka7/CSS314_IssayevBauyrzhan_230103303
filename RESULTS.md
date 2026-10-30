# Empirical Scalability Diagnostics: The Karp-Flatt Metric

## Host Hardware Profile
- **Execution Cores**: 4 Physical / Logical Cores
- **Python Version**: Python 3.10+

## Diagnostic Results Summary

| Experiment Mode | $T_1$ (s) | $T_2$ (s) | $T_4$ (s) | $e(2)$ | $e(4)$ | Architectural Diagnosis |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **A: Serial Tail** | 38.170s | 24.575s | 14.251s | 0.288 | 0.164 | **Flat e**: Fixed Amdahl serialization |
| **B: Lock Contention** | 14.337s | 73.423s | 60.376s | 9.242 | 5.282 | **Exploding e**: Mutex & bus thrashing |
| **C: Privatized State** | 2.813s | 1.691s | 1.272s | 0.202 | 0.270 | **Collapsed e**: Scalability restored |

## Detailed Architectural Findings

1. **Experiment A (Serial Tail)**: 
   - Значения метрики Карпа-Флатта остались в низком диапазоне ($e(2) = 0.288$, $e(4) = 0.164$), показвающем стабильную долю последовательного кода (`time.sleep(0.40)`)[cite: 9]. Ускорение составило $2.68\times$ на 4 ядрах[cite: 9].

2. **Experiment B (Lock Contention)**: 
   - Наблюдается резкое падение производительности ($T_1 = 14.337\text{s} \to T_2 = 73.423\text{s}$, ускорение $S_2 = 0.20\times$)[cite: 10]. Метрика Карпа-Флатта резко возрастает до $e(2) = 9.242$ и $e(4) = 5.282$, математически доказывая межпроцессную борьбу за мьютекс и трафик кэш-линий[cite: 10].

3. **Experiment C (Privatization Fix)**: 
   - Локальное накопление инкрементов в памяти процессов (без общих блокировок) сократило общее время с десятков секунд до $1.272\text{s}$ на 4 ядрах, восстановив параллельное ускорение ($S_4 = 2.21\times$).