# BioBird Agent

面向仿生飞鸟机器人项目的多智能体研发与答辩辅助工具。项目提供 Streamlit 界面、六角色串行工作流、轻量级图像相似度评估，以及 Markdown 和 JSON 结果导出。

## 项目定位

BioBird Agent 用于整理仿生飞鸟机器人项目资料，并为结构设计、控制调参、视觉评估、材料撰写和答辩训练提供辅助建议。当前实现适合课程展示、竞赛准备和原型验证。

图像评分采用颜色直方图、平均亮度和边缘密度等轻量指标。该结果只能用于辅助演示，不能替代严格的计算机视觉实验、飞行测试或学术评估。

## 核心功能

| 模块 | 功能 |
| --- | --- |
| 项目资料 | 录入背景、痛点、硬件基础、当前进度和目标成果 |
| 多智能体工作流 | 依次运行项目总控、结构设计、控制优化、视觉评估、文档生成和答辩模拟六个角色 |
| 图像评估 | 比较机器人图片与参考图片的颜色、亮度和边缘特征 |
| 结果留存 | 自动保存 JSON 运行记录，并支持导出 Markdown 报告 |
| 本地演示 | 未配置 API Key 时自动使用内置模拟结果 |
| 模型接入 | 支持 OpenAI 兼容的 Chat Completions 接口 |

## 快速开始

### 1. 准备环境

需要 Python 3.10 或更高版本。

```bash
git clone https://github.com/fffssss11/biobird-agent.git
cd biobird-agent/biobird_agent
python -m venv .venv
```

Windows PowerShell：

```powershell
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

macOS 或 Linux：

```bash
source .venv/bin/activate
python -m pip install -r requirements.txt
```

### 2. 配置模型

```powershell
Copy-Item .env.example .env
```

macOS 或 Linux：

```bash
cp .env.example .env
```

环境变量说明：

| 变量 | 用途 | 默认值 |
| --- | --- | --- |
| `LLM_API_KEY` | OpenAI 兼容接口的访问密钥 | 空 |
| `LLM_BASE_URL` | 接口基础地址 | `https://api.openai.com/v1` |
| `LLM_MODEL` | 模型名称 | `gpt-4o-mini` |
| `MOCK_MODE` | 强制使用本地模拟输出 | `false` |
| `REQUEST_TIMEOUT` | 请求超时秒数 | `60` |
| `TEMPERATURE` | 模型温度 | `0.35` |

未设置 `LLM_API_KEY` 时，程序会自动进入本地模拟模式。请勿提交包含真实密钥的 `.env` 文件。

### 3. 启动应用

```bash
streamlit run app.py
```

命令行快速验证：

```bash
python run_demo.py
```

运行结果会写入 `biobird_agent/runs/`。该目录已加入忽略规则，避免把本地日志和演示数据提交到仓库。

## 仓库结构

```text
biobird-agent/
├── README.md
├── .gitignore
└── biobird_agent/
    ├── app.py
    ├── config.py
    ├── llm_client.py
    ├── run_demo.py
    ├── requirements.txt
    ├── .env.example
    ├── agents/
    │   ├── base.py
    │   ├── biobird_agents.py
    │   └── workflow.py
    └── utils/
        ├── reporting.py
        ├── token_meter.py
        └── visual_eval.py
```

## 使用边界

- 多智能体输出包含模型生成内容，提交竞赛材料前需要逐项核对。
- 图像相似度分数受拍摄角度、光照、背景和图片质量影响。
- 项目当前没有飞行控制硬件接口，也没有经过真实飞行安全验证。
- `runs/` 中可能包含项目资料，分享运行文件前应检查隐私信息。

## 后续改进方向

- 增加自动化测试和持续集成。
- 引入可复现的视觉评估数据集与指标基线。
- 增加工作流并行执行、失败重试和运行历史检索。
- 补充真实硬件测试记录与项目截图。
