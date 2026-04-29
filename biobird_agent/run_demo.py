"""命令行快速测试，不启动网页也能生成一次多 Agent 运行记录。"""
from agents.workflow import BioBirdWorkflow

project = {
    "项目名称": "BioBird-Agent：面向仿生隐蔽飞行机器人的多智能体研发平台",
    "核心痛点": "本科团队在结构设计、飞行控制调参、隐蔽性评估和竞赛材料整理方面效率低，缺少系统化证据链。",
    "硬件基础": "STM32 控制板、舵机扑翼机构、ADC 电压采集、串口调试、仿生羽翼。",
    "当前进度": "已完成项目方案、应用场景构思和部分 PPT 页面，正在完善飞行测试与证明材料。",
}

if __name__ == "__main__":
    workflow = BioBirdWorkflow()
    data = workflow.run(project)
    print("运行完成，总 token 估算：", data["total_usage"]["total_tokens"])
    for item in data["results"]:
        print("\n=", item["name"], "=")
        print(item["raw_text"][:500])
