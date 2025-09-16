import gurobipy as gp
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
import numpy as np
from tqdm import tqdm

from pabutools.analysis.justifiedrepresentation import is_in_core_lp
from pabutools.analysis.paretooptimality import is_pareto_optimal_lp
from pabutools.election import SatisfactionMeasure


def plot_metric(results):
    plt.figure(figsize=(10, 6))
    timeout = 30 * 60

    for source_dir, times in results.items():
        times.sort()
        n = len(times)
        x = [100 * i / (n - 1) for i in range(n)]
        nt = len([t for t in times if t < timeout])
        avg = sum([t for t in times if t < timeout]) / nt
        plt.scatter(x, times, s=5, label=f"{source_dir} (avg: {avg:.4f}s)")

    plt.yscale("log")
    plt.xlabel("Percent of elections", fontsize=14)
    plt.ylabel("Time (seconds)", fontsize=14)
    plt.xticks(fontsize=12)
    plt.yticks(fontsize=12)
    plt.xlim(0, 100)
    plt.gca().xaxis.set_major_formatter(mtick.PercentFormatter())
    plt.legend(markerscale=3, fontsize=12)
    plt.grid()
    plt.show()


def plot_results(results):
    plot_metric(results["is_in_core"])
    plot_metric(results["is_pareto_optimal"])


def plot_status(status):
    metrics = ["Core", "Pareto Optimality"]
    results = {
        "Satisfied": np.array([status["core"][True], status["po"][True]]),
        "Not satisfied": np.array([status["core"][False], status["po"][False]]),
    }
    width = 0.6

    fig, ax = plt.subplots(figsize=(8, 6))
    bottom = np.zeros(2)

    for res, count in results.items():
        p = ax.bar(metrics, count, width, label=res, bottom=bottom)
        bottom += count
        ax.bar_label(p, label_type="center", fontsize=20)

    plt.xticks(fontsize=14)
    plt.yticks(fontsize=14)
    ax.legend(loc="lower left", fontsize=14)
    plt.show()


def measure_execution_times(
    elections,
    outcomes,
    sat_class: type[SatisfactionMeasure],
    env: gp.Env | None = None,
    relaxations: bool = False,
    branching_priority: bool = False,
    start_hint_vals: bool = False,
    voters_removal: bool = False,
    essential_projects: bool = False,
):
    times = {
        "is_in_core": {
            source_dir: []
            for source_dir in elections
        },
        "is_pareto_optimal": {
            source_dir: []
            for source_dir in elections
        },
    }
    results = {
        "core": {True: 0, False: 0, None: 0},
        "po": {True: 0, False: 0, None: 0},
    }

    for source_dir in elections:
        for i, (instance, profile) in enumerate(tqdm(elections[source_dir])):
            budget_allocation = outcomes[source_dir][i]
            status, exec_time, blocking_coalition = is_in_core_lp(
                                                        instance,
                                                        profile,
                                                        sat_class,
                                                        budget_allocation,
                                                        env=env,
                                                        relaxations=relaxations,
                                                        branching_priority=branching_priority,
                                                        start_hint_vals=start_hint_vals,
                                                        voters_removal=voters_removal,
                                                    )
            times["is_in_core"][source_dir].append(exec_time)
            results["core"][status] += 1

            status, exec_time, dominant_projects = is_pareto_optimal_lp(
                                                        instance,
                                                        profile,
                                                        sat_class,
                                                        budget_allocation,
                                                        env=env,
                                                        essential_projects=essential_projects,
                                                    )
            times["is_pareto_optimal"][source_dir].append(exec_time)
            results["po"][status] += 1

    return times, results
