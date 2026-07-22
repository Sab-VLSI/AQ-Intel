"""
Source Attribution Agent.
Orchestrates LightGBM predictions and Shapley attribution values to classify dominant emission sources.
"""

import logging
from typing import Any, Dict

from backend.app.agents.base import BaseAgent
from backend.app.types import AgentResult
from backend.app.ml.source_attribution.predictor import AttributionPredictor
from backend.app.schemas.features import FeatureVector

logger = logging.getLogger("aqintel.agents.source_attribution")

class SourceAttributionAgent(BaseAgent):
    """
    Coordinates emission classification using the explainable source attribution ML predictor.
    """

    def __init__(self, predictor: AttributionPredictor = None) -> None:
        super().__init__(name="SourceAttributionAgent")
        self.predictor = predictor or AttributionPredictor()

    async def execute(self, *args, **kwargs) -> AgentResult:
        """
        Runs predictions on the provided FeatureVector input.
        Expects:
          - feature_vector: FeatureVector or dict (flat schema)
        """
        self.logger.info("Executing source apportionment algorithm...")
        
        fv = kwargs.get("feature_vector")
        if fv is None:
            err_msg = "Execution rejected: missing required feature_vector parameter."
            self.logger.error(err_msg)
            return AgentResult(
                agent_name=self.name,
                success=False,
                error_message=err_msg
            )

        try:
            # Normalize to flat dictionary representation
            if isinstance(fv, FeatureVector):
                feature_dict = fv.model_dump(mode="json")
            elif isinstance(fv, dict):
                feature_dict = fv
            else:
                raise ValueError("Parameter feature_vector must be dict or FeatureVector Pydantic model.")

            # Calculate predictions and explanations
            prediction_output = self.predictor.predict_attribution(feature_dict)

            return AgentResult(
                agent_name=self.name,
                success=True,
                data=prediction_output
            )
        except Exception as e:
            err_msg = f"SourceAttributionAgent execution failure: {e}"
            self.logger.error(err_msg, exc_info=True)
            return AgentResult(
                agent_name=self.name,
                success=False,
                error_message=err_msg
            )
