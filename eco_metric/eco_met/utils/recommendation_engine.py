def generate_recommendations(data):
    """
    Simple AI-like rule based recommendation engine
    """

    recommendations = []
    potential_reduction = 0

    # Benchmarks
    if data["car_distance"] > 60:
        recommendations.append("Use public transport or carpool at least 2 days per week.")
        recommendations.append("Avoid travelling during peak traffic hours")
        potential_reduction += 10

    if data["flight_hours"] > 50:
        recommendations.append("Reduce air travel or offset flights using carbon offset programs.")
        potential_reduction += 25

    if data["electricity"] > 200:
        recommendations.append("Switch to LED lights and unplug unused electronics.")
        recommendations.append("Don't leave electronics plugged")
        potential_reduction += 15

    if data["gas"] > 50:
        recommendations.append("Use energy-efficient cooking appliances.")
        potential_reduction += 10

    if data["meat_meals"] > 10:
        recommendations.append("Reduce red meat consumption and add vegetarian meals.")
        potential_reduction += 20

    if data["waste_kg"] > 5:
        recommendations.append("Start composting and improve waste segregation.")
        potential_reduction += 8

    if data["recycling"] < 2:
        recommendations.append("Increase recycling of plastics, paper, and metal.")
        potential_reduction += 5

    if data["water_liters"] > 30:
        recommendations.append("Install low-flow shower heads and reduce water usage.")
        potential_reduction += 6

    if data["online_orders"] > 5:
        recommendations.append("Combine online orders to reduce delivery emissions.")
        potential_reduction += 7

    if data["clothing"] > 3:
        recommendations.append("Buy sustainable clothing or reduce fast fashion purchases.")
        potential_reduction += 6

    if len(recommendations) == 4:
        recommendations.append("Great job! Your carbon habits are already eco-friendly.")

    return recommendations, potential_reduction