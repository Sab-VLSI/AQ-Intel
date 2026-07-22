"""
Base Agent Class.
Defines the standard operational contract and lifecycle hooks for all agents.
"""

import logging
from abc import ABC, abstractmethod
from typing import Any
from backend.app.types import AgentResult

class BaseAgent(ABC):
    """
    Abstract base class for all system agents.
    Provides standard lifecycle interfaces and automated logging.
    """
    def __init__(self, name: str) -> None:
        self.name = name
        self.logger = logging.getLogger(f"aqintel.agents.{name.lower()}")

    async def initialize(self) -> None:
        """
        Runs agent initialization routines (e.g. warming up caches, database locks).
        """
        self.logger.info(f"Initializing agent: {self.name}")

    @abstractmethod
    async def execute(self, *args, **kwargs) -> AgentResult:
        """
        Core operational execution loop of the agent. Must return an AgentResult.
        """
        pass

    async def cleanup(self) -> None:
        """
        Performs post-execution cleanup actions.
        """
        self.logger.info(f"Cleaning up agent resources: {self.name}")
