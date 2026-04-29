# BioBird-Agent：面向仿生隐蔽飞行机器人的多智能体研发平台

这是一个可直接运行的 Streamlit 项目，用于把“仿生飞鸟机器人项目”包装成一个真实可演示的 AI Agent 成果。它可以用于申报表第 04 项“使用 Agent 或 AI 驱动构建的具体成果”和第 05 项“证明与影响力证明”。

## 一、功能

1. **项目资料输入**  
   输入项目名称、背景、核心痛点、硬件基础、当前进度和目标成果。

2. **多 Agent 协同分析**  
   系统包含 6 个 Agent：
   - 项目总控 Agent
   - 结构设计 Agent
   - 控制优化 Agent
   - 视觉评估 Agent
   - 文档生成 Agent
   - 答辩模拟 Agent

3. **隐蔽性图像评估**  
   上传机器人图片和真实鸟类/自然场景图片，系统会输出：
   - 颜色相似度
   - 亮度相似度
   - 轮廓相似度
   - 综合评分
   - 优化建议

4. **证明材料导出**  
   可导出 Markdown 报告和 JSON 运行记录，便于上传申报材料或录屏展示。

## 二、安装方式

进入项目目录：

```bash
cd biobird_agent
```

创建虚拟环境，推荐 Python 3.10 及以上：

```bash
python -m venv .venv
```

Windows 激活：

```bash
.venv\Scripts\activate
```

macOS / Linux 激活：

```bash
source .venv/bin/activate
```

安装依赖：

```bash
pip install -r requirements.txt
```

## 三、配置大模型 API

复制配置文件：

```bash
copy .env.example .env
```

macOS / Linux 使用：

```bash
cp .env.example .env
```

打开 `.env`，填写：

```env
LLM_API_KEY=你的 API Key
LLM_BASE_URL=https://api.openai.com/v1
LLM_MODEL=gpt-4o-mini
MOCK_MODE=false
```

如果没有 API Key，也可以直接运行。系统会自动进入本地模拟模式，适合课堂演示和答辩录屏。

## 四、启动项目

```bash
streamlit run app.py
```

浏览器会自动打开页面。如果没有自动打开，可以访问终端中显示的本地地址。

## 五、建议录屏演示流程

1. 打开“项目资料”页，展示仿生鸟项目基本信息。
2. 点击“启动 BioBird 多 Agent 工作流”。
3. 展示 6 个 Agent 的输出结果和 Token 消耗估算。
4. 上传机器人图片和真实鸟/自然场景图片，展示隐蔽性评分。
5. 导出 Markdown 报告和 JSON 运行记录。
6. 打开“答辩与证明材料”页，复制申报表成果描述。

## 六、可填写到申报表第 04 项的描述

我构建了一个面向仿生飞鸟机器人的多 Agent 辅助研发系统，用于解决本科团队在结构设计、控制调参、仿生隐蔽性评估和竞赛材料整理中的效率低、经验不足、证据链分散等问题。系统包含项目总控 Agent、结构设计 Agent、控制优化 Agent、视觉评估 Agent、文档生成 Agent 和答辩模拟 Agent。各 Agent 会围绕项目资料自动生成结构优化建议、控制测试方案、视觉相似度评估、查新报告写作建议和评委问答训练内容。目前系统已能输出完整研发报告和 JSON 运行记录，并记录每次工作流的 Token 消耗，可作为后续扩大 token plan 使用额度的依据。

## 七、文件结构

```text
biobird_agent/
├── app.py                         # Streamlit 主程序
├── config.py                      # 配置读取
├── llm_client.py                  # 大模型客户端，支持模拟模式
├── requirements.txt               # Python 依赖
├── .env.example                   # 环境变量模板
├── agents/
│   ├── base.py                    # Agent 基类
│   ├── biobird_agents.py          # 6 个 Agent 的角色提示词
│   └── workflow.py                # 多 Agent 工作流
├── utils/
│   ├── token_meter.py             # Token 估算
│   ├── visual_eval.py             # 图像隐蔽性评估
│   └── reporting.py               # 报告导出
└── runs/                          # 自动保存运行记录
```

## 八、注意事项

- 图像相似度评估是轻量级演示算法，用于证明项目有量化评估思路，不应写成严格学术视觉模型。
- 如果申报时需要更强技术含量，可以后续接入 YOLO、CLIP、SAM 或自训练鸟类识别模型。
- 如果只是为了提高评估通过率，建议重点展示：运行截图、工作流截图、Token 统计、导出报告、项目 PPT 迭代前后对比。
