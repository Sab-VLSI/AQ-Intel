"""
Historical Dataset Agent.
Orchestrates the preprocessing, matching, merging, cleaning, profiling, and chronological splitting pipeline.
"""

import logging
from pathlib import Path
from typing import Any, Dict, List
import pandas as pd

from backend.app.agents.base import BaseAgent
from backend.app.types import AgentResult

# Import preprocessing pipeline components
from backend.app.ml.preprocessing.loaders.cpcb_loader import CPCBLoader
from backend.app.ml.preprocessing.loaders.openaq_loader import OpenAQLoader
from backend.app.ml.preprocessing.loaders.weather_loader import WeatherLoader
from backend.app.ml.preprocessing.loaders.firms_loader import FIRMSLoader
from backend.app.ml.preprocessing.loaders.osm_loader import OSMLoader

from backend.app.ml.preprocessing.merger import HistoricalDatasetMerger
from backend.app.ml.preprocessing.cleaner import DatasetCleaner
from backend.app.ml.preprocessing.validator import DatasetValidator
from backend.app.ml.preprocessing.dataset_statistics import DatasetStatisticsProfiler
from backend.app.ml.preprocessing.exporter import DatasetExporter
from backend.app.ml.preprocessing.preprocessing_report import PreprocessingReportCompiler
from backend.app.ml.preprocessing.config import TRAINING_DIR

logger = logging.getLogger("aqintel.agents.historicaldataset")

class HistoricalDatasetAgent(BaseAgent):
    """
    Orchestrates the offline data preparation pipeline.
    Implements incremental change tracking via input count files.
    """

    def __init__(self) -> None:
        super().__init__(name="HistoricalDatasetAgent")
        self.tracking_file = TRAINING_DIR / "last_processed.txt"
        
        # Instantiate pipeline components
        self.cpcb_loader = CPCBLoader()
        self.openaq_loader = OpenAQLoader()
        self.weather_loader = WeatherLoader()
        self.firms_loader = FIRMSLoader()
        self.osm_loader = OSMLoader()

        self.merger = HistoricalDatasetMerger()
        self.cleaner = DatasetCleaner()
        self.validator = DatasetValidator()
        self.profiler = DatasetStatisticsProfiler()
        self.exporter = DatasetExporter()
        self.report_compiler = PreprocessingReportCompiler()

    async def execute(self, *args, **kwargs) -> AgentResult:
        """
        Main execution script.
        """
        self.logger.info("HistoricalDatasetAgent: starting preprocessing pipeline execution...")

        try:
            # 1. Load raw dataframes
            cpcb_raw = self.cpcb_loader.load()
            openaq_raw = self.openaq_loader.load()
            weather_raw = self.weather_loader.load()
            firms_raw = self.firms_loader.load()
            osm_raw = self.osm_loader.load()

            # Compute sum of raw records to check for changes (Incremental Preprocessing check)
            total_raw_rows = len(cpcb_raw) + len(openaq_raw) + len(weather_raw) + len(firms_raw) + len(osm_raw)
            self.logger.info(f"Total raw source rows detected: {total_raw_rows}")

            if self._is_incremental_unchanged(total_raw_rows):
                msg = "Incremental check: No new records detected in raw dataset folders. Skipping reprocessing cycle."
                self.logger.info(msg)
                return AgentResult(
                    agent_name=self.name,
                    success=True,
                    data={"message": msg, "total_raw_rows": total_raw_rows, "reprocessed": False}
                )

            # 2. Validate and normalize inputs
            cpcb_norm = self.cpcb_loader.normalize(cpcb_raw) if self.cpcb_loader.validate(cpcb_raw) else pd.DataFrame()
            openaq_norm = self.openaq_loader.normalize(openaq_raw) if self.openaq_loader.validate(openaq_raw) else pd.DataFrame()
            weather_norm = self.weather_loader.normalize(weather_raw) if self.weather_loader.validate(weather_raw) else pd.DataFrame()
            firms_norm = self.firms_loader.normalize(firms_raw) if self.firms_loader.validate(firms_raw) else pd.DataFrame()
            osm_norm = self.osm_loader.normalize(osm_raw) if self.osm_loader.validate(osm_raw) else pd.DataFrame()

            # 3. Form unified primary air quality dataset
            # Concat normalized CPCB and OpenAQ observations
            primary_dfs = []
            source_names = []
            if not cpcb_norm.empty:
                primary_dfs.append(cpcb_norm)
                source_names.append("CPCB")
            if not openaq_norm.empty:
                primary_dfs.append(openaq_norm)
                source_names.append("OpenAQ")

            if not primary_dfs:
                err_msg = "No valid primary air quality inputs (CPCB/OpenAQ) found. Pipeline cannot run."
                self.logger.error(err_msg)
                return AgentResult(
                    agent_name=self.name,
                    success=False,
                    error_message=err_msg
                )

            primary_df = pd.concat(primary_dfs, ignore_index=True)
            primary_source_label = "+".join(source_names)

            # 4. Execute Merger
            merged_df = self.merger.merge(
                primary_df=primary_df,
                primary_source_name=primary_source_label,
                weather_df=weather_norm if not weather_norm.empty else None,
                fire_df=firms_norm if not firms_norm.empty else None,
                osm_df=osm_norm if not osm_norm.empty else None
            )

            # 5. Execute Data Cleaning
            cleaned_df, cleaning_stats = self.cleaner.clean(merged_df)

            # 6. Execute Dataset Validation Checks
            validation_report = self.validator.validate(cleaned_df)

            # 7. Generate Descriptive Profiles
            stats_profile = self.profiler.profile(cleaned_df)

            # 8. Export Splits & Lineage Metadata files
            self.exporter.export(cleaned_df, cleaning_stats, validation_report, source_names)

            # 9. Compile Markdown execution log
            self.report_compiler.compile(cleaning_stats, validation_report, stats_profile)

            # 10. Record tracking token for next incremental run
            self._save_incremental_token(total_raw_rows)

            return AgentResult(
                agent_name=self.name,
                success=True,
                data={
                    "total_raw_rows": total_raw_rows,
                    "final_training_rows": len(cleaned_df),
                    "reprocessed": True,
                    "validation_issues": validation_report.get("issues_found", 0)
                }
            )

        except Exception as e:
            err_msg = f"Preprocessing pipeline failed: {e}"
            self.logger.error(err_msg, exc_info=True)
            return AgentResult(
                agent_name=self.name,
                success=False,
                error_message=err_msg
            )

    def _is_incremental_unchanged(self, current_count: int) -> bool:
        """
        Checks if the sum of raw rows matches the value logged in last_processed.txt.
        """
        try:
            if self.tracking_file.exists():
                with open(self.tracking_file, "r") as f:
                    logged_count = int(f.read().strip())
                return logged_count == current_count
            return False
        except Exception:
            return False

    def _save_incremental_token(self, count: int) -> None:
        """
        Saves the row count check token to last_processed.txt.
        """
        try:
            with open(self.tracking_file, "w") as f:
                f.write(str(count))
        except Exception as e:
            self.logger.warning(f"Could not save incremental tracking file: {e}")
