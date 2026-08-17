def get_precautions(risk):
    if risk == "HIGH RISK":
        return [
            "Evacuate immediately",
            "Avoid open areas",
            "Follow official alerts"
        ]
    elif risk == "MODERATE RISK":
        return [
            "Stay alert",
            "Avoid travel",
            "Keep emergency kit ready"
        ]
    else:
        return ["No immediate danger"]