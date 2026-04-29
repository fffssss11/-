from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List

from agents.base import AgentResult, result_to_dict
from agents.biobird_agents import (
    ControlOptimizationAgent,
    DefenseCoachAgent,
    DocumentAgent,
    ProjectManagerAgent,
    StructureDesignAgent,
    VisualMimicryAgent,
)


class BioBirdWorkflow:
    """多 Agent 串行协作工作流。"""

    def __init__(self) -> None:
        self.agents = [
            ProjectManagerAgent(),
            StructureDesignAgent(),
            ControlOptimizationAgent(),
            VisualMimicryAgent(),
            DocumentAgent(),
            DefenseCoachAgent(),
        ]

    def run(self, project: Dict[str, Any]) -> Dict[str, Any]:
        context: Dict[str, Any] = {"previous_results": []}
        results: List[AgentResult] = []
        for agent in self.agents:
            result = agent.run(project, context)
            results.append(result)
            context["previous_results"].append({
                "agent": result.name,
                "role": result.role,
                "output": result.output,
            })

        total_usage = {
            "prompt_tokens": sum(int(r.usage.get("prompt_tokens", 0)) for r in results),
            "completion_tokens": sum(int(r.usage.get("completion_tokens", 0)) for r in results),
            "total_tokens": sum(int(r.usage.get("total_tokens", 0)) for r in results),
        }
        run_data = {
            "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "project": project,
            "results": [result_to_dict(r) for r in results],
            "total_usage": total_usage,
        }
        self._save_run(run_data)
        return run_data

    def _save_run(self, run_data: Dict[str, Any]) -> None:
        Path("runs").mkdir(exist_ok=True)
        filename = f"runs/biobird_run_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(run_data, f, ensure_ascii=False, indent=2)
