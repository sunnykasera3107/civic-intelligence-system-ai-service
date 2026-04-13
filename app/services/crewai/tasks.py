import logging
import os


from crewai import Task
from crewai.project import task, CrewBase
import yaml

from app.services.crewai.agents import CrewAgents


@CrewBase
class CrewTasks:

    task_config_path = "config/tasks.yaml"

    def __init__(self, agent_obj: CrewAgents = None):
        self._logger = logging.getLogger(__name__)
        self._config = self._get_config(
            os.path.join("app/services/crewai", self.task_config_path)
        )
        self._agents_obj = agent_obj or CrewAgents()

    @task
    def issueanalysis_task(self) -> Task:
        return Task(
            config=self._config['issueanalysis_task'],
            agent=self._agents_obj.issueanalyzer()
        )
    
    def _get_config(self, path: str) -> dict:
        self._logger.info("Loading tasks configuration file")
        with open(path, "r") as f:
            tasks_config = yaml.safe_load(f)
        return tasks_config