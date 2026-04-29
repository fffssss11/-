from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict

import pandas as pd
import streamlit as st
from PIL import Image

from agents.workflow import BioBirdWorkflow
from config import settings
from utils.reporting import export_markdown, save_json
from utils.visual_eval import compare_images


st.set_page_config(
    page_title="BioBird-Agent",
    page_icon="🕊️",
    layout="wide",
)


DEFAULT_PROJECT = {
    "项目名称": "BioBird-Agent：面向仿生隐蔽飞行机器人的多智能体研发平台",
    "项目背景": "传统小型无人机噪声大、外形机械感明显，在生态观察、低空巡检、科普教学等场景中容易引起目标警觉。项目希望通过仿生鸟外形和扑翼飞行方式提升自然场景融合度。",
    "核心痛点": "本科团队在结构设计、控制调参、隐蔽性评估和竞赛材料整理方面经验不足，研发过程容易碎片化，缺少系统化证据链。",
    "硬件基础": "STM32 控制板、舵机扑翼机构、尾翼控制、ADC 电压采集、串口调试、轻量化机身与仿生羽翼。",
    "当前进度": "已完成项目方案、应用场景、PPT 页面构思和部分外观/结构设计，正在完善飞行测试与证明材料。",
    "目标成果": "形成一个可演示的多 Agent 研发辅助系统，输出结构优化、控制调参、视觉隐蔽性评估、文档生成和答辩模拟结果。",
}


def init_state() -> None:
    if "project" not in st.session_state:
        st.session_state.project = DEFAULT_PROJECT.copy()
    if "run_data" not in st.session_state:
        st.session_state.run_data = None
    if "visual_result" not in st.session_state:
        st.session_state.visual_result = None


def display_json_card(title: str, data: Dict[str, Any]) -> None:
    with st.expander(title, expanded=True):
        if isinstance(data, dict):
            for key, value in data.items():
                if isinstance(value, list):
                    st.markdown(f"**{key}**")
                    for item in value:
                        st.markdown(f"- {item}")
                elif isinstance(value, dict):
                    st.markdown(f"**{key}**")
                    st.json(value, expanded=False)
                else:
                    st.markdown(f"**{key}**：{value}")
        else:
            st.write(data)


def project_input_tab() -> None:
    st.subheader("一、项目资料输入")
    st.caption("这些信息会被传给多个 Agent。写得越具体，输出越接近你的真实项目。")

    cols = st.columns(2)
    keys = list(DEFAULT_PROJECT.keys())
    new_project: Dict[str, str] = {}
    for i, key in enumerate(keys):
        with cols[i % 2]:
            new_project[key] = st.text_area(key, value=st.session_state.project.get(key, ""), height=130)

    custom_key = st.text_input("可选：新增字段名，例如：团队分工 / 预算 / 测试条件")
    custom_value = st.text_area("可选：新增字段内容", height=100)

    if st.button("保存项目资料", type="primary"):
        if custom_key.strip() and custom_value.strip():
            new_project[custom_key.strip()] = custom_value.strip()
        st.session_state.project = new_project
        st.success("项目资料已保存。")

    st.markdown("#### 当前资料预览")
    st.json(st.session_state.project, expanded=False)


def workflow_tab() -> None:
    st.subheader("二、多 Agent 协同分析")
    st.caption("点击运行后，系统会依次调用项目总控、结构设计、控制优化、视觉评估、文档生成和答辩模拟 Agent。")

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("运行模式", "模拟模式" if settings.mock_mode or not settings.llm_api_key else "真实大模型")
    with col2:
        st.metric("模型", settings.llm_model if settings.llm_api_key else "mock-local-agent")
    with col3:
        st.metric("Agent 数量", 6)

    if st.button("启动 BioBird 多 Agent 工作流", type="primary"):
        with st.spinner("多 Agent 正在分析项目，请稍等..."):
            workflow = BioBirdWorkflow()
            st.session_state.run_data = workflow.run(st.session_state.project)
        st.success("工作流运行完成，结果已保存到 runs 文件夹。")

    run_data = st.session_state.run_data
    if not run_data:
        st.info("请先启动工作流。")
        return

    usage = run_data.get("total_usage", {})
    st.markdown("#### Token 消耗估算")
    c1, c2, c3 = st.columns(3)
    c1.metric("Prompt Tokens", usage.get("prompt_tokens", 0))
    c2.metric("Completion Tokens", usage.get("completion_tokens", 0))
    c3.metric("Total Tokens", usage.get("total_tokens", 0))

    st.markdown("#### Agent 输出结果")
    for item in run_data.get("results", []):
        display_json_card(f"{item.get('name')}｜{item.get('role')}", item.get("output", {}))

    st.markdown("#### 导出证明材料")
    col_a, col_b = st.columns(2)
    with col_a:
        if st.button("导出 Markdown 研发报告"):
            path = export_markdown(run_data)
            st.success(f"已导出：{path}")
            st.download_button(
                "下载 Markdown 报告",
                data=Path(path).read_text(encoding="utf-8"),
                file_name="BioBird-Agent-研发报告.md",
                mime="text/markdown",
            )
    with col_b:
        if st.button("导出 JSON 运行记录"):
            path = save_json(run_data, "runs/biobird_agent_run.json")
            st.success(f"已导出：{path}")
            st.download_button(
                "下载 JSON 运行记录",
                data=Path(path).read_text(encoding="utf-8"),
                file_name="BioBird-Agent-运行记录.json",
                mime="application/json",
            )


