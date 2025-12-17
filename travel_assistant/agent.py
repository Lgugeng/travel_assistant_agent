"""
智能体主模块
"""

import re
from typing import Dict, List
from .tools import AVAILABLE_TOOLS
from .config import DEFAULT_CONFIG


class TravelAssistantAgent:
    """
    智能旅行助手智能体
    """
  
    def __init__(self, client, tools: Dict = None, system_prompt: str = None):
        """
        初始化智能体
      
        Args:
            client: LLM客户端实例
            tools: 可用工具字典
            system_prompt: 系统提示词
        """
        self.client = client
        self.tools = tools or AVAILABLE_TOOLS.copy()
        self.conversation_history = []
      
        # 默认系统提示词
        self.system_prompt = system_prompt or """
        你是一个智能旅行助手。你的任务是分析用户的请求，并使用可用工具一步步地解决问题。

        可用工具:
        - `get_weather(city: str)`: 查询指定城市的实时天气。
        - `get_attraction(city: str, weather: str)`: 根据城市和天气搜索推荐的旅游景点。
        - `get_hotels(city: str, budget: str)`: 根据城市和预算推荐酒店。

        行动格式:
        你的回答必须严格遵循以下格式。首先是你的思考过程，然后是你要执行的具体行动：
        Thought: [这里是你的思考过程和下一步计划]
        Action: [这里是你要调用的工具，格式为 function_name(arg_name="arg_value")]

        任务完成:
        当你收集到足够的信息，能够回答用户的最终问题时，你必须在`Action:`字段后使用 `finish(answer="...")` 来输出最终答案。

        请开始吧！
        """
  
    def add_tool(self, name: str, tool_function):
        """
        添加新工具
      
        Args:
            name: 工具名称
            tool_function: 工具函数
        """
        self.tools[name] = tool_function
  
    def parse_llm_output(self, llm_output: str) -> tuple:
        """
        解析LLM输出
      
        Args:
            llm_output: LLM原始输出
          
        Returns:
            (thought, action_str) 或 (None, None)
        """
        # 移除re.DOTALL标志，避免.匹配换行符
        patterns = [
            (r"Thought:\s*(.*?)(?=\r?\nAction:|$)", r"Action:\s*(.*?)(?=\r?\nThought:|$)"),
            (r"思考[:：]\s*(.*?)(?=\r?\n行动[:：]|$)", r"(?:行动|Action)[:：]\s*(.*?)(?=\r?\n|$)"),
            (r"THOUGHT:\s*(.*?)(?=\r?\nACTION:|$)", r"ACTION:\s*(.*?)(?=\r?\n|$)"),
        ]
      
        for thought_pattern, action_pattern in patterns:
            thought_match = re.search(thought_pattern, llm_output, re.IGNORECASE | re.MULTILINE)
            action_match = re.search(action_pattern, llm_output, re.IGNORECASE | re.MULTILINE)
          
            if thought_match and action_match:
                thought = thought_match.group(1).strip()
                action_str = action_match.group(1).strip()
                return thought, action_str
      
        return None, None
  
    def execute_action(self, action_str: str) -> str:
        """
        执行动作
      
        Args:
            action_str: 动作字符串
          
        Returns:
            执行结果
        """
        # 检查是否是finish动作
        if action_str.lower().startswith("finish"):
            match = re.search(r'finish\(answer="(.*)"\)', action_str, re.DOTALL)
            if match:
                return f"FINISH: {match.group(1)}"
          
            match = re.search(r"finish\(answer='(.*)'\)", action_str, re.DOTALL)
            if match:
                return f"FINISH: {match.group(1)}"
          
            # 简化的finish格式
            if action_str.lower().startswith("finish"):
                answer = action_str[6:].strip('()\"\'').strip()
                return f"FINISH: {answer}"
          
            return "错误: finish命令格式不正确"
      
        # 解析工具调用
        match = re.match(r'(\w+)\((.*)\)', action_str.strip())
        if not match:
            return f"错误: 无法解析动作 '{action_str}'"
      
        tool_name = match.group(1)
        args_str = match.group(2)
      
        # 解析参数
        kwargs = {}
        if args_str:
            # 匹配键值对
            pattern = r'(\w+)=["\']?([^\"\',]+)["\']?'
            matches = re.findall(pattern, args_str)
            for key, value in matches:
                kwargs[key] = value.strip(' \"\'')
      
        # 执行工具
        if tool_name in self.tools:
            try:
                result = self.tools[tool_name](**kwargs)
                return result
            except Exception as e:
                return f"错误: 执行工具时出错 - {str(e)}"
        else:
            return f"错误: 未定义的工具 '{tool_name}'"
  
    def run(self, user_query: str, max_iterations: int = None, 
            stream: bool = False, verbose: bool = True) -> str:
        """
        运行智能体
      
        Args:
            user_query: 用户查询
            max_iterations: 最大迭代次数
            stream: 是否使用流式输出
            verbose: 是否打印详细信息
          
        Returns:
            最终结果
        """
        max_iterations = max_iterations or DEFAULT_CONFIG["max_iterations"]
        self.conversation_history = [f"用户请求: {user_query}"]
      
        if verbose:
            print(f"🤖 智能体开始处理请求: {user_query}")
      
        for iteration in range(1, max_iterations + 1):
            if verbose:
                print(f"\n🔄 第 {iteration} 轮循环")
          
            # 构建完整prompt
            full_prompt = "\n".join(self.conversation_history)
          
            # 调用LLM
            messages = [
                {"role": "system", "content": self.system_prompt},
                {"role": "user", "content": full_prompt}
            ]
          
            if stream:
                if verbose:
                    print("💭 思考中: ", end="")
              
                # 流式输出
                llm_output = ""
                for chunk in self.client.chat(messages, stream=True):
                    llm_output += chunk
                    if verbose:
                        print(chunk, end="", flush=True)
              
                if verbose:
                    print()
            else:
                llm_output = self.client.chat(messages, stream=False)
                if verbose:
                    print(f"💭 思考结果: {llm_output[:100]}...")
          
            # 解析输出
            thought, action_str = self.parse_llm_output(llm_output)
          
            if not thought or not action_str:
                if verbose:
                    print("⚠️ 无法解析输出格式")
                self.conversation_history.append("错误: 无法解析输出格式")
                break
          
            # 记录思考
            self.conversation_history.append(f"Thought: {thought}")
            if verbose:
                print(f"🤔 思考: {thought}")
          
            # 执行行动
            self.conversation_history.append(f"Action: {action_str}")
            if verbose:
                print(f"🔧 行动: {action_str}")
          
            observation = self.execute_action(action_str)
          
            # 检查是否完成
            if observation.startswith("FINISH:"):
                final_answer = observation[7:].strip()
                if verbose:
                    print(f"\n✅ 任务完成: {final_answer[:100]}...")
                return final_answer
          
            # 记录观察
            self.conversation_history.append(f"Observation: {observation}")
            if verbose:
                print(f"👀 观察: {observation[:100]}...")
      
        # 达到最大迭代次数
        if verbose:
            print(f"⚠️ 达到最大迭代次数 ({max_iterations})，任务未完成")
      
        # 尝试返回最后的结果
        for entry in reversed(self.conversation_history):
            if entry.startswith("Observation:"):
                return entry[12:].strip()
      
        return "任务未完成"
  
    def get_conversation_history(self) -> List[str]:
        """
        获取对话历史
      
        Returns:
            对话历史列表
        """
        return self.conversation_history.copy()
  
    def clear_history(self):
        """清空对话历史"""
        self.conversation_history = []
