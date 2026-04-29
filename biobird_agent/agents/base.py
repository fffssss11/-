from __future__ import annotations

import json
from dataclasses import dataclass, asdict
from typing import Any, Dict, List

from llm_client import llm_client
from utils.token_meter import estimate_tokens


@dataclass
class AgentResult:
    name: str
    role: str
    output: Dict[str, Any]
    raw_text: str
    usage: Dict[str, int]
    model: str


class BaseAgent:
    name = "Base Agent"
    role = "通用分析"
    system_prompt = "你是一个严谨的项目分析助手，请输出 JSON。"

    def build_user_prompt(self, project: Dict[str, Any], context: Dict[str, Any]) -> str:
        return f"项目资料：\n{json.dumps(project, ensure_ascii=False, indent=2)}\n\n上下文：\n{json.dumps(context, ensure_ascii=False, indent=2)}"

    def run(self, project: Dict[str, Any], context: Dict[str, Any] | None = None) -> AgentResult:
        context = context or {}
        messages = [
            {"role": "system", "content": self.system_prompt},
            {"role": "user", "content": self.build_user_prompt(project, context)},
        ]
        response = llm_client.chat(messages, temperature=0.35)
        raw_text = response["content"]
        try:
            parsed = json.loads(raw_text)
        except json.JSONDecodeError:
            parsed = {"text": raw_text}
        return AgentResult(
            name=self.name,
            role=self.role,
            output=parsed,
            raw_text=raw_text,
            usage=response.get("usage", {
                "prompt_tokens": estimate_tokens(messages[1]["content"]),
                "completion_tokens": estimate_tokens(raw_text),
                "total_tokens": estimate_tokens(messages[1]["content"] + raw_text),
            }),
            model=response.get("model", "unknown"),
        )


def result_to_dict(result: AgentResult) -> Dict[str, Any]:
    return asdict(result)
