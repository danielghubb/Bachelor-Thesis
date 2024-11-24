import json
import os
from enum import Enum
import numpy as np
from natsort import os_sorted

from calculate_statistics import *


def getAllGraphs(path):
    graphs = os_sorted(os.listdir(path))
    return [g for g in graphs if g.split('.')[-1] == 'json']


def load_data(path, name):
    fp = f"{path}{name}.json"
    if os.path.isfile(fp):
        with open(fp, 'r') as file:
            data = json.load(file)
            return data
    else:
        print(f'ERROR: {name} can not load json data. The graph file does not exist.')

def analyse_results_overall_instances(instances, path_to_instances):
    
    approximate_solver_time = []
    approximate_solver_time_reduced = []
    approximate_solver_cost = []
    approximate_solver_cost_reduced = []
    approximate_solver_build_time = []
    approximate_solver_build_time_reduced = []


    exact_solver_time = []
    exact_solver_time_reduced = []
    exact_solver_cost = []
    exact_solver_cost_reduced = []
    exact_solver_build_time = []
    exact_solver_build_time_reduced = []

    solution_by_rr_cost = []


    
    for inst in instances:
        g = inst.split('.')[0]  # remove the .json fullname
        data = load_data(path_to_instances, g)

        # Handle approximation solver data
        if "approximation_solver" in data and "exact_solver" in data:
            approximation_solver = data["approximation_solver"]
            exact_solver = data["exact_solver"]

            if all(key in approximation_solver for key in [
                "approximate_time", "approximate_time_reduced", 
                "approximate_solutionCost", "approximate_solutionCost_reduced",
                "approx_buildTime", "approx_buildTime_reduced"]) and all(key in exact_solver for key in [
                "exact_time", "exact_time_reduced", 
                "exact_solutionCost", "exact_solutionCost_reduced",
                "exact_buildTime", "exact_buildTime_reduced"]):
                
                approximate_solver_time.append(approximation_solver["approximate_time"])
                approximate_solver_time_reduced.append(approximation_solver["approximate_time_reduced"])
                approximate_solver_cost.append(approximation_solver["approximate_solutionCost"])
                approximate_solver_cost_reduced.append(approximation_solver["approximate_solutionCost_reduced"])
                approximate_solver_build_time.append(approximation_solver["approx_buildTime"])
                approximate_solver_build_time_reduced.append(approximation_solver["approx_buildTime_reduced"])

                exact_solver_time.append(exact_solver["exact_time"])
                exact_solver_time_reduced.append(exact_solver["exact_time_reduced"])
                exact_solver_cost.append(exact_solver["exact_solutionCost"])
                exact_solver_cost_reduced.append(exact_solver["exact_solutionCost_reduced"])
                exact_solver_build_time.append(exact_solver["exact_buildTime"])
                exact_solver_build_time_reduced.append(exact_solver["exact_buildTime_reduced"])


                if "solution_by_rr" in data:
                    if data["solution_by_rr"]:  # Check if the list is not empty
                        total_weight = sum(entry["weight"] for entry in data["solution_by_rr"])
                    else:  # If the list is empty
                        total_weight = 0
                    solution_by_rr_cost.append(total_weight)
                else:
                    print(f'WARNING: {g} missing solution_by_rr data.')
            else:
                print(f'WARNING: {g} is missing data.')
        else:
            print(f'WARNING: {g} is missing data.')

    
    calculate_statistics_overall_instances(approximate_solver_time, approximate_solver_time_reduced, approximate_solver_cost, approximate_solver_cost_reduced,
                         approximate_solver_build_time, approximate_solver_build_time_reduced, exact_solver_time, exact_solver_time_reduced,
                         exact_solver_cost, exact_solver_cost_reduced, exact_solver_build_time, exact_solver_build_time_reduced, solution_by_rr_cost)
        


