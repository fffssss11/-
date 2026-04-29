from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict


def export_markdown(run_data: Dict[str, Any], output_path: str = "runs/biobird_agent_report.md") -> str:
    Path("runs").mkdir(exist_ok=True)
    lines: list[str] = []
    lines.append("# BioBird-Agent 多智能体研发报告")
    lines.append("")
    lines.append(f"生成时间：{run_data.get('created_at', '')}")
    lines.append("")

    project = run_data.get("project", {})
    lines.append("## 一、项目资料")
    for k, v in project.items():
        lines.append(f"- **{k}**：{v}")
    lines.append("")

    lines.append("## 二、Token 消耗估算")
    usage = run_data.get("total_usage", {})
    lines.append(f"- Prompt tokens：{usage.get('prompt_tokens', 0)}")
    lines.append(f"- Completion tokens：{usage.get('completion_tokens', 0)}")
    lines.append(f"- Total tokens：{usage.get('total_tokens', 0)}")
    lines.append("")

    lines.append("## 三、多 Agent 输出")
    for item in run_data.get("results", []):
        lines.append(f"### {item.get('name', '')}：{item.get('role', '')}")
        output = item.get("output", {})
        if isinstance(output, dict):
            for key, value in output.items():
                if isinstance(value, list):
                    lines.append(f"**{key}：**")
                    for x in value:
                        lines.append(f"- {x}")
                else:
                    lines.append(f"**{key}：** {value}")
        else:
            lines.append(str(output))
        lines.append("")

    lines.append("## 四、可上传证明材料建议")
    lines.extend([
        "1. 多 Agent 工作流运行截图，包含六个 Agent 的输出结果。",
        "2. 系统生成的 JSON/Markdown 研发报告。",
        "3. 隐蔽性图像评估截图，展示颜色、亮度、轮廓评分。",
        "4. 项目 PPT 迭代前后对比图。",
        "5. 飞行测试视频、串口调参日志或 GitHub 仓库链接。",
    ])

    path = Path(output_path)
    path.write_text("\n".join(lines), encoding="utf-8")
    return str(path)


def save_json(data: Dict[str, Any], output_path: str) -> str:
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    Path(output_path).write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    return output_path
