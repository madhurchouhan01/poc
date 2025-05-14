from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from hypermindz.tools.custom_tool import calculate_channel_metrics

@CrewBase
class SensitivityCrew():
    agents_config = "config/agents.yaml"
    tasks_config = "config/tasks.yaml"

    @agent
    def  sensitivity_analysis_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['sensitivity_analysis_agent'],
            tools=[calculate_channel_metrics],
            verbose=True,
        )

    @task
    def analyze_sensitivity(self) -> Task:
        return Task(
            config=self.tasks_config['analyze_sensitivity'],
            agent=self.sensitivity_analysis_agent(),
        )

    @crew
    def crew(self) -> Crew:
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
        )