class AdvisorService:
    @staticmethod
    def generate_recommendation(analysis_results):
        """
        Generates a human-readable recommendation based on route analysis.
        """
        dist = analysis_results.get('distance', 0)
        eta = analysis_results.get('eta', 0)
        p_risk = analysis_results.get('piracy_risk', 0)
        w_risk = analysis_results.get('weather_risk', 0)
        o_risk = analysis_results.get('overall_risk', 0)
        
        advice = []
        
        # Risk assessment
        if o_risk > 70:
            advice.append("CRITICAL: This route carries extreme risk. Consider alternative paths.")
        elif o_risk > 40:
            advice.append("CAUTION: Moderate to high risk detected. Ensure vessel security is heightened.")
        else:
            advice.append("SAFE: This route is considered relatively safe for navigation.")

        # Piracy specific
        if p_risk > 50:
            advice.append(f"Piracy risk is high ({p_risk}%). Multiple piracy zones intersected.")
        
        # Weather specific
        if w_risk > 50:
            advice.append(f"Adverse weather conditions detected ({w_risk}%). Expect heavy seas.")

        # Final summary
        summary = f"Route analysis complete. Total distance: {dist}nm, Estimated ETA: {eta} days. Overall risk score: {o_risk}/100."
        
        return {
            "summary": summary,
            "advice": advice,
            "overall_assessment": "Avoid" if o_risk > 70 else "Proceed with Caution" if o_risk > 40 else "Proceed"
        }
