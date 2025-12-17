"""
流式输出示例
"""

import os
from travel_assistant import SiliconFlowClient, TravelAssistantAgent


def main():
    """流式输出示例"""
    api_key = os.environ.get("SILICONFLOW_API_KEY")
    if not api_key:
        print("请设置 SILICONFLOW_API_KEY 环境变量")
        return
  
    # 创建客户端
    client = SiliconFlowClient(api_key=api_key)
  
    # 创建智能体（启用流式输出）
    agent = TravelAssistantAgent(client)
  
    # 运行流式查询
    print("开始流式处理...")
    result = agent.run(
        "查询杭州天气并推荐西湖周边的景点",
        stream=True,  # 启用流式
        verbose=True
    )
  
    print(f"\n最终结果: {result}")


if __name__ == "__main__":
    main()
