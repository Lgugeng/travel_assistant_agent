"""
配置模块
"""

DEFAULT_CONFIG = {
    "api_base_url": "https://api.siliconflow.cn/v1",
    "default_model": "deepseek-ai/DeepSeek-V2.5",
    "default_temperature": 0.7,
    "max_iterations": 5,
    "timeout": 30,
}

# 支持的模型列表
SUPPORTED_MODELS = {
    "deepseek-v2.5": "deepseek-ai/DeepSeek-V2.5",
    "qwen2.5-7b": "Qwen/Qwen2.5-7B-Instruct",
    "qwen2.5-14b": "Qwen/Qwen2.5-14B-Instruct",
    "chatglm3-6b": "THUDM/chatglm3-6b",
    "llama-3.2-3b": "meta-llama/Llama-3.2-3B-Instruct",
    "llama-3.1-8b": "meta-llama/Llama-3.1-8B-Instruct",
    "yi-6b": "01-ai/Yi-6B",
}

# 预设的城市天气对应关系
CITY_MAPPING = {
    "北京": "Beijing", "上海": "Shanghai", "广州": "Guangzhou", "深圳": "Shenzhen",
    "杭州": "Hangzhou", "南京": "Nanjing", "成都": "Chengdu", "重庆": "Chongqing",
    "西安": "Xi'an", "武汉": "Wuhan", "苏州": "Suzhou", "厦门": "Xiamen",
    "青岛": "Qingdao", "大连": "Dalian", "天津": "Tianjin", "沈阳": "Shenyang",
    "哈尔滨": "Harbin", "长春": "Changchun", "郑州": "Zhengzhou", "长沙": "Changsha",
    "合肥": "Hefei", "福州": "Fuzhou", "昆明": "Kunming", "南宁": "Nanning",
    "贵阳": "Guiyang", "兰州": "Lanzhou", "银川": "Yinchuan", "西宁": "Xining",
    "乌鲁木齐": "Urumqi", "拉萨": "Lhasa", "香港": "Hongkong", "澳门": "Macau",
    "台北": "Taipei"
}
