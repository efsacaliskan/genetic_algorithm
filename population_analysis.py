from genetic_algorithm import *
import matplotlib.pyplot as plt



D_DIR = "datasets/"
D_NAME = "dataset1/"
POP = [10,50,100,500,1000]
ITE = 100
E_RATIO = 0.10
M_RATE = 0.05
results = {}
results_time = {}
for population in POP:
    score_list = []
    time_list = []
    for i in range(10):
        result = genetic_algorithm(D_DIR ,D_NAME, population, ITE, E_RATIO, M_RATE )
        computational_time = result[0]
        best_chromosome = result[1][0]
        best_score = result[1][1]
        score_list.append(best_score)
        time_list.append(computational_time)

    results[population] = sum(score_list)/len(score_list)
    results_time[population] = sum(time_list) / len(time_list)



plt.figure()
plt.plot(results.keys(), results.values(),'o-')
plt.title("Population size vs Objective")
plt.xlabel("Population size")
plt.ylabel("Objective")
plt.grid(True, linestyle='--')

plt.figure()
plt.plot(results_time.keys(), results_time.values(),'o-')
plt.title("Population size vs Computational time")
plt.xlabel("Population size")
plt.ylabel("Time(s)")
plt.grid(True, linestyle='--')
plt.show()