def analyse_results_by_habitat_size(instances, path_to_instances):
    # Initialize arrays for storing time data for each habitat size
    habitat_sizes = ["4-6", "6-8", "8-10", "10-12", "12-14"]
    approximate_time = {size: [] for size in habitat_sizes}
    exact_time = {size: [] for size in habitat_sizes}
    approximate_time_reduced = {size: [] for size in habitat_sizes}
    exact_time_reduced = {size: [] for size in habitat_sizes}
    solution_cost_ratios = {size: [] for size in habitat_sizes}

    # Track percentages of instances where reduced times are greater
    exact_time_reduced_greater = {size: 0 for size in habitat_sizes}
    approximate_time_reduced_greater = {size: 0 for size in habitat_sizes}
    total_instances = {size: 0 for size in habitat_sizes}

    # Loop through each instance and store the data in the appropriate list
    for inst in instances:
        g = inst.split('.')[0]
        appendix = g.split('_')[2]
        data = load_data(path_to_instances, g)

        if "approximation_solver" in data and "exact_solver" in data:
            approximation_solver = data["approximation_solver"]
            exact_solver = data["exact_solver"]

            if all(key in approximation_solver for key in [
                "approximate_time", "approximate_time_reduced", 
                "approximate_solutionCost", "approximate_solutionCost_reduced",
                "approx_buildTime", "approx_buildTime_reduced"]) and all(key in exact_solver for key in [
                "exact_time", "exact_time_reduced", 
                "exact_solutionCost", "exact_solutionCost_reduced",
                "exact_buildTime", "exact_buildTime_reduced"]):

                # Append time data for the approximation and exact solvers
                approximate_time[appendix].append(approximation_solver["approximate_time"])
                exact_time[appendix].append(exact_solver["exact_time"])
                approximate_time_reduced[appendix].append(approximation_solver["approximate_time_reduced"])
                exact_time_reduced[appendix].append(exact_solver["exact_time_reduced"])

                # Increment total instance count for this habitat size
                total_instances[appendix] += 1

                # Check if reduced times are greater and update counts
                if exact_time_reduced[appendix][-1] > exact_time[appendix][-1]:
                    exact_time_reduced_greater[appendix] += 1

                if approximate_time_reduced[appendix][-1] > approximate_time[appendix][-1]:
                    approximate_time_reduced_greater[appendix] += 1


                #getting values for cost ratio
                exact_solver_cost = exact_solver["exact_solutionCost"]
                if data["solution_by_rr"]:  # Check if the list is not empty
                    total_weight = sum(entry["weight"] for entry in data["solution_by_rr"])
                else:  # If the list is empty
                    total_weight = 0
                
                cost_ratio = float(total_weight) / float(exact_solver_cost)
                
                solution_cost_ratios[appendix].append(cost_ratio)


            else:
                print(f'WARNING: {g} missing computation data.')

    # Calculate the median time ratio for each habitat size and percentages
    ratio_time_median = []
    ratio_time_median_reduced = []
    exact_time_reduced_percentage = []
    approximate_time_reduced_percentage = []
    solution_cost_ratio_median = []
    ratio_time_between_instances_exact =[]
    ratio_time_between_instances_approx =[]

    for size in habitat_sizes:
        # Convert lists to numpy arrays for statistical calculations
        approx_time_arr = np.array(approximate_time[size])
        exact_time_arr = np.array(exact_time[size])
        approx_time_arr_reduced = np.array(approximate_time_reduced[size])
        exact_time_arr_reduced = np.array(exact_time_reduced[size])

        # Calculate median time ratio
        median_ratio = np.median(exact_time_arr / approx_time_arr)
        ratio_time_median.append(median_ratio)

        # Calculate median time ratio for reduced data
        median_ratio_reduced = np.median(exact_time_arr_reduced / approx_time_arr_reduced)
        ratio_time_median_reduced.append(median_ratio_reduced)

        # Calculate median time ratio for cost
        median_cost_ratio = np.mean(solution_cost_ratios[size])
        #print(solution_cost_ratios[size])
        solution_cost_ratio_median.append(median_cost_ratio)

        # Calculate median time ratio between reduced and non reduced
        median_time_ratio_between_reduced_nonreduced_exact= np.median(exact_time_arr_reduced / exact_time_arr)
        median_time_ratio_between_reduced_nonreduced_approx= np.median(approx_time_arr_reduced / approx_time_arr)
        ratio_time_between_instances_exact.append(median_time_ratio_between_reduced_nonreduced_exact)
        ratio_time_between_instances_approx.append(median_time_ratio_between_reduced_nonreduced_approx)

        # Calculate percentages
        if total_instances[size] > 0:
            exact_time_reduced_percentage.append(
                (exact_time_reduced_greater[size] / total_instances[size]) * 100
            )
            approximate_time_reduced_percentage.append(
                (approximate_time_reduced_greater[size] / total_instances[size]) * 100
            )
        else:
            exact_time_reduced_percentage.append(0)
            approximate_time_reduced_percentage.append(0)

    # Write the results to a file
    with open("experiments/analyse_results/time_ratio_by_habitatSize.txt", "w") as file:
        for size, median, median_reduced, exact_perc, approx_perc, cost_median, between_exact, between_approx  in zip(
                habitat_sizes, 
                ratio_time_median, 
                ratio_time_median_reduced, 
                exact_time_reduced_percentage, 
                approximate_time_reduced_percentage,
                solution_cost_ratio_median,
                ratio_time_between_instances_exact,
                ratio_time_between_instances_approx


            ):
                file.write(f"Habitat Size {size}:\n")
                file.write(f"  Median Time Ratio = {median}\n")
                file.write(f"  Median Time Ratio (Reduced) = {median_reduced}\n")
                file.write(f"  Percentage of Instances where exact_time_reduced > exact_time = {exact_perc}%\n")
                file.write(f"  Percentage of Instances where approximate_time_reduced > approximate_time = {approx_perc}%\n")
                file.write(f"  Mean Solution Cost Ratio (solution_by_rr_cost / exact_solver_cost) = {cost_median}\n")
                file.write(f"  Median Time Ratio Between Reduced And NonReduced Exact= {between_exact}\n")
                file.write(f"  Median Time Ratio Between Reduced And NonReduced Approx= {between_approx}\n\n")






