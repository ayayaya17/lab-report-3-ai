import streamlit as st

st.title("Scholarship Advisory – Rule-Based System")

# --- INTERNAL RULES (hidden from user) ---
rules = [
    {
        "name": "Top merit candidate",
        "priority": 100,
        "conditions": [
            ["cgpa", ">=", 3.7],
            ["co_curricular_score", ">=", 80],
            ["family_income", "<=", 8000],
            ["disciplinary_actions", "==", 0]
        ],
        "action": {
            "decision": "AWARD_FULL",
            "reason": "Excellent academic & co-curricular performance, with acceptable need"
        }
    },
    {
        "name": "Good candidate - partial scholarship",
        "priority": 80,
        "conditions": [
            ["cgpa", ">=", 3.3],
            ["co_curricular_score", ">=", 60],
            ["family_income", "<=", 12000],
            ["disciplinary_actions", "<=", 1]
        ],
        "action": {
            "decision": "AWARD_PARTIAL",
            "reason": "Good academic & involvement record with moderate need"
        }
    },
    {
        "name": "Need-based review",
        "priority": 70,
        "conditions": [
            ["cgpa", ">=", 2.5],
            ["family_income", "<=", 4000]
        ],
        "action": {
            "decision": "REVIEW",
            "reason": "High need but borderline academic score"
        }
    },
    {
        "name": "Low CGPA – not eligible",
        "priority": 95,
        "conditions": [
            ["cgpa", "<", 2.5]
        ],
        "action": {
            "decision": "REJECT",
            "reason": "CGPA below minimum scholarship requirement"
        }
    },
    {
        "name": "Serious disciplinary record",
        "priority": 90,
        "conditions": [
            ["disciplinary_actions", ">=", 2]
        ],
        "action": {
            "decision": "REJECT",
            "reason": "Too many disciplinary records"
        }
    }
]

# --- USER INPUT SECTION ---
st.subheader("📘 Applicant Information")

cgpa = st.number_input("CGPA", 0.0, 4.0, 3.5)
family_income = st.number_input("Monthly Family Income (RM)", 0, 50000, 3000)
co_score = st.number_input("Co-curricular Score (0–100)", 0, 100, 70)
community_hours = st.number_input("Community Service Hours", 0, 500, 20)
semester = st.number_input("Current Semester", 1, 12, 3)
disciplinary_actions = st.number_input("Disciplinary Actions", 0, 10, 0)

applicant = {
    "cgpa": cgpa,
    "family_income": family_income,
    "co_curricular_score": co_score,
    "community_hours": community_hours,
    "semester": semester,
    "disciplinary_actions": disciplinary_actions,
}

# --- RULE ENGINE FUNCTION ---
def evaluate_rules(rules, facts):
    matched_rules = []

    for rule in rules:
        is_match = True
        for cond in rule["conditions"]:
            field, op, value = cond
            fact_value = facts[field]

            if op == ">=" and not (fact_value >= value): is_match = False
            if op == "<=" and not (fact_value <= value): is_match = False
            if op == ">" and not (fact_value > value): is_match = False
            if op == "<" and not (fact_value < value): is_match = False
            if op == "==" and not (fact_value == value): is_match = False

        if is_match:
            matched_rules.append(rule)

    if not matched_rules:
        return {"decision": "NO_DECISION", "reason": "No rules matched"}

    best_rule = sorted(matched_rules, key=lambda x: -x["priority"])[0]
    return best_rule["action"]

# --- RUN EVALUATION ---
if st.button("Evaluate"):
    result = evaluate_rules(rules, applicant)

    st.subheader("Scholarship Decision")
    st.write("**Decision:**", result["decision"])
    st.write("**Reason:**", result["reason"])
