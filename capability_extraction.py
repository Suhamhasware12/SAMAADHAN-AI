# ============================================================
# SAMAADHAN AI
# Capability Extraction Module
# ============================================================

"""
This module identifies the capabilities required to solve
a societal problem.

Current MVP:
    Transparent rule-based capability extraction.

The architecture can later be extended with richer NLP /
semantic models.
"""


# ------------------------------------------------------------
# Capability definitions for different problem domains
# ------------------------------------------------------------

DOMAIN_CAPABILITIES = {

    "agriculture": [
        "Agriculture / Plant Pathology",
        "AI/ML + Computer Vision",
        "IoT / Field Monitoring",
        "Hardware / Prototype Development"
    ],

    "waste": [
        "Waste Management",
        "AI/ML",
        "IoT / Sensors",
        "Hardware / Automation"
    ],

    "water": [
        "Water Management",
        "AI/ML / Data Analytics",
        "IoT / Sensors",
        "Environmental Science"
    ],

    "education": [
        "Education / Domain Expertise",
        "AI/ML / Data Analytics",
        "Web / Mobile Development",
        "User Research"
    ],

    "healthcare": [
        "Healthcare / Medical Expertise",
        "AI/ML / Data Analytics",
        "IoT / Sensors",
        "Software Development"
    ]
}


# ------------------------------------------------------------
# Keyword-based domain detection
# ------------------------------------------------------------

DOMAIN_KEYWORDS = {

    "agriculture": [
        "crop",
        "agriculture",
        "farmer",
        "farming",
        "plant",
        "soil",
        "pest",
        "disease",
        "leaf",
        "harvest"
    ],

    "waste": [
        "waste",
        "garbage",
        "recycling",
        "plastic",
        "trash",
        "dustbin",
        "segregation",
        "wet waste",
        "dry waste"
    ],

    "water": [
        "water",
        "river",
        "lake",
        "irrigation",
        "flood",
        "drainage",
        "pollution",
        "water quality"
    ],

    "education": [
        "student",
        "school",
        "college",
        "education",
        "learning",
        "teacher",
        "classroom",
        "exam"
    ],

    "healthcare": [
        "health",
        "hospital",
        "patient",
        "medical",
        "disease",
        "doctor",
        "diagnosis",
        "healthcare"
    ]
}


# ------------------------------------------------------------
# Detect problem domain
# ------------------------------------------------------------

def detect_domain(category="", description=""):
    """
    Detect the most relevant domain from category and
    problem description.
    """

    text = f"{category} {description}".lower()

    scores = {}

    for domain, keywords in DOMAIN_KEYWORDS.items():

        score = 0

        for keyword in keywords:

            if keyword in text:
                score += 1

        scores[domain] = score

    if not scores:
        return "general"

    best_domain = max(scores, key=scores.get)

    if scores[best_domain] == 0:

        # Fall back to category if no keyword is detected
        category_lower = category.lower()

        if category_lower in DOMAIN_CAPABILITIES:
            return category_lower

        return "general"

    return best_domain


# ------------------------------------------------------------
# Extract required capabilities
# ------------------------------------------------------------

def extract_capabilities(category="", description=""):
    """
    Identify capabilities required to address a problem.
    """

    domain = detect_domain(
        category,
        description
    )

    capabilities = DOMAIN_CAPABILITIES.get(
        domain,
        [
            "Domain Expertise",
            "AI/ML / Data Analytics",
            "Software Development",
            "Field Testing"
        ]
    )

    return {
        "domain": domain,
        "capabilities": capabilities
    }


# ------------------------------------------------------------
# Explain the capability extraction
# ------------------------------------------------------------

def explain_capabilities(category="", description=""):
    """
    Generate an explainable description of the
    capability extraction process.
    """

    result = extract_capabilities(
        category,
        description
    )

    domain = result["domain"]
    capabilities = result["capabilities"]

    return {
        "domain": domain,
        "capabilities": capabilities,
        "explanation": (
            "The system analysed the problem category and "
            "description and identified the capabilities "
            "required for a multidisciplinary solution."
        )
    }


# ------------------------------------------------------------
# Test the module directly
# ------------------------------------------------------------

if __name__ == "__main__":

    test_category = "Agriculture"

    test_description = (
        "Farmers are facing crop disease and need a system "
        "for disease detection and field monitoring."
    )

    result = explain_capabilities(
        test_category,
        test_description
    )

    print("\nSAMAADHAN AI - Capability Analysis")
    print("-----------------------------------")

    print("Detected Domain:")
    print(result["domain"])

    print("\nRequired Capabilities:")

    for capability in result["capabilities"]:
        print(f"- {capability}")

    print("\nExplanation:")
    print(result["explanation"])