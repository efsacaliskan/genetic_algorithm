from genetic_algorithm import *
import matplotlib.pyplot as plt



D_DIR = "datasets/"
D_NAME = "dataset1/"
POP = 100
ITE = 10
E_RATIO = [0, 0.05, 0.10, 0.20]
M_RATE = 0.05
results = {}
results_time = {}
for e in E_RATIO:
    score_list = []
    time_list = []
    for i in range(10):
        result = genetic_algorithm(D_DIR ,D_NAME, POP, ITE, e, M_RATE )
        computational_time = result[0]
        best_chromosome = result[1][0]
        best_score = result[1][1]
        score_list.append(best_score)
        time_list.append(computational_time)

    results[e] = sum(score_list)/len(score_list)
    results_time[e] = sum(time_list) / len(time_list)



plt.figure()
plt.plot(results.keys(), results.values(),'o-')
plt.title("Elitisim ratio vs Objective")
plt.xlabel("Elitisim ratio")
plt.ylabel("Objective")
plt.grid(True, linestyle='--')

plt.figure()
plt.plot(results_time.keys(), results_time.values(),'o-')
plt.title("Elitisim ratio vs Computational time")
plt.xlabel("Elitisim ratio")
plt.ylabel("Time(s)")
plt.grid(True, linestyle='--')
plt.show()

