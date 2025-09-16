import random

from pabutools.election import (
    Instance,
    Profile,
    SatisfactionMeasure,
)
from pabutools.rules import BudgetAllocation

from model import get_election


def random_rule(
    instance: Instance,
    profile: Profile,
    sat_class: type[SatisfactionMeasure] | None = None,
) -> BudgetAllocation:
    projects = list(instance)
    random.shuffle(projects)

    W = []
    remaining = instance.budget_limit
    for p in projects:
        if p.cost <= remaining:
            W.append(p)
            remaining -= p.cost
    return W


def bounded_overspending(
    instance: Instance,
    profile: Profile,
    sat_class: type[SatisfactionMeasure] | None = None,
    real_budget: int = 0
) -> BudgetAllocation:
    e = get_election(instance, profile, sat_class)

    W = set()
    costW = 0
    remaining = set(c for c in e.profile)
    endow = {i : 1.0 * e.budget / len(e.voters) for i in e.voters}
    ratio = {c : -1.0 for c in e.profile}
    while True:
        next_candidate = None
        lowest_ratio = float("inf")
        remaining_sorted = sorted(remaining, key=lambda c: ratio[c])
        best_util = 0
        for c in remaining_sorted:
            if ratio[c] >= lowest_ratio:
                break
            if costW + c.cost <= e.budget:
                supporters_sorted = sorted([i for i in e.profile[c]], key=lambda i: endow[i] / e.profile[c][i])
                util = sum(e.profile[c].values())
                money_used = 0
                last_rho = 0
                new_ratio = float("inf")
                for i in supporters_sorted:
                    alpha = min(1.0, (money_used + util * (endow[i] / e.profile[c][i])) / c.cost)
                    if round(alpha, 5) > 0 and round(util, 5) > 0:
                        rho = ((alpha * c.cost) - money_used) / (alpha * util)
                        if rho < last_rho:
                            break
                        if rho / alpha < new_ratio :
                            new_ratio = rho / alpha
                            new_rho = rho
                    util -= e.profile[c][i]
                    money_used += endow[i]
                    last_rho = endow[i] / e.profile[c][i]
                ratio[c] = new_ratio
                if ratio[c] < lowest_ratio:
                    lowest_ratio = ratio[c]
                    lowest_rho = new_rho
                    next_candidate = c
                    best_util = sum([e.profile[c][i] for i in e.profile[c]])
                elif ratio[c] == lowest_ratio:
                    util = sum([e.profile[c][i] for i in e.profile[c]])
                    if util > best_util:
                        next_candidate = c
                        best_util = util
        if next_candidate is None:
            break
        else:
            W.add(next_candidate)
            costW += next_candidate.cost
            remaining.remove(next_candidate)
            for i in e.profile[next_candidate]:
                endow[i] -= min(endow[i], lowest_rho * e.profile[next_candidate][i])
            if real_budget:  # optimization for 'increase-budget' completions
                if costW > real_budget:
                    return None
    return W
