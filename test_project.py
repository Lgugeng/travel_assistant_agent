#!/usr/bin/env python3
"""
测试项目基本功能
"""

from travel_assistant import TravelAssistantAgent
from unittest.mock import Mock


def test_basic_functionality():
    """测试项目基本功能"""
    # 创建模拟客户端
    mock_client = Mock()
    
    # 模拟LLM响应
    mock_client.chat.return_value = """
    Thought: 我需要查询北京的天气
    Action: get_weather(city="北京")
    """
    
    # 创建智能体
    agent = TravelAssistantAgent(mock_client)
    
    # 测试智能体初始化
    print("✅ 智能体初始化成功")
    assert agent.client == mock_client
    assert len(agent.tools) > 0
    
    # 测试工具解析
    print("✅ 工具解析成功")
    llm_output = """
    Thought: 我需要查询天气
    Action: get_weather(city="北京")
    """
    thought, action = agent.parse_llm_output(llm_output)
    assert thought == "我需要查询天气"
    assert action == "get_weather(city=\"北京\")"
    
    # 测试执行动作
    print("✅ 执行动作成功")
    result = agent.execute_action("get_weather(city=\"北京\")")
    assert "北京" in result
    
    # 测试添加工具
    print("✅ 添加工具成功")
    def custom_tool():
        return "custom result"
    agent.add_tool("custom_tool", custom_tool)
    assert "custom_tool" in agent.tools
    
    # 测试清空历史
    print("✅ 清空历史成功")
    agent.conversation_history.append("test")
    agent.clear_history()
    assert len(agent.conversation_history) == 0
    
    print("🎉 项目基本功能测试通过！")


if __name__ == "__main__":
    test_basic_functionality()
