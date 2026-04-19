from crewai import Crew, Process
from crewai.project import CrewBase, crew

from app.services.crewai.agents import CrewAgents
from app.services.crewai.tasks import CrewTasks


@CrewBase
class MainCrew:

    @crew
    def maincrew(self) -> Crew:
        agents = CrewAgents()
        tasks = CrewTasks()

        return Crew(
            agents=[agents.improver(), agents.issueanalyzer()],
            tasks=[tasks.improvement_task(), tasks.issueanalysis_task()]
        )