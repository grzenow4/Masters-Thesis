import os
import pickle
from tqdm import tqdm

from pabutools.election import (
    AbstractApprovalProfile,
    AbstractCardinalProfile,
    AbstractOrdinalProfile,
    parse_pabulib,
)


def load_pabulib_data(source_dir):
    elections = {
        "approval": [],
        "cardinal": [],
        "ordinal": [],
    }
    for file in os.listdir(os.path.join(source_dir)):
        if file.endswith(".pb"):
            instance, profile = parse_pabulib(os.path.join(source_dir, file))
            if isinstance(profile, AbstractApprovalProfile):
                elections["approval"].append((instance, profile))
            elif isinstance(profile, AbstractCardinalProfile):
                elections["cardinal"].append((instance, profile))
            elif isinstance(profile, AbstractOrdinalProfile):
                elections["ordinal"].append((instance, profile))

    print(f"""Found {len(elections["approval"]) + len(elections["cardinal"]) + len(elections["ordinal"])} elections with:\n- {len(elections["approval"])} approval elections\n- {len(elections["cardinal"])} cardinal elections\n- {len(elections["ordinal"])} ordinal elections""")
    return elections


def split_pabulib_data(elections, prof_type):
    result = {
        "all_10": [],
        "all_30": [],
        "all_50": [],
        "all_100": [],
        "all": [],
    }
    for election in elections[prof_type]:
        if len(election[0]) <= 10:
            result["all_10"].append(election)
        elif len(election[0]) <= 30:
            result["all_30"].append(election)
        elif len(election[0]) <= 50:
            result["all_50"].append(election)
        elif len(election[0]) <= 100:
            result["all_100"].append(election)
        else:
            result["all"].append(election)
    return result


def compute_outcomes(elections, sat_class, rule):
    outcomes = {
        "all_10": [],
        "all_30": [],
        "all_50": [],
        "all_100": [],
        "all": [],
    }
    for source_dir in elections:
        for instance, profile in tqdm(elections[source_dir]):
            outcome = rule(instance, profile, sat_class)
            outcomes[source_dir].append(outcome)
    return outcomes


def save_to_file(path, obj):
    with open(path, "wb") as f:
        pickle.dump(obj, f)


def load_from_file(path):
    with open(path, "rb") as f:
        return pickle.load(f)
