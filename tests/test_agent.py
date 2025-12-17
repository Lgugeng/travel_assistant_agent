"""
测试智能体
"""

import pytest
from unittest.mock import Mock
from travel_assistant.agent import TravelAssistantAgent


class TestTravelAssistantAgent:
    """测试智能体"""
  
    def test_init(self):
        """测试初始化"""
        mock_client = Mock()
        agent = TravelAssistantAgent(mock_client)
        
        assert agent.client == mock_client
        assert len(agent.tools) > 0
        assert len(agent.conversation_history) == 0
  
    def test_add_tool(self):
        """测试添加工具"""
        mock_client = Mock()
        agent = TravelAssistantAgent(mock_client)
        
        # 初始工具数量
        initial_count = len(agent.tools)
        
        # 添加自定义工具
        def custom_tool():
            return "custom result"
        
        agent.add_tool("custom_tool", custom_tool)
        
        # 工具数量应该增加
        assert len(agent.tools) == initial_count + 1
        assert "custom_tool" in agent.tools
  
    def test_parse_llm_output(self):
        """测试解析LLM输出"""
        mock_client = Mock()
        agent = TravelAssistantAgent(mock_client)
        
        # 测试标准格式
        llm_output = """
        Thought: 我需要查询天气
        Action: get_weather(city="北京")
        """
        
        thought, action = agent.parse_llm_output(llm_output)
        assert thought == "我需要查询天气"
        assert action == "get_weather(city=\"北京\")"
  
    def test_clear_history(self):
        """测试清空历史"""
        mock_client = Mock()
        agent = TravelAssistantAgent(mock_client)
        
        # 添加一些历史记录
        agent.conversation_history.append("测试历史")
        assert len(agent.conversation_history) == 1
        
        # 清空历史
        agent.clear_history()
        assert len(agent.conversation_history) == 0


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
