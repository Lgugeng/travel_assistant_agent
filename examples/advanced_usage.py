"""
高级使用示例
"""

import os
from travel_assistant import SiliconFlowClient, TravelAssistantAgent, get_weather, get_attraction


def custom_tool(city: str, preference: str = None) -> str:
    """自定义工具示例"""
    return f"根据您的偏好'{preference}'，推荐{city}的特色活动。"


def main():
    """高级使用示例"""
    api_key = os.environ.get("SILICONFLOW_API_KEY")
    if not api_key:
        print("请设置 SILICONFLOW_API_KEY 环境变量")
        return
  
    # 1. 创建带有自定义配置的客户端
    client = SiliconFlowClient(
        api_key=api_key,
        model="qwen2.5-7b",  # 使用别名
        temperature=0.5,  # 降低随机性
        timeout=60  # 延长超时时间
    )
  
    # 2. 查看可用模型
    models = client.get_available_models()
    print(f"可用模型: {models[:5]}...")  # 显示前5个
  
    # 3. 创建智能体并添加自定义工具
    agent = TravelAssistantAgent(client)
    agent.add_tool("custom_tool", custom_tool)
  
    # 4. 自定义系统提示词
    custom_system_prompt = """
    你是一个专业的旅行规划师。请帮助用户规划旅行。
  
    可用工具:
    - get_weather(city): 查询天气
    - get_attraction(city, weather): 推荐景点
    - custom_tool(city, preference): 根据偏好推荐活动
  
    请仔细思考每一步，确保提供有用的建议。
    """
    agent.system_prompt = custom_system_prompt
  
    # 5. 运行复杂查询
    complex_query = """
    我想去北京旅游3天，主要想参观历史文化景点，
    预算是中等，帮我规划一下行程，包括天气、景点和住宿建议。
    """
  
    print(f"\n处理复杂查询: {complex_query}")
    result = agent.run(complex_query, max_iterations=8, verbose=True)
  
    print(f"\n最终规划:\n{result}")
  
    # 6. 获取对话历史
    history = agent.get_conversation_history()
    print(f"\n对话历史记录数: {len(history)}")


if __name__ == "__main__":
    main()
