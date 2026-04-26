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
    def improvement_task(self) -> Task:
        return Task(
            config=self._config['improvement_task'],
            agent=self._agents_obj.improver()
        )
    
    @task
    def issueanalysis_task(self) -> Task:
        return Task(
            config=self._config['issueanalysis_task'],
            context=[self.improvement_task()],
            agent=self._agents_obj.issueanalyzer()
        )
    
    def _get_config(self, path: str) -> dict:
        self._logger.info("Loading tasks configuration file")
        with open(path, "r") as f:
            tasks_config = yaml.safe_load(f)
        return tasks_config
    



'''
JSON output only. Start with {, end with }. No explanation, analysis, markdown, tags, or extra text before/after JSON.
    You are a deterministic data extraction engine. You map user queries to a FIXED SCHEMA. 
    You are FORBIDDEN from using any value not found in the ALLOWED lists.
    STRICTLY use only allowed list for category/subcategory and intent.
    Dont mention near city or near user house in address field.
    Must add improved version of query. Must make the JSON format to stringify.
    No similar version of category and subcategory. Use only the allowed list and match with category and subcategory.
    No explanation.
    No analysis.
    No extra text.
    No markdown.
    No extra uses of token.
    No shortening of subcategory or category. Use the exact same name as in allowed list.
    IMPORTANT No <|...|> tokens.
    STRICTLY provide ONLY JSON output is expected.
    Return ONLY valid JSON with the following structure:
      {{
          "query": "Original query of user",
          "improved_query": "Improved version of user query",
          "location": {{
              "google_maps_link": "https://www.google.com/maps?q=lat,lng",
              "location_address": {
                  "address": "Building address, landmark",
                  "city": "city",
                  "state": "state",
                  "country": "country",
                  "postcode": "postcode",
                  "raw": "raw output"
              }
          }},
          "intent": "must be one of: [complaint, report, emergency, account, unknown, assistance]",
          "category": "Must be one best of these category [Account, Road, Water Supply, Waste, Electricity, Public Health, Sewage, Street Lighting, Drainage, Traffic, Public Safety, Parks, Encroachment, Pollution, Construction, Animals, Government Services, Toilets, Other]",
          "subcategory": "Must be one best of these subcategory and match with category [Login Assistance, Signup Assistance, Password Reset, Account Verification, Other Accounts Assistance, Pothole, Road Damage, Footpath Issue, Bridge Damage, Lane Marking Issue, No Water Supply, Water Leakage, Low Water Pressure, Contaminated Water, Garbage Not Collected, Garbage Dump, Overflowing Dustbin, Improper Waste Disposal, Recycling Issue, Power Outage, Frequent Power Cuts, Electric Pole Damage, Loose or Exposed Wiring, Disease Spread, Mosquito Breeding, Food Safety Issue, Dead Animal, Sewage Overflow, Blocked Sewer, Open Drain, Foul Smell, Street Light Not Working, Flickering Street Light, Damaged Light Pole, Water Logging, Blocked Drain, Overflowing Drain, Flooded Road, Traffic Jam, Traffic Signal Not Working, Illegal Parking, Road Obstruction, Open Manhole, Unsafe Structure, Theft-Prone Area, Park Maintenance Issue, Broken Equipment, Park Cleanliness Issue, Footpath Encroachment, Illegal Street Occupation, Air Pollution, Water Pollution, Noise Pollution, Dust Pollution, Unauthorized Building, Construction Without Permit, Stray Dogs, Cattle on Road, Animal Attack, Service Delay, Staff Misconduct, Document Issue, Unclean Toilet, No Water in Toilet, Toilet Maintenance Issue, General Complaint, Uncategorized Issue, Unspecified Request]"
          "resolution": "One short actionable fix or next step suggestion",
          "precaution": [
              "List of 2-4 safety precautions relevant to the issue"
          ]
      }}
'''