"""
工具函数模块
"""

import requests
from .config import CITY_MAPPING


def get_weather(city: str, use_english: bool = True) -> str:
    """
    查询城市天气
  
    Args:
        city: 城市名称（中文或英文）
        use_english: 是否使用英文查询（兼容性更好）
      
    Returns:
        格式化的天气信息
    """
    # 城市名称映射
    query_city = city
    if use_english and city in CITY_MAPPING:
        query_city = CITY_MAPPING[city]
  
    url = f"https://wttr.in/{query_city}?format=j1"
  
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
      
        # 提取天气信息
        current = data['current_condition'][0]
        weather_desc = current['weatherDesc'][0]['value']
        temp_c = current['temp_C']
        humidity = current.get('humidity', 'N/A')
        wind_speed = current.get('windspeedKmph', 'N/A')
        feels_like = current.get('FeelsLikeC', temp_c)
      
        # 构建结果
        result_lines = [
            f"📍 {city} 当前天气",
            f"  天气状况: {weather_desc}",
            f"  温度: {temp_c}°C (体感: {feels_like}°C)",
            f"  湿度: {humidity}%",
            f"  风速: {wind_speed} km/h"
        ]
      
        # 添加预报信息（如果有）
        if 'weather' in data:
            today_forecast = data['weather'][0]
            if 'maxtempC' in today_forecast and 'mintempC' in today_forecast:
                result_lines.append(
                    f"  最高/最低温度: {today_forecast['maxtempC']}°C / {today_forecast['mintempC']}°C"
                )
      
        return "\n".join(result_lines)
      
    except requests.exceptions.Timeout:
        return f"⏰ 查询{city}天气超时，请稍后重试"
    except Exception as e:
        return f"❌ 查询天气失败: {str(e)}"


def get_attraction(city: str, weather: str = None) -> str:
    """
    根据城市和天气推荐景点
  
    Args:
        city: 城市名称
        weather: 天气描述（可选）
      
    Returns:
        景点推荐信息
    """
    # 景点数据库
    attractions_db = {
        "北京": {
            "晴天": "北京晴天推荐景点:\n1. 故宫 - 晴天下的红墙黄瓦格外壮观\n2. 颐和园 - 游湖赏景最佳时机\n3. 八达岭长城 - 登高望远，视野开阔\n4. 天坛公园 - 古建筑在阳光下更显宏伟\n5. 奥林匹克公园 - 适合户外运动",
            "雨天": "北京雨天推荐景点:\n1. 国家博物馆 - 丰富的文物收藏\n2. 首都博物馆 - 了解北京历史文化\n3. 中国科学技术馆 - 有趣的科学体验\n4. 798艺术区 - 室内画廊和咖啡馆\n5. 王府井百货 - 购物美食一站式",
            "阴天": "北京阴天推荐景点:\n1. 颐和园 - 阴天游园别有一番风味\n2. 圆明园 - 历史文化遗址\n3. 什刹海 - 漫步湖边很舒适\n4. 南锣鼓巷 - 逛胡同小店\n5. 雍和宫 - 参观佛教寺庙",
            "雪天": "北京雪天推荐景点:\n1. 故宫 - 雪中紫禁城宛如仙境\n2. 颐和园 - 雪景中的皇家园林\n3. 景山公园 - 俯瞰雪中故宫全景\n4. 北海公园 - 雪中划船别有情趣",
            "雾天": "北京雾天建议室内景点:\n1. 国家大剧院 - 欣赏演出\n2. 北京天文馆 - 探索宇宙\n3. 老舍茶馆 - 体验传统文化"
        },
        # ... 其他城市的数据库
    }
  
    # 确定天气类型
    weather_type = "一般"
    if weather:
        weather_lower = weather.lower()
        if any(k in weather_lower for k in ["晴", "sunny"]):
            weather_type = "晴天"
        elif any(k in weather_lower for k in ["雨", "rain"]):
            weather_type = "雨天"
        elif any(k in weather_lower for k in ["阴", "cloud"]):
            weather_type = "阴天"
        elif any(k in weather_lower for k in ["雪", "snow"]):
            weather_type = "雪天"
        elif any(k in weather_lower for k in ["雾", "fog"]):
            weather_type = "雾天"
  
    # 获取推荐
    if city in attractions_db:
        if weather_type in attractions_db[city]:
            return (f"根据{weather_type}天气，为您推荐{city}的景点:\n\n"
                f"{attractions_db[city][weather_type]}")
        else:
            first_type = next(iter(attractions_db[city]))
            return f"为您推荐{city}的景点:\n\n{attractions_db[city][first_type]}"
    else:
        # 通用推荐
        if weather_type == "雨天":
            return f"由于{city}是{weather_type}，建议游览室内景点：博物馆、美术馆、科技馆、购物中心等。"
        elif weather_type == "晴天":
            return f"{city}是{weather_type}，适合户外活动：公园、湖边、山区、历史古迹等。"
        else:
            return f"推荐{city}的知名景点：市中心、文化街区、美食街等。"


def get_hotels(city: str, budget: str = "中等") -> str:
    """
    查询酒店推荐
  
    Args:
        city: 城市名称
        budget: 预算范围（经济/中等/豪华）
      
    Returns:
        酒店推荐信息
    """
    # 简化的酒店数据库
    hotels_db = {
        "北京": {
            "经济": "经济型酒店:\n1. 如家酒店（王府井店）\n2. 7天连锁酒店\n3. 汉庭酒店\n4. 格林豪泰酒店",
            "中等": "中等价位酒店:\n1. 全季酒店\n2. 亚朵酒店\n3. 桔子水晶酒店\n4. 和颐酒店",
            "豪华": "豪华酒店:\n1. 北京王府半岛酒店\n2. 北京华尔道夫酒店\n3. 北京瑰丽酒店\n4. 北京柏悦酒店"
        },
        "上海": {
            "经济": "经济型酒店:\n1. 如家酒店（南京路店）\n2. 锦江之星\n3. 布丁酒店\n4. 速8酒店",
            "中等": "中等价位酒店:\n1. 全季酒店\n2. 亚朵酒店\n3. 桔子水晶酒店\n4. 和颐酒店",
            "豪华": "豪华酒店:\n1. 上海外滩华尔道夫酒店\n2. 上海浦东丽思卡尔顿酒店\n3. 上海半岛酒店\n4. 上海宝格丽酒店"
        }
    }
  
    if city in hotels_db and budget in hotels_db[city]:
        return hotels_db[city][budget]
    else:
        return f"建议您通过携程、去哪儿等平台查询{city}的{budget}价位酒店。"


# 工具函数字典，方便智能体调用
AVAILABLE_TOOLS = {
    "get_weather": get_weather,
    "get_attraction": get_attraction,
    "get_hotels": get_hotels,
}
