"""
Coordinator Agent.
Orchestrates agent pipelines and acts as the entry point for complete workflow execution runs.
Delegates entirely to backend/app/coordinator/coordinator.py.
"""

import logging
from typing import Any, Dict

from backend.app.agents.base import BaseAgent
from backend.app.types import AgentResult
from backend.app.coordinator.coordinator import AQIntelCoordinator

logger = logging.getLogger("aqintel.agents.coordinator")


class CoordinatorAgent(BaseAgent):
    """
    Entry point orchestration agent.
    """

    def __init__(self) -> None:
        super().__init__(name="CoordinatorAgent")
        self.coordinator = AQIntelCoordinator()

    async def execute(self, *args, **kwargs) -> AgentResult:
        """
        Main pipeline synchronous execution block.
        Expects keyword arguments for environmental observation:
          - latitude: float
          - longitude: float
          - city: Optional[str]
          - ward: Optional[str]
        """
        self.logger.info("CoordinatorAgent: starting synchronous workflow execution...")
        try:
            decision = await self.coordinator.run(observation=kwargs)
            return AgentResult(
                agent_name=self.name,
                success=True,
                data={"decision_package": decision.model_dump(mode="json")}
            )
        except Exception as e:
            err_msg = f"Coordinator pipeline execution failed: {e}"
            self.logger.error(err_msg, exc_info=True)
            return AgentResult(
                agent_name=self.name,
                success=False,
                error_message=err_msg
            )

    async def execute_async(self, *args, **kwargs) -> AgentResult:
        """
        Main pipeline asynchronous execution wrapper.
        """
        self.logger.info("CoordinatorAgent: starting asynchronous workflow execution...")
        try:
            decision = await self.coordinator.run_async(observation=kwargs)
            return AgentResult(
                agent_name=self.name,
                success=True,
                data={"decision_package": decision.model_dump(mode="json")}
            )
        except Exception as e:
            err_msg = f"Coordinator async pipeline execution failed: {e}"
            self.logger.error(err_msg, exc_info=True)
            return AgentResult(
                agent_name=self.name,
                success=False,
                error_message=err_msg
            )

    def health(self) -> Dict[str, Any]:
        """
        Pulls current system component health checks.
        """
        return self.coordinator.health_check()
