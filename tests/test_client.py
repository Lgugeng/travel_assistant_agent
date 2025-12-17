"""
测试客户端
"""

import pytest
from unittest.mock import Mock, patch
from travel_assistant.client import SiliconFlowClient


class TestSiliconFlowClient:
    """测试 SiliconFlowClient"""
  
    def test_init(self):
        """测试初始化"""
        client = SiliconFlowClient(api_key="test-key", model="test-model")
        assert client.api_key == "test-key"
        assert client.model == "test-model"
        assert client.base_url == "https://api.siliconflow.cn/v1"
  
    def test_init_with_alias(self):
        """测试使用模型别名"""
        client = SiliconFlowClient(api_key="test-key", model="qwen2.5-7b")
        # 应该将别名转换为完整模型名
        assert "Qwen" in client.model
  
    def test_missing_api_key(self):
        """测试缺少API密钥"""
        with pytest.raises(ValueError):
            SiliconFlowClient(api_key="")
  
    @patch('requests.post')
    def test_chat(self, mock_post):
        """测试聊天功能"""
        # 模拟响应
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "choices": [{"message": {"content": "测试回复"}}]
        }
        mock_post.return_value = mock_response
      
        client = SiliconFlowClient(api_key="test-key")
        result = client.chat([{"role": "user", "content": "你好"}])
      
        assert result == "测试回复"
        mock_post.assert_called_once()


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
