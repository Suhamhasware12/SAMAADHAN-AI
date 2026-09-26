# ============================================================
# SAMAADHAN AI
# Matching & Collaboration Gap Detection Module
# ============================================================

"""
This module performs transparent capability-based matching.

It:
1. Compares required capabilities with stakeholder capabilities.
2. Classifies stakeholders as STRONG / GOOD / PARTIAL MATCH.
3. Calculates capability coverage.
4. Detects missing capabilities.
5. Recommends the type of partner required.
"""


# ------------------------------------------------------------
# Text normalization
# ------------------------------------------------------------

def normalize(text):
    """
    Convert text into a normalized form for comparison.
    """

    if not text:
        return ""

    return (
        text.lower()
        .replace("/", " ")
        .replace("+", " ")
        .replace("-", " ")
        .replace("_", " ")
    )


# ------------------------------------------------------------
# Tokenize capability text
# ------------------------------------------------------------

def tokenize(text):
    """
    Convert capability text into meaningful words.
    """

    normalized = normalize(text)

    stop_words = {
        "and",
        "the",
        "of",
        "for",
        "with",
        "in",
        "on"
    }

    words = normalized.split()

    return {
        word
        for word in words
        if word not in stop_words
        and len(word) > 1
    }


# ------------------------------------------------------------
# Capability similarity
# ------------------------------------------------------------

def capability_similarity(required, stakeholder_capability):
    """
    Calculate simple token-overlap similarity.

    Returns a value between 0 and 1.
    """

    required_tokens = tokenize(required)
    stakeholder_tokens = tokenize(stakeholder_capability)

    if not required_tokens or not stakeholder_tokens:
        return 0.0

    common_tokens = (
        required_tokens.intersection(stakeholder_tokens)
    )

    return len(common_tokens) / len(required_tokens)


# ------------------------------------------------------------
# Match a stakeholder against one capability
# ------------------------------------------------------------

def match_capability(required, stakeholder_capabilities):
    """
    Determine whether a stakeholder covers a required capability.

    Returns:
        status
        matched capability
        similarity
    """

    best_similarity = 0.0
    best_capability = None

    for capability in stakeholder_capabilities:

        similarity = capability_similarity(
            required,
            capability
        )

        if similarity > best_similarity:
            best_similarity = similarity
            best_capability = capability

    if best_similarity >= 1.0:
        status = "STRONG"

    elif best_similarity >= 0.5:
        status = "GOOD"

    elif best_similarity > 0:
        status = "PARTIAL"

    else:
        status = "NO MATCH"
        best_capability = None

    return {
        "status": status,
        "matched_capability": best_capability,
        "similarity": best_similarity
    }


# ------------------------------------------------------------
# Match stakeholder with all required capabilities
# ------------------------------------------------------------

def match_stakeholder(
    required_capabilities,
    stakeholder_capabilities
):
    """
    Match one stakeholder against all required capabilities.
    """

    results = []

    for required in required_capabilities:

        result = match_capability(
            required,
            stakeholder_capabilities
        )

        results.append({
            "required_capability": required,
            "status": result["status"],
            "matched_capability": result["matched_capability"],
            "similarity": result["similarity"]
        })

    # Determine overall match status

    strong_count = sum(
        1
        for result in results
        if result["status"] == "STRONG"
    )

    good_count = sum(
        1
        for result in results
        if result["status"] == "GOOD"
    )

    partial_count = sum(
        1
        for result in results
        if result["status"] == "PARTIAL"
    )

    if strong_count > 0:
        overall_status = "STRONG MATCH"

    elif good_count > 0:
        overall_status = "GOOD MATCH"

    elif partial_count > 0:
        overall_status = "PARTIAL MATCH"

    else:
        overall_status = "NO MATCH"

    matched_capabilities = [
        result["required_capability"]
        for result in results
        if result["status"] in [
            "STRONG",
            "GOOD",
            "PARTIAL"
        ]
    ]

    return {
        "overall_status": overall_status,
        "matched_capabilities": matched_capabilities,
        "details": results
    }


# ------------------------------------------------------------
# Match multiple stakeholders
# ------------------------------------------------------------

def compute_matches(
    required_capabilities,
    stakeholders
):
    """
    Compute matches for a list of stakeholders.

    Each stakeholder should contain:

        name
        capabilities
        type
    """

    matches = []

    for stakeholder in stakeholders:

        result = match_stakeholder(
            required_capabilities,
            stakeholder.get("capabilities", [])
        )

        matches.append({
            "name": stakeholder.get("name", ""),
            "type": stakeholder.get("type", ""),
            "capabilities": stakeholder.get(
                "capabilities",
                []
            ),
            "overall_status": result["overall_status"],
            "matched_capabilities": result[
                "matched_capabilities"
            ],
            "details": result["details"]
        })

    # Sort:
    # STRONG → GOOD → PARTIAL → NO MATCH

    priority = {
        "STRONG MATCH": 4,
        "GOOD MATCH": 3,
        "PARTIAL MATCH": 2,
        "NO MATCH": 1
    }

    matches.sort(
        key=lambda item: priority.get(
            item["overall_status"],
            0
        ),
        reverse=True
    )

    return matches


# ------------------------------------------------------------
# Capability coverage
# ------------------------------------------------------------

