import numpy as np

def calculate_statistics_overall_instances(approximate_solver_time, approximate_solver_time_reduced, approximate_solver_cost, approximate_solver_cost_reduced,
                         approximate_solver_build_time, approximate_solver_build_time_reduced, exact_solver_time, exact_solver_time_reduced,
                         exact_solver_cost, exact_solver_cost_reduced, exact_solver_build_time, exact_solver_build_time_reduced, solution_by_rr_cost):


    # Convert lists to numpy arrays
    approximate_solver_time = np.array(approximate_solver_time)
    exact_solver_time = np.array(exact_solver_time)
    approximate_solver_cost = np.array(approximate_solver_cost)
    exact_solver_cost = np.array(exact_solver_cost)
    approximate_solver_build_time = np.array(approximate_solver_build_time)
    exact_solver_build_time = np.array(exact_solver_build_time)

    approximate_solver_time_reduced = np.array(approximate_solver_time_reduced)
    exact_solver_time_reduced = np.array(exact_solver_time_reduced)
    approximate_solver_cost_reduced = np.array(approximate_solver_cost_reduced)
    exact_solver_cost_reduced = np.array(exact_solver_cost_reduced)
    approximate_solver_build_time_reduced = np.array(approximate_solver_build_time_reduced)
    exact_solver_build_time_reduced = np.array(exact_solver_build_time_reduced)

    solution_by_rr_cost = np.array(solution_by_rr_cost)


    #solver times without building time
    approximate_solver_time_without_building = approximate_solver_time - approximate_solver_build_time
    exact_solver_time_without_building = exact_solver_time - exact_solver_build_time

    approximate_solver_time_without_building_reduced = approximate_solver_time_reduced - approximate_solver_build_time_reduced
    exact_solver_time_without_building_reduced = exact_solver_time_reduced - exact_solver_build_time_reduced

    # Calculate ratios
    time_ratio = exact_solver_time / approximate_solver_time
    time_ratio_without_building = exact_solver_time_without_building / approximate_solver_time_without_building
    cost_ratio = approximate_solver_cost / exact_solver_cost
    build_time_ratio = exact_solver_build_time / approximate_solver_build_time

    time_ratio_reduced = exact_solver_time_reduced / approximate_solver_time_reduced
    time_ratio_without_building_reduced = exact_solver_time_without_building_reduced / approximate_solver_time_without_building_reduced
    cost_ratio_reduced = approximate_solver_cost_reduced / exact_solver_cost_reduced
    build_time_ratio_reduced = exact_solver_build_time_reduced / approximate_solver_build_time_reduced

    cost_ratio_rr_to_exact = solution_by_rr_cost/exact_solver_cost

    time_ratio_between_approx_solvers = approximate_solver_time_reduced/approximate_solver_time
    time_ratio_between_exact_solvers = exact_solver_time_reduced/exact_solver_time
    approx_more_time_on_reduced = len([value for value in time_ratio_between_approx_solvers if value > 1])
    exact_more_time_on_reduced = len([value for value in time_ratio_between_exact_solvers if value > 1])

    # Calculate additional build time to time ratios
    build_time_ratio_exact = exact_solver_build_time / exact_solver_time
    build_time_ratio_approx = approximate_solver_build_time / approximate_solver_time

    build_time_ratio_exact_reduced = exact_solver_build_time_reduced / exact_solver_time_reduced
    build_time_ratio_approx_reduced = approximate_solver_build_time_reduced / approximate_solver_time_reduced


    # Calculate statistics for approximate solver times
    approximate_time_stats = {
        'median': np.median(approximate_solver_time),
        'mean': np.mean(approximate_solver_time),
        'std': np.std(approximate_solver_time),
        'min': np.min(approximate_solver_time),
        'max': np.max(approximate_solver_time)
    }

    # Calculate statistics for exact solver times
    exact_time_stats = {
        'median': np.median(exact_solver_time),
        'mean': np.mean(exact_solver_time),
        'std': np.std(exact_solver_time),
        'min': np.min(exact_solver_time),
        'max': np.max(exact_solver_time)
    }

    # Calculate statistics for time ratio
    time_ratio_stats = {
        'median': np.median(time_ratio),
        'mean': np.mean(time_ratio),
        'std': np.std(time_ratio),
        'min': np.min(time_ratio),
        'max': np.max(time_ratio)
    }

    time_ratio_between_exact_stats = {
        'median': np.median(time_ratio_between_exact_solvers),
        'mean': np.mean(time_ratio_between_exact_solvers),
        'std': np.std(time_ratio_between_exact_solvers),
        'min': np.min(time_ratio_between_exact_solvers),
        'max': np.max(time_ratio_between_exact_solvers)
    }

    time_ratio_between_approx_stats = {
        'median': np.median(time_ratio_between_approx_solvers),
        'mean': np.mean(time_ratio_between_approx_solvers),
        'std': np.std(time_ratio_between_approx_solvers),
        'min': np.min(time_ratio_between_approx_solvers),
        'max': np.max(time_ratio_between_approx_solvers)
    }



    # Calculate statistics for time ratio
    time_ratio_without_building_stats = {
        'median': np.median(time_ratio_without_building),
        'mean': np.mean(time_ratio_without_building),
        'std': np.std(time_ratio_without_building),
        'min': np.min(time_ratio_without_building),
        'max': np.max(time_ratio_without_building)
    }

    # Calculate statistics for cost ratio
    cost_ratio_stats = {
        'median': np.median(cost_ratio),
        'mean': np.mean(cost_ratio),
        'std': np.std(cost_ratio),
        'min': np.min(cost_ratio),
        'max': np.max(cost_ratio)
    }

    cost_ratio_rr_to_exact_stats = {
        'median': np.median(cost_ratio_rr_to_exact),
        'mean': np.mean(cost_ratio_rr_to_exact),
        'std': np.std(cost_ratio_rr_to_exact),
        'min': np.min(cost_ratio_rr_to_exact),
        'max': np.max(cost_ratio_rr_to_exact)
    }

    # Calculate statistics for build time ratio
    build_time_ratio_stats = {
        'median': np.median(build_time_ratio),
        'mean': np.mean(build_time_ratio),
        'std': np.std(build_time_ratio),
        'min': np.min(build_time_ratio),
        'max': np.max(build_time_ratio)
    }

    # Calculate statistics for build time to time ratios
    build_time_ratio_exact_stats = {
        'median': np.median(build_time_ratio_exact),
        'mean': np.mean(build_time_ratio_exact),
        'std': np.std(build_time_ratio_exact),
        'min': np.min(build_time_ratio_exact),
        'max': np.max(build_time_ratio_exact)
    }

    build_time_ratio_approx_stats = {
        'median': np.median(build_time_ratio_approx),
        'mean': np.mean(build_time_ratio_approx),
        'std': np.std(build_time_ratio_approx),
        'min': np.min(build_time_ratio_approx),
        'max': np.max(build_time_ratio_approx)
    }

    # Calculate statistics for reduced arrays
    approximate_time_stats_reduced = {
        'median': np.median(approximate_solver_time_reduced),
        'mean': np.mean(approximate_solver_time_reduced),
        'std': np.std(approximate_solver_time_reduced),
        'min': np.min(approximate_solver_time_reduced),
        'max': np.max(approximate_solver_time_reduced)
    }

    exact_time_stats_reduced = {
        'median': np.median(exact_solver_time_reduced),
        'mean': np.mean(exact_solver_time_reduced),
        'std': np.std(exact_solver_time_reduced),
        'min': np.min(exact_solver_time_reduced),
        'max': np.max(exact_solver_time_reduced)
    }

    time_ratio_stats_reduced = {
        'median': np.median(time_ratio_reduced),
        'mean': np.mean(time_ratio_reduced),
        'std': np.std(time_ratio_reduced),
        'min': np.min(time_ratio_reduced),
        'max': np.max(time_ratio_reduced)
    }

    time_ratio_without_building_stats_reduced = {
        'median': np.median(time_ratio_without_building_reduced),
        'mean': np.mean(time_ratio_without_building_reduced),
        'std': np.std(time_ratio_without_building_reduced),
        'min': np.min(time_ratio_without_building_reduced),
        'max': np.max(time_ratio_without_building_reduced)
    }

    cost_ratio_stats_reduced = {
        'median': np.median(cost_ratio_reduced),
        'mean': np.mean(cost_ratio_reduced),
        'std': np.std(cost_ratio_reduced),
        'min': np.min(cost_ratio_reduced),
        'max': np.max(cost_ratio_reduced)
    }

    build_time_ratio_stats_reduced = {
        'median': np.median(build_time_ratio_reduced),
        'mean': np.mean(build_time_ratio_reduced),
        'std': np.std(build_time_ratio_reduced),
        'min': np.min(build_time_ratio_reduced),
        'max': np.max(build_time_ratio_reduced)
    }

    build_time_ratio_exact_stats_reduced = {
        'median': np.median(build_time_ratio_exact_reduced),
        'mean': np.mean(build_time_ratio_exact_reduced),
        'std': np.std(build_time_ratio_exact_reduced),
        'min': np.min(build_time_ratio_exact_reduced),
        'max': np.max(build_time_ratio_exact_reduced)
    }

    build_time_ratio_approx_stats_reduced = {
        'median': np.median(build_time_ratio_approx_reduced),
        'mean': np.mean(build_time_ratio_approx_reduced),
        'std': np.std(build_time_ratio_approx_reduced),
        'min': np.min(build_time_ratio_approx_reduced),
        'max': np.max(build_time_ratio_approx_reduced)
    }

    # Prepare output data
    output_data = (
        f"\nApproximate Solver Time - Median: {approximate_time_stats['median']}, "
        f"Mean: {approximate_time_stats['mean']}, Std: {approximate_time_stats['std']}, "
        f"Min: {approximate_time_stats['min']}, Max: {approximate_time_stats['max']}\n"

        f"Exact Solver Time - Median: {exact_time_stats['median']}, "
        f"Mean: {exact_time_stats['mean']}, Std: {exact_time_stats['std']}, "
        f"Min: {exact_time_stats['min']}, Max: {exact_time_stats['max']}\n"

        f"Time Ratio Between Solvers- Median: {time_ratio_stats['median']}, "
        f"Mean: {time_ratio_stats['mean']}, Std: {time_ratio_stats['std']}, "
        f"Min: {time_ratio_stats['min']}, Max: {time_ratio_stats['max']}\n"

        f"Time Ratio Between Solvers Without Building - Median: {time_ratio_without_building_stats['median']}, "
        f"Mean: {time_ratio_without_building_stats['mean']}, Std: {time_ratio_without_building_stats['std']}, "
        f"Min: {time_ratio_without_building_stats['min']}, Max: {time_ratio_without_building_stats['max']}\n"

        f"Cost Ratio Between Solvers - Median: {cost_ratio_stats['median']}, "
        f"Mean: {cost_ratio_stats['mean']}, Std: {cost_ratio_stats['std']}, "
        f"Min: {cost_ratio_stats['min']}, Max: {cost_ratio_stats['max']}\n"

        f"Cost Ratio Between RR and exact solver  - Median: {cost_ratio_rr_to_exact_stats['median']}, "
        f"Mean: {cost_ratio_rr_to_exact_stats['mean']}, Std: {cost_ratio_rr_to_exact_stats['std']}, "
        f"Min: {cost_ratio_rr_to_exact_stats['min']}, Max: {cost_ratio_rr_to_exact_stats['max']}\n"

        f"Build Time Ratio - Median: {build_time_ratio_stats['median']}, "
        f"Mean: {build_time_ratio_stats['mean']}, Std: {build_time_ratio_stats['std']}, "
        f"Min: {build_time_ratio_stats['min']}, Max: {build_time_ratio_stats['max']}\n"

        f"Build Time to Exact Solver Time Ratio - Median: {build_time_ratio_exact_stats['median']}, "
        f"Mean: {build_time_ratio_exact_stats['mean']}, Std: {build_time_ratio_exact_stats['std']}, "
        f"Min: {build_time_ratio_exact_stats['min']}, Max: {build_time_ratio_exact_stats['max']}\n"

        f"Build Time to Approx Solver Time Ratio - Median: {build_time_ratio_approx_stats['median']}, "
        f"Mean: {build_time_ratio_approx_stats['mean']}, Std: {build_time_ratio_approx_stats['std']}, "
        f"Min: {build_time_ratio_approx_stats['min']}, Max: {build_time_ratio_approx_stats['max']}\n\n"

        f"Approximate Solver Time (Reduced) - Median: {approximate_time_stats_reduced['median']}, "
        f"Mean: {approximate_time_stats_reduced['mean']}, Std: {approximate_time_stats_reduced['std']}, "
        f"Min: {approximate_time_stats_reduced['min']}, Max: {approximate_time_stats_reduced['max']}\n"

        f"Exact Solver Time (Reduced) - Median: {exact_time_stats_reduced['median']}, "
        f"Mean: {exact_time_stats_reduced['mean']}, Std: {exact_time_stats_reduced['std']}, "
        f"Min: {exact_time_stats_reduced['min']}, Max: {exact_time_stats_reduced['max']}\n"

        f"Time Ratio (Reduced) - Median: {time_ratio_stats_reduced['median']}, "
        f"Mean: {time_ratio_stats_reduced['mean']}, Std: {time_ratio_stats_reduced['std']}, "
        f"Min: {time_ratio_stats_reduced['min']}, Max: {time_ratio_stats_reduced['max']}\n"

        f"Time Ratio Without Building (Reduced) - Median: {time_ratio_without_building_stats_reduced['median']}, "
        f"Mean: {time_ratio_without_building_stats_reduced['mean']}, Std: {time_ratio_without_building_stats_reduced['std']}, "
        f"Min: {time_ratio_without_building_stats_reduced['min']}, Max: {time_ratio_without_building_stats_reduced['max']}\n"

        f"Cost Ratio (Reduced) - Median: {cost_ratio_stats_reduced['median']}, "
        f"Mean: {cost_ratio_stats_reduced['mean']}, Std: {cost_ratio_stats_reduced['std']}, "
        f"Min: {cost_ratio_stats_reduced['min']}, Max: {cost_ratio_stats_reduced['max']}\n"

        f"Build Time Ratio (Reduced) - Median: {build_time_ratio_stats_reduced['median']}, "
        f"Mean: {build_time_ratio_stats_reduced['mean']}, Std: {build_time_ratio_stats_reduced['std']}, "
        f"Min: {build_time_ratio_stats_reduced['min']}, Max: {build_time_ratio_stats_reduced['max']}\n"

        f"Build Time to Exact Solver Time Ratio (Reduced) - Median: {build_time_ratio_exact_stats_reduced['median']}, "
        f"Mean: {build_time_ratio_exact_stats_reduced['mean']}, Std: {build_time_ratio_exact_stats_reduced['std']}, "
        f"Min: {build_time_ratio_exact_stats_reduced['min']}, Max: {build_time_ratio_exact_stats_reduced['max']}\n"

        f"Build Time to Approx Solver Time Ratio (Reduced) - Median: {build_time_ratio_approx_stats_reduced['median']}, "
        f"Mean: {build_time_ratio_approx_stats_reduced['mean']}, Std: {build_time_ratio_approx_stats_reduced['std']}, "
        f"Min: {build_time_ratio_approx_stats_reduced['min']}, Max: {build_time_ratio_approx_stats_reduced['max']}\n\n"

        f"Time Ratio Between Exact Solver - Median: {time_ratio_between_exact_stats['median']}, "
        f"Mean: {time_ratio_between_exact_stats['mean']}, Std: {time_ratio_between_exact_stats['std']}, "
        f"Min: {time_ratio_between_exact_stats['min']}, Max: {time_ratio_between_exact_stats['max'] }, Over 1: {exact_more_time_on_reduced} \n"

        f"Time Ratio Between Approx Solver - Median: {time_ratio_between_approx_stats['median']}, "
        f"Mean: {time_ratio_between_approx_stats['mean']}, Std: {time_ratio_between_approx_stats['std']}, "
        f"Min: {time_ratio_between_approx_stats['min']}, Max: {time_ratio_between_approx_stats['max']}, Over 1: {approx_more_time_on_reduced}\n"
    )


    # Write the output data to a file
    with open('experiments/analyse_results/overall_statistics.txt', 'w') as file:
        file.write(output_data)

    # Write the cost pairs to the file
    with open('experiments/analyse_results/cost_pairs.txt', 'w') as file:
        for i in range(len(exact_solver_cost)):
            file.write(f"({exact_solver_cost[i]}, {approximate_solver_cost[i]})\n")
