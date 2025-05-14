import json
import copy



def calculate_channel_metrics(input_data: str, parameter: str) -> dict:
    """
    Perform sensitivity analysis by changing the given parameter over a range
    and calculating its impact on reach metrics.

    Args:
        input_data (str): JSON string containing all the data
        parameter (str): Name of the parameter to tweak

    Returns:
        dict: Mapping of varied parameter values to resulting metrics
    """

    data = json.loads(input_data)
    print(data)
    print(type(data))
    results = {}

    # Define tweak ranges for supported parameters
    tweak_ranges = {
        "Flight (months)": list(range(max(1, data["Inputs"]["Flight (months)"] - 3), data["Inputs"]["Flight (months)"] + 4)),  # +/- 3 months
        "Audience Size": [int(data["Inputs"]["Audience Size"] * r) for r in [0.8, 0.9, 1.0, 1.1, 1.2]],
        "US Adult Population": [int(data["Inputs"]["US Adult Population"] * r) for r in [0.9, 1.0, 1.1]],
        "Total Budget": [int(data["Total Budget"] * r) for r in [0.8, 0.9, 1.0, 1.1, 1.2]]
    }

    if parameter not in tweak_ranges:
        return {"error": f"Unsupported parameter for sensitivity analysis: {parameter}"}

    for value in tweak_ranges[parameter]:
        modified_data = copy.deepcopy(data)
        
        # Map parameter name to key in JSON
        if parameter == "Flight (months)":
            modified_data["Flight (months)"] = value
        elif parameter == "Audience Size":
            modified_data["Audience Size"] = value
        elif parameter == "US Adult Population":
            modified_data["US Adult Population"] = value
        elif parameter == "Total Budget":
            modified_data["Total Budget"] = value

        # Compute metrics
        sum_gross_imps = 0
        sum_target_imps = 0

        for channel_data in modified_data['Channels']:
            percentage_alloc = channel_data['Percent Allocation']
            cpm = channel_data['CPM']
            target_multiplier = channel_data['Target Comp Multiplier']

            monthly_budget = (modified_data["Total Budget"] * percentage_alloc) / modified_data["Flight (months)"]
            target_comp = modified_data["Inputs"]["Audience Size"] / modified_data["Inputs"]["US Adult Population"]
            target_audience_comp = target_comp * target_multiplier
            gross_imps = (monthly_budget / cpm) * 1000
            target_imps = target_audience_comp * gross_imps

            sum_gross_imps += gross_imps
            sum_target_imps += target_imps

        gross_unique_reach = sum_gross_imps / modified_data["Summary"]["Frequency"]['Gross']
        target_unique_reach = sum_target_imps / modified_data["Summary"]["Frequency"]['Target']
        gross_reach_percent = (gross_unique_reach / modified_data["Inputs"]["US Adult Population"]) * 100
        target_reach_percent = (target_unique_reach / modified_data["Inputs"]["Audience Size"]) * 100

        results[str(value)] = {
            "Gross Unique Reach": round(gross_unique_reach),
            "Target Unique Reach": round(target_unique_reach),
            "Gross Reach %": round(gross_reach_percent, 2),
            "Target Reach %": round(target_reach_percent, 2)
        }

    return {
        "parameter": parameter,
        "sensitivity_analysis": results
    }

with open('input_file.json', 'r') as file:
    data = file.read()

result = calculate_channel_metrics(data,"Flight (months)")
print(result)