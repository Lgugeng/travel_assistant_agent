"""
SiliconFlow 客户端模块
"""

import requests
from typing import Dict, Any, Iterator
from .config import DEFAULT_CONFIG, SUPPORTED_MODELS


class SiliconFlowClient:
    """
    SiliconFlow API 客户端
    支持流式和非流式输出
    """

    def __init__(self, api_key: str,
                 model: str = None,
                 base_url: str = None,
                 temperature: float = None,
                 timeout: int = None):
        """
        初始化客户端

        Args:
            api_key: SiliconFlow API密钥
            model: 模型名称或别名
            base_url: API基础URL
            temperature: 温度参数
            timeout: 请求超时时间
        """
        self.api_key = api_key
        self.model = model or DEFAULT_CONFIG["default_model"]

        # 如果传入的是别名，转换为完整模型名
        if self.model in SUPPORTED_MODELS:
            self.model = SUPPORTED_MODELS[self.model]

        self.base_url = base_url or DEFAULT_CONFIG["api_base_url"]
        self.temperature = temperature or DEFAULT_CONFIG["default_temperature"]
        self.timeout = timeout or DEFAULT_CONFIG["timeout"]

        # 设置请求头
        self.headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }

        # 验证配置
        self._validate_config()

    def _validate_config(self):
        """验证配置"""
        if not self.api_key:
            raise ValueError("API密钥不能为空")

        if not self.model:
            raise ValueError("模型名称不能为空")

    def chat(self, messages: list,
             stream: bool = False,
             temperature: float = None,
             max_tokens: int = 1000) -> Any:
        """
        发送聊天请求
      
        Args:
            messages: 消息列表
            stream: 是否使用流式输出
            temperature: 温度参数
            max_tokens: 最大token数
          
        Returns:
            流式模式下返回生成器，非流式模式下返回字符串
        """
        temp = temperature or self.temperature
      
        payload = {
            "model": self.model,
            "messages": messages,
            "temperature": temp,
            "max_tokens": max_tokens,
            "stream": stream
        }
      
        try:
            response = requests.post(
                f"{self.base_url}/chat/completions",
                headers=self.headers,
                json=payload,
                timeout=self.timeout,
                stream=stream
            )
          
            response.raise_for_status()
          
            if stream:
                return self._handle_stream_response(response)
            else:
                return self._handle_normal_response(response)
                
        except requests.exceptions.Timeout:
            raise TimeoutError(f"请求超时 ({self.timeout}秒)")
        except requests.exceptions.RequestException as e:
            raise ConnectionError(f"网络请求失败: {str(e)}")
  
    def _handle_normal_response(self, response: requests.Response) -> str:
        """处理非流式响应"""
        data = response.json()
        if "choices" not in data or not data["choices"]:
            raise ValueError("API响应格式错误")
      
        return data["choices"][0]["message"]["content"]
  
    def _handle_stream_response(self, response: requests.Response) -> Iterator[str]:
        """处理流式响应"""
        for line in response.iter_lines():
            if line:
                line = line.decode('utf-8')
              
                # 跳过SSE格式的注释行
                if line.startswith('data: '):
                    data = line[6:]  # 移除 "data: " 前缀
                  
                    if data == '[DONE]':
                        break
                  
                    try:
                        chunk = requests.json.loads(data)
                        if (chunk.get('choices') and
                                chunk['choices'][0].get('delta') and
                                chunk['choices'][0]['delta'].get('content')):
                            yield chunk['choices'][0]['delta']['content']
                    except Exception:
                        continue
  
    def get_available_models(self) -> list:
        """
        获取可用的模型列表（需要API支持）
      
        Returns:
            模型名称列表
        """
        try:
            response = requests.get(
                f"{self.base_url}/models",
                headers=self.headers,
                timeout=self.timeout
            )

            if response.status_code == 200:
                data = response.json()
                if isinstance(data, dict) and 'data' in data:
                    return [model['id'] for model in data['data']]
                elif isinstance(data, list):
                    return data
            return []

        except Exception:
            # 如果API不支持，返回预设模型列表
            return list(SUPPORTED_MODELS.values())
  
    def get_usage(self) -> Dict[str, Any]:
        """
        获取API使用情况（需要API支持）
      
        Returns:
            使用情况字典
        """
        try:
            response = requests.get(
                f"{self.base_url}/usage",
                headers=self.headers,
                timeout=self.timeout
            )

            if response.status_code == 200:
                return response.json()
            return {}

        except Exception:
            return {}


# 兼容性别名
OpenAIClient = SiliconFlowClient