def calculate_coverage(
    required_capabilities,
    selected_stakeholders
):
    """
    Calculate which required capabilities are covered
    by the selected collaboration team.
    """

    covered = []
    missing = []

    for required in required_capabilities:

        is_covered = False

        for stakeholder in selected_stakeholders:

            result = match_capability(
                required,
                stakeholder.get("capabilities", [])
            )

            if result["status"] in [
                "STRONG",
                "GOOD"
            ]:
                is_covered = True
                break

        if is_covered:
            covered.append(required)

        else:
            missing.append(required)

    total = len(required_capabilities)

    covered_count = len(covered)

    coverage_ratio = (
        covered_count / total
        if total > 0
        else 0
    )

    return {
        "required": required_capabilities,
        "covered": covered,
        "missing": missing,
        "covered_count": covered_count,
        "total_required": total,
        "coverage_ratio": coverage_ratio
    }


# ------------------------------------------------------------
# Collaboration gap detection
# ------------------------------------------------------------

def detect_collaboration_gaps(
    required_capabilities,
    selected_stakeholders
):
    """
    Detect missing capabilities in the current team.
    """

    coverage = calculate_coverage(
        required_capabilities,
        selected_stakeholders
    )

    gaps = []

    for capability in coverage["missing"]:

        recommendation = recommend_partner_type(
            capability
        )

        gaps.append({
            "missing_capability": capability,
            "recommended_partner": recommendation
        })

    return {
        "covered": coverage["covered"],
        "missing": coverage["missing"],
        "coverage_ratio": coverage["coverage_ratio"],
        "gaps": gaps
    }


# ------------------------------------------------------------
# Partner recommendation
# ------------------------------------------------------------

def recommend_partner_type(missing_capability):
    """
    Recommend the type of partner required for a
    missing capability.
    """

    capability = normalize(
        missing_capability
    )

    if (
        "hardware" in capability
        or "prototype" in capability
        or "automation" in capability
    ):
        return "Industry / Hardware Partner"

    if (
        "iot" in capability
        or "sensor" in capability
        or "field monitoring" in capability
    ):
        return "IoT / Sensor Team"

    if (
        "ai" in capability
        or "machine learning" in capability
        or "computer vision" in capability
        or "data analytics" in capability
    ):
        return "AI/ML Team"

    if (
        "agriculture" in capability
        or "plant pathology" in capability
        or "environmental" in capability
        or "healthcare" in capability
        or "medical" in capability
        or "education" in capability
    ):
        return "Domain Expert / Research Partner"

    return "Relevant Domain Partner"


# ------------------------------------------------------------
# Generate human-readable explanation
# ------------------------------------------------------------

def explain_match(
    stakeholder_name,
    match_result
):
    """
    Generate an explainable matching statement.
    """

    status = match_result["overall_status"]

    matched = match_result[
        "matched_capabilities"
    ]

    if matched:

        capability_text = ", ".join(
            matched
        )

        return (
            f"{stakeholder_name} is a {status.lower()} "
            f"because it covers: {capability_text}."
        )

    return (
        f"{stakeholder_name} does not currently "
        f"cover the required capabilities."
    )


# ------------------------------------------------------------
# Demo / test
# ------------------------------------------------------------

if __name__ == "__main__":

    required_capabilities = [
        "Agriculture / Plant Pathology",
        "AI/ML + Computer Vision",
        "IoT / Field Monitoring",
        "Hardware / Prototype Development"
    ]

    stakeholders = [

        {
            "name": "AI/ML Student Team",
            "type": "University Team",
            "capabilities": [
                "AI/ML",
                "Computer Vision",
                "Data Analytics"
            ]
        },

        {
            "name": "IoT Innovation Team",
            "type": "University Team",
            "capabilities": [
                "IoT",
                "Sensors",
                "Field Monitoring"
            ]
        },

        {
            "name": "Agriculture Expert",
            "type": "Domain Expert",
            "capabilities": [
                "Agriculture",
                "Plant Pathology",
                "Crop Science"
            ]
        },

        {
            "name": "Hardware Innovation Partner",
            "type": "Industry Partner",
            "capabilities": [
                "Hardware",
                "Prototype Development",
                "Automation"
            ]
        }
    ]

    print("\nSAMAADHAN AI - Matching Engine")
    print("--------------------------------")

    matches = compute_matches(
        required_capabilities,
        stakeholders
    )

    print("\nSTAKEHOLDER MATCHES:\n")

    for match in matches:

        print(
            f"{match['name']} "
            f"-> {match['overall_status']}"
        )

        if match["matched_capabilities"]:

            print(
                "   Covers: "
                + ", ".join(
                    match["matched_capabilities"]
                )
            )

    # --------------------------------------------------------
    # Demonstrate collaboration gap detection
    # --------------------------------------------------------

    selected_team = [
        stakeholders[0],
        stakeholders[1],
        stakeholders[2]
    ]

    gap_result = detect_collaboration_gaps(
        required_capabilities,
        selected_team
    )

    print("\nCOLLABORATION GAP DETECTION")
    print("----------------------------")

    print(
        f"Coverage: "
        f"{len(gap_result['covered'])}/"
        f"{len(required_capabilities)}"
    )

    print("\nCovered:")

    for capability in gap_result["covered"]:
        print(f"- {capability}")

    print("\nMissing:")

    for capability in gap_result["missing"]:
        print(f"- {capability}")

    print("\nRECOMMENDATION:")

    for gap in gap_result["gaps"]:

        print(
            f"- Missing: "
            f"{gap['missing_capability']}"
        )

        print(
            f"  Recommended: "
            f"{gap['recommended_partner']}"
        )