"""
Travel Assistant Agent Module
一个基于 SiliconFlow 的智能旅行助手模块
"""

from .client import SiliconFlowClient
from .tools import get_weather, get_attraction, get_hotels
from .agent import TravelAssistantAgent
from .config import DEFAULT_CONFIG

__version__ = "1.0.0"
__author__ = "Your Name"
__email__ = "your.email@example.com"

__all__ = [
    "SiliconFlowClient",
    "TravelAssistantAgent",
    "get_weather",
    "get_attraction",
    "get_hotels",
    "DEFAULT_CONFIG"
]
