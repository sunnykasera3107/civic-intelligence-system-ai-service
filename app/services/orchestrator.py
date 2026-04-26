import os
import json
import logging

from app.services.crewai.crew import MainCrew


class Orchestrator:
    def __init__(self, httpclient):
        self._logger = logging.getLogger(__name__)
        self._httpclient = httpclient
        logging.getLogger("crewai").setLevel(logging.ERROR)
        os.environ["LITELLM_LOG"] = "ERROR"
        self._crew = MainCrew()

    async def handler(self, query, messages: list = None, file_path: str = "", coord: tuple = None):
        user_query = json.dumps({"query": query, "coord": coord or ()})
        # self._logger.info(f"query: {user_query}")
        response = self._crew.maincrew().kickoff(inputs={"query": user_query})
        # self._logger.info(response.raw or response)

        return {"response": (response.raw or response)}

    async def close_connection(self):
        await self._httpclient.close()