def calculate_risk(blockage, rain_score):
    """
    Calculate drain risk score from blockage and rain score.

    blockage: 0-100
    rain_score: 0-100

    Returns:
        risk_score: 0-100
        status: GREEN / YELLOW / RED
    """

    # Weighted risk formula
    risk_score = (0.7 * blockage) + (0.3 * rain_score)

    # Keep score between 0 and 100
    risk_score = max(0, min(100, risk_score))

    # Status thresholds
   # Status thresholds
if blockage > 75 or risk_score >= 70:
    status = "RED"
elif risk_score >= 40:
    status = "YELLOW"
else:
    status = "GREEN"
    return round(risk_score, 2), status


def rain_score_from_forecast(rain_probability):
    """
    Convert forecast rain probability into a 0-100 rain score.
    """

    return max(0, min(100, rain_probability))


# -------------------------
# TEST CASES
# -------------------------

if __name__ == "__main__":
    test_cases = [
        (0, 0),
        (30, 20),
        (60, 40),
        (90, 30),
        (50, 80),
        (80, 80),
    ]

    print("RISK CALCULATION TESTS")
    print("-" * 50)

    for blockage, rain_score in test_cases:
        score, status = calculate_risk(blockage, rain_score)

        print(
            f"Blockage: {blockage}% | "
            f"Rain Score: {rain_score} | "
            f"Risk Score: {score} | "
            f"Status: {status}"
        )
