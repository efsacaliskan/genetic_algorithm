import pickle
import random
import time

import numpy as np
import os





def genetic_algorithm(DATASET_DIR,DATASET_NAME,POPULATION,ITERATION,ELITE_RATIO,MUTATION_RATE):

    def get_students_list(chromosome):
        students_used = []
        for students in chromosome.values():
            students_used += students
        return students_used


    def random_chromosome(number_of_projects, number_of_studens):
        # first create a dictionary with keys of every project
        chromosome = {}
        elements_in_chromosome = 0
        projects = list(range(number_of_projects))
        students = list(range(number_of_studens))
        students_selected = random.choices(students, k=number_of_projects)
        for i in range(number_of_projects):
            chromosome[i] = [students_selected[i]]
            elements_in_chromosome += 1

        min_element_in_chromosome = number_of_projects
        max_element_in_chromosome = min_element_in_chromosome * 3
        random_number_of_elements_in_chromosome = random.randint(min_element_in_chromosome, max_element_in_chromosome)

        while elements_in_chromosome < random_number_of_elements_in_chromosome:
            candidate_project = random.choice(projects)
            candidate_student = random.choice(students)
            number_of_students_candidate_project = len(chromosome[candidate_project])
            if number_of_students_candidate_project >= 3:
                continue
            all_elements = get_students_list(chromosome)
            if all_elements.count(candidate_student) >= 2:
                continue
            if candidate_student in chromosome[candidate_project]:
                continue
            chromosome[candidate_project].append(candidate_student)
            elements_in_chromosome += 1

        return chromosome


    def fitness_function(chromosome, requirements, proficiency_levels):
        total_proficiency_level = 0
        for i in range(len(chromosome)):
            students =  chromosome[i]
            project = i
            project_requirement = requirements[project]
            for student in students:
                student_proficiency_level = proficiency_levels[student]
                total_proficiency_level += project_requirement.dot(student_proficiency_level)
        return total_proficiency_level

    def crossover(chromosome1, chromosome2, number_of_projects, number_of_studens):
        child = {}
        crosspoint = random.randint(1,number_of_projects-2)
        for project in list(range(crosspoint)):
            child[project] = list(chromosome1[project])
        for p in list(range(crosspoint,number_of_projects)):
            child[p] = []
            students = chromosome2[p]
            for student in students:
                all_elements = get_students_list(child)
                if all_elements.count(student) < 2:
                    child[p].append(student)

        return child

    def mutate(chromosome, number_of_projects):
        all_projects = list(range(number_of_projects))
        swap_projects = random.choices(all_projects, k=2)
        project1, project2 = swap_projects
        tmp = list(chromosome[project1])
        chromosome[project1] = list(chromosome[project2])
        chromosome[project2] = tmp

    with open(os.path.join(DATASET_DIR, DATASET_NAME, "requirements.pkl"), "rb") as f:
        requirements: np.ndarray = pickle.load(f)

    with open(os.path.join(DATASET_DIR, DATASET_NAME, "proficiency_levels.pkl"), "rb") as f:
        proficiency_levels: np.ndarray = pickle.load(f)

    start_time = time.time()

    number_of_projects, number_of_proficiency = requirements.shape
    number_of_students = proficiency_levels.shape[0]

    #create initial random population
    population_of_chromosomes = []
    for i in range(POPULATION):
        chromosome = random_chromosome(number_of_projects, number_of_students)
        total_proficiency_level = fitness_function(chromosome, requirements, proficiency_levels)
        population_of_chromosomes.append([chromosome,total_proficiency_level ])



    for iteration in range(ITERATION):
        #roulette wheel selection
        population_of_chromosomes = sorted(population_of_chromosomes,key = lambda x : x[1], reverse=True)

        cumulative_scores = []
        for chromosome in population_of_chromosomes:
            score = chromosome[1]
            if len(cumulative_scores) > 0:
                cumulative_scores.append(cumulative_scores[-1] + score)
            else:
                cumulative_scores.append( score)

        max_cumulative = cumulative_scores[-1]

        new_population_of_chromosomes = []
        elite_popultation = int(POPULATION * ELITE_RATIO)
        if elite_popultation % 2 == 1:
            elite_popultation += 1
        for i in range(elite_popultation):
            new_population_of_chromosomes.append(population_of_chromosomes[i])


        for j in range( (POPULATION - elite_popultation) //2):


            random_score = random.randint(0,max_cumulative)
            selected_chromosome1 = population_of_chromosomes[0][0]
            for i in range(POPULATION):
                if  cumulative_scores[i] > random_score:
                    selected_chromosome1 = population_of_chromosomes[i][0]
                    break

            random_score = random.randint(0,max_cumulative)
            selected_chromosome2 = population_of_chromosomes[0][0]
            for i in range(POPULATION):
                if  cumulative_scores[i] > random_score:
                    selected_chromosome2 = population_of_chromosomes[i][0]
                    break


            child1 = crossover(selected_chromosome1,selected_chromosome2,number_of_projects, number_of_students)
            if random.random() < MUTATION_RATE:
                mutate(child1, number_of_projects)
            child2 = crossover(selected_chromosome2, selected_chromosome1, number_of_projects, number_of_students)
            if random.random() < MUTATION_RATE:
                mutate(child2, number_of_projects)
            new_population_of_chromosomes.append( [child1  , fitness_function(child1,requirements, proficiency_levels)] )
            new_population_of_chromosomes.append([child2, fitness_function(child2, requirements, proficiency_levels)])

        population_of_chromosomes = new_population_of_chromosomes

    total_time = time.time() - start_time
    population_of_chromosomes = sorted(population_of_chromosomes, key=lambda x: x[1], reverse=True)

    return (total_time,population_of_chromosomes[0] )


def print_result(chromosome ,score):
    print("%20s %10s %10s %10s" % ("PROJECT","STUDENT1","STUDENT2","STUDENT3") )
    for i in range(len(chromosome)):
        print("%20s " % ("Project" + str(i+1)) , end="")
        for student in chromosome[i]:
            print("%10d " % ( student + 1), end="")
        print()
    print("SCORE : %d"% (score) )

if __name__ == "__main__":
    D_DIR = "datasets/"
    D_NAME = "dataset1/"
    POP = 100
    ITE = 100
    E_RATIO = 0.10
    M_RATE = 0.05
    result = genetic_algorithm(D_DIR, D_NAME, POP, ITE, E_RATIO, M_RATE)
    computational_time = result[0]
    best_chromosome = result[1][0]
    best_score = result[1][1]
    print_result(best_chromosome, best_score)