def visualise_results_by_density(instances, path_to_instances):
    # Initialize arrays for storing time data for each density
    densities = ["10", "20", "30", "40", "50", "60", "70", "80", "90"]
    approximate_time = {density: [] for density in densities}
    exact_time = {density: [] for density in densities}
    approximate_time_reduced = {density: [] for density in densities}
    exact_time_reduced = {density: [] for density in densities}
    solution_cost_ratios = {density: [] for density in densities}

    # Track percentages of instances where reduced times are greater
    exact_time_reduced_greater = {density: 0 for density in densities}
    approximate_time_reduced_greater = {density: 0 for density in densities}
    total_instances = {density: 0 for density in densities}

    # Loop through each instance and store the data in the appropriate list
    for inst in instances:
        g = inst.split('.')[0]
        density = g.split('_')[-1].replace('density', '')
        data = load_data(path_to_instances, g)

        if data:
            if "approximation_solver" in data and "exact_solver" in data:
                approximation_solver = data["approximation_solver"]
                exact_solver = data["exact_solver"]

                if all(key in approximation_solver for key in [
                    "approximate_time", "approximate_time_reduced", 
                    "approximate_solutionCost", "approximate_solutionCost_reduced",
                    "approx_buildTime", "approx_buildTime_reduced"]) and all(key in exact_solver for key in [
                    "exact_time", "exact_time_reduced", 
                    "exact_solutionCost", "exact_solutionCost_reduced",
                    "exact_buildTime", "exact_buildTime_reduced"]):

                    # Append time data for the approximation and exact solvers
                    approximate_time[density].append(approximation_solver["approximate_time"])
                    exact_time[density].append(exact_solver["exact_time"])
                    approximate_time_reduced[density].append(approximation_solver["approximate_time_reduced"])
                    exact_time_reduced[density].append(exact_solver["exact_time_reduced"])

                    # Increment total instance count for this density
                    total_instances[density] += 1

                    # Check if reduced times are greater and update counts
                    if exact_time_reduced[density][-1] > exact_time[density][-1]:
                        exact_time_reduced_greater[density] += 1

                    if approximate_time_reduced[density][-1] > approximate_time[density][-1]:
                        approximate_time_reduced_greater[density] += 1

                    # Calculate and store solution cost ratio
                    exact_solver_cost = exact_solver["exact_solutionCost"]
                    if data["solution_by_rr"]:  # Check if the list is not empty
                        total_weight = sum(entry["weight"] for entry in data["solution_by_rr"])
                    else:  # If the list is empty
                        total_weight = 0

                    cost_ratio = float(total_weight) / float(exact_solver_cost)
                    solution_cost_ratios[density].append(cost_ratio)
                
                else:
                    print(f'WARNING: {g} missing computation data.')

    # Calculate the median time ratio for each density and percentages
    ratio_time_median = []
    ratio_time_median_reduced = []
    exact_time_reduced_percentage = []
    approximate_time_reduced_percentage = []
    solution_cost_ratio_median = []
    ratio_time_between_instances_exact =[]
    ratio_time_between_instances_approx =[]

    for density in densities:
        # Convert lists to numpy arrays for statistical calculations
        approx_time_arr = np.array(approximate_time[density])
        exact_time_arr = np.array(exact_time[density])
        approx_time_arr_reduced = np.array(approximate_time_reduced[density])
        exact_time_arr_reduced = np.array(exact_time_reduced[density])

        # Calculate median ratios
        ratio_time_median.append(np.median(exact_time_arr / approx_time_arr))
        ratio_time_median_reduced.append(np.median(exact_time_arr_reduced / approx_time_arr_reduced))

        median_cost_ratio = np.mean(solution_cost_ratios[density])
        solution_cost_ratio_median.append(median_cost_ratio)

        # Calculate median time ratio between reduced and non reduced
        median_time_ratio_between_reduced_nonreduced_exact= np.median(exact_time_arr_reduced / exact_time_arr)
        median_time_ratio_between_reduced_nonreduced_approx= np.median(approx_time_arr_reduced / approx_time_arr)
        ratio_time_between_instances_exact.append(median_time_ratio_between_reduced_nonreduced_exact)
        ratio_time_between_instances_approx.append(median_time_ratio_between_reduced_nonreduced_approx)


        # Calculate percentages
        if total_instances[density] > 0:
            exact_time_reduced_percentage.append(
                (exact_time_reduced_greater[density] / total_instances[density]) * 100
            )
            approximate_time_reduced_percentage.append(
                (approximate_time_reduced_greater[density] / total_instances[density]) * 100
            )
        else:
            exact_time_reduced_percentage.append(0)
            approximate_time_reduced_percentage.append(0)

    # Write the results to a file
    with open("experiments/analyse_results/time_ratio_by_density.txt", "w") as file:
        for density, median, median_reduced, exact_perc, approx_perc, cost_median,  between_exact, between_approx in zip(
            densities,
            ratio_time_median,
            ratio_time_median_reduced,
            exact_time_reduced_percentage,
            approximate_time_reduced_percentage,
            solution_cost_ratio_median,
            ratio_time_between_instances_exact,
            ratio_time_between_instances_approx
        ):
            file.write(f"Density {density}:\n")
            file.write(f"  Median Time Ratio = {median}\n")
            file.write(f"  Median Time Ratio (Reduced) = {median_reduced}\n")
            file.write(f"  Percentage of Instances where exact_time_reduced > exact_time = {exact_perc}%\n")
            file.write(f"  Percentage of Instances where approximate_time_reduced > approximate_time = {approx_perc}%\n")
            file.write(f"  Mean Solution Cost Ratio (solution_by_rr_cost / exact_solver_cost) = {cost_median}\n")
            file.write(f"  Median Time Ratio Between Reduced And NonReduced Exact= {between_exact}\n")
            file.write(f"  Median Time Ratio Between Reduced And NonReduced Approx= {between_approx}\n\n")


if __name__ == '__main__':


    path_to_instances = 'create_instances/instances/'
    instances = getAllGraphs(path_to_instances)

    analyse_results_overall_instances(instances, path_to_instances)
    analyse_results_by_habitat_size(instances, path_to_instances)
    visualise_results_by_density(instances, path_to_instances)

