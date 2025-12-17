"""
基础使用示例
"""

import os
from dotenv import load_dotenv
from travel_assistant import SiliconFlowClient, TravelAssistantAgent

# 加载.env文件
load_dotenv()


def main():
    """基础使用示例"""
    # 从环境变量获取API密钥
    api_key = os.environ.get("SILICONFLOW_API_KEY")
    if not api_key:
        print("请设置 SILICONFLOW_API_KEY 环境变量")
        return
  
    # 1. 创建客户端
    client = SiliconFlowClient(
        api_key=api_key,
        model="deepseek-ai/DeepSeek-V2.5"
    )
  
    # 2. 创建智能体
    agent = TravelAssistantAgent(client)
  
    # 3. 运行查询
    queries = [
        "查询北京天气并推荐景点",
        "上海下雨了，有什么室内景点推荐？",
        "帮我规划一下广州的旅行",
    ]
  
    for query in queries:
        print(f"\n{'='*60}")
        print(f"查询: {query}")
        print(f"{'='*60}")
      
        result = agent.run(query, verbose=True)
        print(f"\n结果: {result}")
      
        # 清空对话历史
        agent.clear_history()


if __name__ == "__main__":
    main()
