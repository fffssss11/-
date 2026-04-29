"""
BioBird-Agent 配置文件

运行方式：
1. 复制 .env.example 为 .env
2. 填入你的大模型 API Key
3. 执行：streamlit run app.py

说明：本项目默认兼容 OpenAI 风格的 /v1/chat/completions 接口，
也可以接入学校/公司/国产大模型平台，只要它支持相同格式。
"""
from __future__ import annotations

import os
from dataclasses import dataclass
from dotenv import load_dotenv

load_dotenv()


@dataclass(frozen=True)
class Settings:
    app_name: str = "BioBird-Agent 仿生飞鸟机器人多智能体研发平台"
    llm_api_key: str = os.getenv("LLM_API_KEY", "")
    llm_base_url: str = os.getenv("LLM_BASE_URL", "https://api.openai.com/v1")
    llm_model: str = os.getenv("LLM_MODEL", "gpt-4o-mini")
    request_timeout: int = int(os.getenv("REQUEST_TIMEOUT", "60"))
    temperature: float = float(os.getenv("TEMPERATURE", "0.35"))
    mock_mode: bool = os.getenv("MOCK_MODE", "auto").lower() in {"1", "true", "yes"}


settings = Settings()
