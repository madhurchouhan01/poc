import os
import json
from hypermindz.crew import SensitivityCrew

def run():
    # Dynamically resolve the path
    current_dir = os.path.dirname(__file__)
    input_path = os.path.join(current_dir, 'input_file.json')

    with open(input_path, 'r') as file:
        data = file.read()

    query = "How would changing the 'Flight (months)' affect my overall budget?"
    result = SensitivityCrew().crew().kickoff(inputs={"data": data, "query": query})

    output_path = os.path.join(current_dir, 'sensitivity_report.md')
    with open(output_path, 'w') as file:
        file.write(result.raw)
