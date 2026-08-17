def predict_risk(data):
    score = 0

    # Temperature risk
    if data["temp"] > 40:
        score += 2
    elif data["temp"] > 35:
        score += 1

    # Humidity risk
    if data["humidity"] > 80:
        score += 2

    # Wind risk
    if data["wind"] > 12:
        score += 3
    elif data["wind"] > 8:
        score += 2

    # Final decision
    if score >= 5:
        return "HIGH RISK"
    elif score >= 3:
        return "MODERATE RISK"
    else:
        return "SAFE"