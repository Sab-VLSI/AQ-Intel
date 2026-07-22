"""
Urban Memory Agent.
Orchestrates Case-Based Reasoning actions, storing incidents, retrieving diverse cases, and logging outcomes.
"""

import logging
from typing import Any, Dict

from backend.app.agents.base import BaseAgent
from backend.app.types import AgentResult
from backend.app.ml.urban_memory.memory_service import MemoryService
from backend.app.schemas.memory_case import MemoryCase

logger = logging.getLogger("aqintel.agents.urban_memory")

class UrbanMemoryAgent(BaseAgent):
    """
    Coordinates urban memory read/write storage and retrieval queries.
    """

    def __init__(self, service: MemoryService = None) -> None:
        super().__init__(name="UrbanMemoryAgent")
        self.service = service or MemoryService()

    async def execute(self, *args, **kwargs) -> AgentResult:
        """
        Executes memory commands based on the action parameter.
        Expects:
          - action: "store", "retrieve", "record_intervention", "record_outcome", or "get_statistics"
        """
        action = kwargs.get("action")
        if not action:
            err_msg = "Execution rejected: missing required 'action' parameter."
            self.logger.error(err_msg)
            return AgentResult(agent_name=self.name, success=False, error_message=err_msg)

        self.logger.info(f"UrbanMemoryAgent: processing action '{action}'...")

        try:
            if action == "store":
                case_data = kwargs.get("memory_case")
                if not case_data:
                    raise ValueError("Missing 'memory_case' parameter for store action.")

                if isinstance(case_data, dict):
                    case = MemoryCase(**case_data)
                elif isinstance(case_data, MemoryCase):
                    case = case_data
                else:
                    raise TypeError("Parameter 'memory_case' must be dict or MemoryCase.")

                self.service.store_case(case)
                return AgentResult(
                    agent_name=self.name,
                    success=True,
                    data={"case_id": case.case_id}
                )

            elif action == "retrieve":
                query_case = kwargs.get("query_case")
                if not query_case:
                    raise ValueError("Missing 'query_case' parameter for retrieve action.")
                
                top_n = int(kwargs.get("top_n", 5))
                
                # Normalize query_case to dictionary
                if isinstance(query_case, MemoryCase):
                    query_dict = query_case.model_dump(mode="json")
                elif isinstance(query_case, dict):
                    query_dict = query_case
                else:
                    raise TypeError("Parameter 'query_case' must be dict or MemoryCase.")

                matches = self.service.retrieve_cases(query_dict, top_n=top_n)
                return AgentResult(
                    agent_name=self.name,
                    success=True,
                    data={"similar_cases": matches}
                )

            elif action == "record_intervention":
                case_id = kwargs.get("case_id")
                actual_action = kwargs.get("actual_action")
                if not case_id or not actual_action:
                    raise ValueError("Missing 'case_id' or 'actual_action' for recording intervention.")

                self.service.record_intervention(case_id, actual_action)
                return AgentResult(agent_name=self.name, success=True, data={})

            elif action == "record_outcome":
                case_id = kwargs.get("case_id")
                if not case_id:
                    raise ValueError("Missing 'case_id' parameter for recording outcome.")

                aqi_24 = kwargs.get("aqi_24h")
                aqi_48 = kwargs.get("aqi_48h")
                aqi_72 = kwargs.get("aqi_72h")

                self.service.record_outcome(
                    case_id=case_id,
                    aqi_24h=float(aqi_24) if aqi_24 is not None else None,
                    aqi_48h=float(aqi_48) if aqi_48 is not None else None,
                    aqi_72h=float(aqi_72) if aqi_72 is not None else None
                )
                return AgentResult(agent_name=self.name, success=True, data={})

            elif action == "get_statistics":
                stats = self.service.get_statistics()
                return AgentResult(agent_name=self.name, success=True, data=stats)

            else:
                raise ValueError(f"Unknown memory action: '{action}'")

        except Exception as e:
            err_msg = f"UrbanMemoryAgent action '{action}' failed: {e}"
            self.logger.error(err_msg, exc_info=True)
            return AgentResult(agent_name=self.name, success=False, error_message=err_msg)
