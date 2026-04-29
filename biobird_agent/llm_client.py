from __future__ import annotations

import json
import time
from typing import Any, Dict, List, Optional

import requests

from config import settings
from utils.token_meter import estimate_tokens


class LLMError(RuntimeError):
    pass


class LLMClient:
    """OpenAI-compatible Chat Completions 客户端。

    如果未配置 API Key 或 MOCK_MODE=true，则自动返回本地模拟结果，
    方便课堂演示、答辩录屏和无网环境调试。
    """

    def __init__(self) -> None:
        self.api_key = settings.llm_api_key
        self.base_url = settings.llm_base_url.rstrip("/")
        self.model = settings.llm_model
        self.timeout = settings.request_timeout
        self.temperature = settings.temperature
        self.force_mock = settings.mock_mode

    @property
    def use_mock(self) -> bool:
        return self.force_mock or not self.api_key

    def chat(
        self,
        messages: List[Dict[str, str]],
        *,
        temperature: Optional[float] = None,
        response_format: Optional[Dict[str, str]] = None,
    ) -> Dict[str, Any]:
        prompt_text = "\n".join(m.get("content", "") for m in messages)
        prompt_tokens = estimate_tokens(prompt_text)

        if self.use_mock:
            content = self._mock_response(messages)
            return {
                "content": content,
                "usage": {
                    "prompt_tokens": prompt_tokens,
                    "completion_tokens": estimate_tokens(content),
                    "total_tokens": prompt_tokens + estimate_tokens(content),
                },
                "model": "mock-local-agent",
            }

        url = f"{self.base_url}/chat/completions"
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }
        payload: Dict[str, Any] = {
            "model": self.model,
            "messages": messages,
            "temperature": self.temperature if temperature is None else temperature,
        }
        if response_format:
            payload["response_format"] = response_format

        try:
            resp = requests.post(url, headers=headers, json=payload, timeout=self.timeout)
            resp.raise_for_status()
        except requests.RequestException as exc:
            raise LLMError(f"大模型请求失败：{exc}") from exc

        data = resp.json()
        try:
            content = data["choices"][0]["message"]["content"]
        except (KeyError, IndexError, TypeError) as exc:
            raise LLMError(f"大模型返回格式异常：{data}") from exc

        usage = data.get("usage") or {
            "prompt_tokens": prompt_tokens,
            "completion_tokens": estimate_tokens(content),
            "total_tokens": prompt_tokens + estimate_tokens(content),
        }
        return {"content": content, "usage": usage, "model": data.get("model", self.model)}

    def _mock_response(self, messages: List[Dict[str, str]]) -> str:
        """根据 system prompt 的关键词生成稳定的演示结果。"""
        system_text = "\n".join(
            m.get("content", "") for m in messages if m.get("role") == "system"
        )
        time.sleep(0.2)
        if "结构设计 Agent" in system_text:
            return json.dumps({
                "agent": "结构设计 Agent",
                "core_findings": [
                    "当前项目关键风险是重心位置、扑翼连杆强度和舵机输出余量之间的匹配。",
                    "建议将电池靠近机身重心布置，并给机翼根部预留可调孔位，方便实测后微调翼面攻角。"
                ],
                "actions": [
                    "建立机身重心—翼展—舵机扭矩对照表",
                    "对扑翼连杆、机翼根部和尾翼连接件做薄弱点检查",
                    "将关键承力件由单点螺丝固定改为双点定位或加筋结构"
                ],
                "risks": ["机翼根部疲劳开裂", "电池位置改变导致俯仰不稳定", "舵机过载发热"],
                "evidence": "可输出结构优化记录表、迭代前后 CAD/实物照片和测试视频作为证明。"
            }, ensure_ascii=False, indent=2)
        if "控制优化 Agent" in system_text:
            return json.dumps({
                "agent": "控制优化 Agent",
                "core_findings": [
                    "控制链路应先保证手动可控，再逐步加入姿态稳定和半自主飞行逻辑。",
                    "建议记录 PWM、舵机角度、飞行姿态和电池电压，形成可回放的调参日志。"
                ],
                "actions": [
                    "设计低、中、高三档扑翼频率测试方案",
                    "建立舵机中位校准程序，避免左右翼输出不一致",
                    "增加低电压保护和失控降频策略"
                ],
                "risks": ["左右翼相位不一致", "电压下降导致舵机力矩不足", "过快调参造成结构损坏"],
                "evidence": "可上传串口日志、调参表、飞行测试视频和控制程序仓库。"
            }, ensure_ascii=False, indent=2)
        if "视觉评估 Agent" in system_text:
            return json.dumps({
                "agent": "视觉评估 Agent",
                "core_findings": [
                    "隐蔽性展示应从外形轮廓、颜色纹理、运动姿态和场景融合四个维度说明。",
                    "答辩中可以用真假鸟对比图/动图向评委提问，增强项目记忆点。"
                ],
                "actions": [
                    "采集真实鸟类、机器人和自然背景图像进行并排对比",
                    "统一图片拍摄角度，避免因光线差异影响判断",
                    "在 PPT 中加入评委互动问题：哪一个是假鸟？"
                ],
                "risks": ["外观仿生停留在静态展示", "背景过于单一", "缺少量化评价指标"],
                "evidence": "可输出图像相似度评分、真假鸟对比页和现场演示视频。"
            }, ensure_ascii=False, indent=2)
        if "文档生成 Agent" in system_text:
            return json.dumps({
                "agent": "文档生成 Agent",
                "core_findings": [
                    "材料应突出项目背景、技术路线、创新点、应用场景和阶段成果，而不是只描述外观。",
                    "查新报告中应把仿生隐蔽、扑翼结构、低空巡检和多场景应用分别展开。"
                ],
                "actions": [
                    "生成 400 字以内项目简介",
                    "生成查新报告各栏目草稿",
                    "生成答辩 PPT 页面文案和讲稿",
                    "建立每次 AI 输出的版本记录"
                ],
                "risks": ["文字同质化", "创新点表述过泛", "缺少实际落地证据"],
                "evidence": "可保留 AI 对话截图、文档版本对比和最终报告页面。"
            }, ensure_ascii=False, indent=2)
        if "答辩模拟 Agent" in system_text:
            return json.dumps({
                "agent": "答辩模拟 Agent",
                "questions": [
                    "你们的仿生鸟与普通无人机相比，核心优势是什么？",
                    "项目的隐蔽性如何证明，不只是主观觉得像鸟？",
                    "飞行稳定性目前达到什么水平，失败样例如何处理？",
                    "本科生团队各成员分别完成了哪些工作？",
                    "后续如何从原型机走向可应用系统？"
                ],
                "answer_strategy": [
                    "先讲痛点，再讲方案，最后讲已有证据。",
                    "用测试视频、对比图片和结构迭代记录支撑回答。",
                    "承认当前限制，同时给出下一阶段改进路线。"
                ],
                "evidence": "可录制一段 AI 随机提问与团队回答的训练视频。"
            }, ensure_ascii=False, indent=2)
        return json.dumps({
            "agent": "项目总控 Agent",
            "summary": "系统已完成仿生飞鸟机器人项目的任务拆解，建议按结构、控制、视觉、材料和答辩五条线并行推进。",
            "milestones": ["完成项目资料输入", "完成多 Agent 研发建议", "完成隐蔽性评估", "形成证明材料包"],
            "next_step": "先补充实物图片、飞行测试记录和当前 PPT 页面，再生成最终申报表内容。"
        }, ensure_ascii=False, indent=2)


llm_client = LLMClient()
