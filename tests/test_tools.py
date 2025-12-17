"""
测试工具函数
"""

import pytest
from unittest.mock import Mock, patch
from travel_assistant.tools import get_weather, get_attraction


class TestTools:
    """测试工具函数"""
  
    @patch('requests.get')
    def test_get_weather_success(self, mock_get):
        """测试成功获取天气"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "current_condition": [{
                "weatherDesc": [{"value": "晴天"}],
                "temp_C": "25",
                "humidity": "60",
                "windspeedKmph": "10"
            }]
        }
        mock_get.return_value = mock_response
      
        result = get_weather("北京")
        assert "北京" in result
        assert "晴天" in result
        assert "25" in result
  
    @patch('requests.get')
    def test_get_weather_failure(self, mock_get):
        """测试获取天气失败"""
        mock_get.side_effect = Exception("网络错误")
      
        result = get_weather("北京")
        assert "失败" in result or "错误" in result
  
    def test_get_attraction(self):
        """测试获取景点推荐"""
        result = get_attraction("北京", "晴天")
        assert "北京" in result
        assert "晴天" in result or "景点" in result
  
    def test_get_attraction_unknown_city(self):
        """测试未知城市的景点推荐"""
        result = get_attraction("未知城市", "晴天")
        assert "未知城市" in result or "景点" in result


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
