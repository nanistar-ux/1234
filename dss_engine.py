def recommend_schemes(entities: dict) -> dict:
    """
    Recommend OR reject schemes based on eligibility.
    Returns both accepted and rejected schemes with reasons.
    """
    area = entities.get("area_ha") or 0
    coords = entities.get("coordinates")

    approved = []
    rejected = []
    trace = []

    # Rule 1: PM-KISAN → must have <2 ha, farmer identity required
    if 0 < area <= 2.0:
        approved.append("PM-KISAN (Income Support)")
        trace.append("Rule1: area <= 2 ha → Eligible for PM-KISAN")
    else:
        rejected.append({"scheme": "PM-KISAN", "reason": "Landholding > 2 ha"})
        trace.append("Rule1: area > 2 ha → Rejected PM-KISAN")

    # Rule 2: PMFBY → only if farmer has declared crops + land >1 ha
    if 1.0 < area <= 5.0:
        if entities.get("crop_declared", True):  # dummy condition
            approved.append("PMFBY (Crop Insurance)")
            trace.append("Rule2: 1–5 ha + crops declared → Eligible for PMFBY")
        else:
            rejected.append({"scheme": "PMFBY", "reason": "No crops declared"})
            trace.append("Rule2: Missing crops → Rejected PMFBY")
    else:
        rejected.append({"scheme": "PMFBY", "reason": "Landholding outside 1–5 ha"})
        trace.append("Rule2: area not in 1–5 ha → Rejected PMFBY")

    # Rule 3: Jal Jeevan Mission → only if no water assets
    water_pct = entities.get("assets_detected", {}).get("water", {}).get("pct", 0)
    if water_pct < 5:
        approved.append("Jal Jeevan Mission (Tap Water)")
        trace.append("Rule3: Water assets <5% → Eligible for JJM")
    else:
        rejected.append({"scheme": "Jal Jeevan Mission", "reason": "Adequate water sources already detected"})
        trace.append("Rule3: water assets >=5% → Rejected JJM")

    # Rule 4: PMAY-G → only if no house detected
    built_pct = entities.get("assets_detected", {}).get("built", {}).get("pct", 0)
    if built_pct < 10:
        approved.append("PMAY-G (Housing)")
        trace.append("Rule4: Few built assets → Eligible for PMAY-G")
    else:
        rejected.append({"scheme": "PMAY-G", "reason": "House already present"})
        trace.append("Rule4: Built assets >=10% → Rejected PMAY-G")

    # Rule 5: MGNREGA → large land or community work
    if area > 5.0:
        approved.append("MGNREGA (Employment & Works)")
        trace.append("Rule5: area >5 ha → Eligible for MGNREGA")
    else:
        rejected.append({"scheme": "MGNREGA", "reason": "Small holding, focus on other schemes"})
        trace.append("Rule5: area <=5 ha → Rejected MGNREGA")

    # Rule 6: Missing coordinates → reject auto, need manual field survey
    if not coords:
        rejected.append({"scheme": "All", "reason": "No GPS coordinates → Manual verification required"})
        trace.append("Rule6: Missing coordinates → Claim flagged for manual check")

    return {
        "approved": approved,
        "rejected": rejected,
        "trace": trace
    }
