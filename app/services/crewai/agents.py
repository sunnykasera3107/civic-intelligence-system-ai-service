import logging
import os
import yaml

from crewai import Agent, LLM
from crewai.project import agent, CrewBase

from app.pipelines.query_cleaner.cleaner import Cleaner


@CrewBase
class CrewAgents:

    agent_config_path = "config/agents.yaml"

    def __init__(self):
        self._logger = logging.getLogger(__name__)
        self._cleaner = Cleaner()
        self._config = self._get_config(
            os.path.join("app/services/crewai", self.agent_config_path)
        )
    
    def _get_config(self, path: str) -> dict:
        self._logger.info("Loading agent configuration file")
        with open(path, "r") as f:
            agents_config = yaml.safe_load(f)
        return agents_config
    
    def _get_llm(self) -> LLM:
        self._logger.info("Creating LLM object")
        # return LLM(
        #     model="groq/llama-3.3-70b-versatile"
        # )
        return LLM(
            model="ollama/gpt-oss:120b-cloud",
            base_url="http://host.docker.internal:11434"
        )
        
    @agent
    def improver(self) -> Agent:
        self._logger.info("Improver agent starting improvement")
        llm = self._get_llm()
        return Agent(
            config=self._config['improver'],  # type: ignore[index]
            llm=llm
        )
    
    @agent
    def issueanalyzer(self) -> Agent:
        self._logger.info("Issue Analyzer agent starting analysis")
        llm = self._get_llm()
        return Agent(
            config=self._config['issueanalyzer'],  # type: ignore[index]
            tools=[self._cleaner],
            llm=llm
        )