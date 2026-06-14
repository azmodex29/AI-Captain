class RiskFusionEngine:
    def __init__(self, piracy_weight=0.6, weather_weight=0.4):
        self.piracy_weight = piracy_weight
        self.weather_weight = weather_weight

    def calculate_overall_risk(self, piracy_score, weather_score):
        """
        Combines different risk scores into a single overall risk score.
        Weights can be adjusted based on user preference (Safest vs Fastest).
        """
        overall_score = (piracy_score * self.piracy_weight) + (weather_score * self.weather_weight)
        
        # Ensure it's between 0 and 100
        return min(max(round(overall_score), 0), 100)

    def get_risk_label(self, score):
        if score < 20:
            return "Low"
        elif score < 50:
            return "Moderate"
        elif score < 75:
            return "High"
        else:
            return "Extreme"
