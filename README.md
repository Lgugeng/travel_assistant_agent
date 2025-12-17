# Travel Assistant Agent

基于 SiliconFlow API 的智能旅行助手智能体模块。

## 安装

```bash
# 从源码安装
pip install -e .

# 或者直接使用
pip install git+https://github.com/yourusername/travel-assistant-agent.git
```

## 快速开始

```python
from travel_assistant import SiliconFlowClient, TravelAssistantAgent

# 创建客户端
client = SiliconFlowClient(
    api_key="your-api-key",
    model="deepseek-ai/DeepSeek-V2.5"
)

# 创建智能体
agent = TravelAssistantAgent(client)

# 运行查询
result = agent.run("查询北京天气并推荐景点")
print(result)
```

## 示例

更多示例请查看 `examples/` 目录。

## 许可证

MIT

