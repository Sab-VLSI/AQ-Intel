"""
Decision Simulator Agent.
Delegates all simulation logic to DecisionSimulatorService.
"""

import logging
from typing import Any, Dict, List

from backend.app.agents.base import BaseAgent
from backend.app.types import AgentResult
from backend.app.ml.decision_simulator.decision_simulator_service import DecisionSimulatorService

logger = logging.getLogger("aqintel.agents.decision_simulator")


class DecisionSimulatorAgent(BaseAgent):
    """
    Receives current event state, executes counterfactual simulations,
    and returns ranked intervention recommendations.
    Agent contains no simulation logic — fully delegated to the service layer.
    """

    def __init__(self, service: DecisionSimulatorService = None) -> None:
        super().__init__(name="DecisionSimulatorAgent")
        self.service = service or DecisionSimulatorService()

    async def execute(self, *args, **kwargs) -> AgentResult:
        """
        Dispatches simulation actions.
        Supported actions:
          - "simulate"          — single intervention
          - "simulate_multiple" — composed multi-intervention scenario
          - "rank"              — all interventions ranked
        """
        action = kwargs.get("action", "rank")
        base_features: Dict[str, Any] = kwargs.get("base_features", {})
        query_case_dict: Dict[str, Any] = kwargs.get("query_case_dict", base_features)

        if not base_features:
            err = "Missing required 'base_features' parameter."
            self.logger.error(err)
            return AgentResult(agent_name=self.name, success=False, error_message=err)

        try:
            if action == "simulate":
                intervention_id = kwargs.get("intervention_id")
                if not intervention_id:
                    raise ValueError("Missing 'intervention_id' for 'simulate' action.")

                result = self.service.simulate(
                    base_features=base_features,
                    intervention_id=intervention_id,
                    query_case_dict=query_case_dict,
                )
                return AgentResult(agent_name=self.name, success=True, data=result)

            elif action == "simulate_multiple":
                intervention_ids: List[str] = kwargs.get("intervention_ids", [])
                if not intervention_ids:
                    raise ValueError("Missing 'intervention_ids' for 'simulate_multiple' action.")

                result = self.service.simulate_multiple(
                    base_features=base_features,
                    intervention_ids=intervention_ids,
                    scenario_name=kwargs.get("scenario_name"),
                    query_case_dict=query_case_dict,
                )
                return AgentResult(agent_name=self.name, success=True, data=result)

            elif action == "rank":
                ranked = self.service.rank(
                    base_features=base_features,
                    query_case_dict=query_case_dict,
                )
                return AgentResult(
                    agent_name=self.name,
                    success=True,
                    data={"ranked_interventions": ranked, "total": len(ranked)},
                )

            else:
                raise ValueError(f"Unknown action '{action}'. Valid: simulate, simulate_multiple, rank.")

        except Exception as e:
            err_msg = f"DecisionSimulatorAgent action '{action}' failed: {e}"
            self.logger.error(err_msg, exc_info=True)
            return AgentResult(agent_name=self.name, success=False, error_message=err_msg)