def visual_tab() -> None:
    st.subheader("三、仿生隐蔽性图像评估")
    st.caption("上传机器人图片和真实鸟类/自然背景图片，系统会计算颜色、亮度和轮廓相似度。")

    col1, col2 = st.columns(2)
    with col1:
        robot_file = st.file_uploader("上传仿生鸟机器人图片", type=["jpg", "jpeg", "png"], key="robot")
    with col2:
        ref_file = st.file_uploader("上传真实鸟类或应用场景参考图", type=["jpg", "jpeg", "png"], key="ref")

    if robot_file and ref_file:
        robot_img = Image.open(robot_file)
        ref_img = Image.open(ref_file)
        c1, c2 = st.columns(2)
        c1.image(robot_img, caption="机器人图片", use_container_width=True)
        c2.image(ref_img, caption="参考图片", use_container_width=True)

        if st.button("开始视觉相似度评估", type="primary"):
            result = compare_images(robot_img, ref_img)
            st.session_state.visual_result = result

    if st.session_state.visual_result:
        result = st.session_state.visual_result
        st.markdown("#### 评估结果")
        m1, m2, m3, m4 = st.columns(4)
        m1.metric("颜色相似度", result["color_similarity"])
        m2.metric("亮度相似度", result["brightness_similarity"])
        m3.metric("轮廓相似度", result["edge_similarity"])
        m4.metric("综合分", result["final_score"])
        st.info(result["interpretation"])
        st.markdown("#### 优化建议")
        for suggestion in result["suggestions"]:
            st.markdown(f"- {suggestion}")

        chart_data = pd.DataFrame({
            "指标": ["颜色", "亮度", "轮廓"],
            "相似度": [
                result["color_similarity"],
                result["brightness_similarity"],
                result["edge_similarity"],
            ],
        })
        st.bar_chart(chart_data, x="指标", y="相似度")


def defense_tab() -> None:
    st.subheader("四、答辩展示与证明材料建议")
    st.markdown("""
你可以把这个系统作为申报表第 04、05 项的证明：

- 第 04 项写：你构建了一个多 Agent 辅助研发系统，解决结构设计、控制调参、隐蔽性评估、文档整理和答辩训练效率低的问题。
- 第 05 项上传：系统运行截图、Token 消耗截图、图像评估截图、导出的报告、飞行测试视频或代码仓库链接。
""")

    if st.session_state.run_data:
        st.markdown("#### 可直接用于申报表的成果描述草稿")
        usage = st.session_state.run_data.get("total_usage", {})
        text = f"""我构建了一个面向仿生飞鸟机器人的多 Agent 辅助研发系统，用于解决本科团队在结构设计、控制调参、仿生隐蔽性评估和竞赛材料整理中的效率低、经验不足、证据链分散等问题。系统包含项目总控 Agent、结构设计 Agent、控制优化 Agent、视觉评估 Agent、文档生成 Agent 和答辩模拟 Agent。各 Agent 会围绕项目资料自动生成结构优化建议、控制测试方案、视觉相似度评估、查新报告写作建议和评委问答训练内容。目前系统已能输出完整研发报告和 JSON 运行记录，并记录每次工作流的 Token 消耗。本次演示估算消耗 {usage.get('total_tokens', 0)} tokens，可作为后续扩大 token plan 使用额度的依据。"""
        st.text_area("成果描述", value=text, height=220)
    else:
        st.info("运行一次工作流后，这里会自动生成可复制到申报表的成果描述。")


def main() -> None:
    init_state()
    st.title("🕊️ BioBird-Agent")
    st.caption("面向仿生隐蔽飞行机器人的多智能体研发、评估与答辩辅助平台")

    tabs = st.tabs([
        "项目资料",
        "多 Agent 工作流",
        "图像隐蔽性评估",
        "答辩与证明材料",
    ])
    with tabs[0]:
        project_input_tab()
    with tabs[1]:
        workflow_tab()
    with tabs[2]:
        visual_tab()
    with tabs[3]:
        defense_tab()


if __name__ == "__main__":
    main()
