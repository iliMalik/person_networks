
from db.queries.query_questions import get_yes_Ids

def screening_algo(session_id: str):

    # Get responses
    yes_ids = get_yes_Ids(session_id)

    # Define screening criteria
    criteria = {
        "MDD": {
            "core": [1, 2],  # Q1 or Q2
            "others": [3, 4, 11, 16, 17, 18, 34],  # Need 2+
            "rule": lambda core_yes, others_yes: (1 in core_yes or 2 in core_yes) and len(others_yes) >= 2
        },
        "GAD": {
            "core": [6],  # Q6
            "others": [7, 8, 9, 10],  # Need 2+
            "rule": lambda core_yes, others_yes: 6 in core_yes and len(others_yes) >= 2
        },
        "Panic": {
            "core": [8],  # Q8
            "others": [7, 9, 10],  # Need 1+
            "rule": lambda core_yes, others_yes: 8 in core_yes and len(others_yes) >= 1
        },
        "Bipolar": {
            "core": [5, 18],  # Q5 and Q18
            "others": [19, 12, 11],  # Need 1+
            "rule": lambda core_yes, others_yes: 5 in core_yes and 18 in core_yes and len(others_yes) >= 1
        },
        "OCD": {
            "core": [22, 23],  # Q22 and Q23
            "others": [24],  # Optional
            "rule": lambda core_yes, others_yes: 22 in core_yes and 23 in core_yes
        },
        "PTSD": {
            "core": [28],  # Q28
            "others": [29, 30, 4, 16, 34],  # Need 1+
            "rule": lambda core_yes, others_yes: 28 in core_yes and len(others_yes) >= 1
        },
        "ADHD": {
            "core": [11, 12],  # Q11 and Q12
            "others": [18, 19, 31],  # Need 1+
            "rule": lambda core_yes, others_yes: 11 in core_yes and 12 in core_yes and len(others_yes) >= 1
        },
        "Schizophrenia": {
            "core": [14, 15],  # Q14 or Q15
            "others": [13],  # Optional
            "rule": lambda core_yes, others_yes: 14 in core_yes or 15 in core_yes
        },
        "Eating": {
            "core": [25],  # Q25
            "others": [26, 27],  # Need 1+
            "rule": lambda core_yes, others_yes: 25 in core_yes and len(others_yes) >= 1
        },
        "Substance": {
            "core": [21],  # Q21
            "others": [19, 31],  # Optional
            "rule": lambda core_yes, others_yes: 21 in core_yes
        },
        "Suicide": {
            "core": [33, 34, 35],  # Any
            "others": [],
            "rule": lambda core_yes, others_yes: len(core_yes) >= 1,
            "note": "Immediate referral to crisis services or emergency care is advised."
        },
        "Functional": {
            "core": [31, 32],  # Any
            "others": [],
            "rule": lambda core_yes, others_yes: len(core_yes) >= 1
        }
    }

    # Apply criteria and calculate severity
    results = {}
    for disorder, config in criteria.items():
        core_yes = [qid for qid in config["core"] if qid in yes_ids]
        others_yes = [qid for qid in config["others"] if qid in yes_ids]
        flag = config["rule"](core_yes, others_yes)

        # Calculate severity
        total_required = len(config["core"]) + len(config["others"])
        matched_count = len(core_yes) + len(others_yes)
        severity = 0.0 if not flag else (matched_count / total_required * 100) if total_required > 0 else 0.0

        result = {
            "flag": flag,
            "core_matched": core_yes,
            "others_matched": others_yes,
            "severity": round(severity, 1),
            "matched_count": matched_count,
            "total_required": total_required
        }
        if "note" in config:
            result["note"] = config["note"]

        results[disorder] = result

    # Print for debugging

    return results










