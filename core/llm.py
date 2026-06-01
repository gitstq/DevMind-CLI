#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
DevMind-CLI 核心模块 - LLM接口封装
"""

import json
import time
from typing import Optional, Dict, Any, List
from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError


class GLMClient:
    """GLM-5.1 API客户端"""
    
    def __init__(
        self,
        api_key: Optional[str] = None,
        api_url: str = "https://open.bigmodel.cn/api/paas/v4",
        model: str = "glm-5-0520",
        timeout: int = 120,
        verbose: bool = False
    ):
        """
        初始化GLM客户端
        
        Args:
            api_key: API密钥
            api_url: API地址
            model: 模型名称
            timeout: 超时时间（秒）
            verbose: 详细输出模式
        """
        self.api_key = api_key
        self.api_url = api_url
        self.model = model
        self.timeout = timeout
        self.verbose = verbose
        
        # 如果没有提供API密钥，尝试从环境变量获取
        if not self.api_key:
            import os
            self.api_key = os.environ.get("GLM_API_KEY")
        
        # 默认系统提示词
        self.system_prompt = """你是一个专业的代码智能助手，名叫DevMind。
你的职责是：
1. 分析代码结构和逻辑
2. 发现潜在的问题和优化点
3. 提供高质量的代码建议
4. 生成清晰的文档

请用简洁、专业的方式回答。如果不确定，请如实说明。"""
    
    def chat(
        self,
        messages: List[Dict[str, str]],
        temperature: float = 0.7,
        max_tokens: int = 2048
    ) -> str:
        """
        发送对话请求
        
        Args:
            messages: 消息列表
            temperature: 温度参数
            max_tokens: 最大令牌数
            
        Returns:
            AI响应文本
        """
        if not self.api_key:
            return self._offline_response("API密钥未设置，请设置 GLM_API_KEY 环境变量或使用 --api-key 参数")
        
        # 构建请求
        url = f"{self.api_url}/chat/completions"
        
        payload = {
            "model": self.model,
            "messages": messages,
            "temperature": temperature,
            "max_tokens": max_tokens
        }
        
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        if self.verbose:
            print(f"📡 发送请求到: {url}")
            print(f"📦 模型: {self.model}")
        
        try:
            req = Request(
                url,
                data=json.dumps(payload).encode("utf-8"),
                headers=headers,
                method="POST"
            )
            
            with urlopen(req, timeout=self.timeout) as response:
                result = json.loads(response.read().decode("utf-8"))
                
                if self.verbose:
                    print(f"✅ 请求成功")
                
                return result["choices"][0]["message"]["content"]
                
        except HTTPError as e:
            error_body = e.read().decode("utf-8") if e.fp else ""
            return self._error_response(f"API请求失败 (HTTP {e.code}): {error_body}")
        except URLError as e:
            return self._error_response(f"网络错误: {e.reason}")
        except Exception as e:
            return self._error_response(f"未知错误: {str(e)}")
    
    def analyze_code(
        self,
        code: str,
        language: str = "python",
        task: str = "analyze"
    ) -> str:
        """
        分析代码
        
        Args:
            code: 代码内容
            language: 编程语言
            task: 分析任务类型
            
        Returns:
            分析结果
        """
        prompts = {
            "analyze": f"""请分析以下{language}代码，给出：
1. 代码结构和主要功能
2. 潜在的Bug或问题
3. 性能优化建议
4. 代码质量评分（1-10）

代码:
```{language}
{code}
```""",
            
            "review": f"""请审查以下{language}代码，关注：
1. 代码风格一致性
2. 最佳实践遵循情况
3. 安全漏洞
4. 可维护性问题

代码:
```{language}
{code}
```""",
            
            "explain": f"""请解释以下{language}代码的逻辑和功能：

代码:
```{language}
{code}
```""",
            
            "debug": f"""请分析以下{language}代码可能存在的问题，并给出调试建议：

代码:
```{language}
{code}
```"""
        }
        
        prompt = prompts.get(task, prompts["analyze"])
        
        messages = [
            {"role": "system", "content": self.system_prompt},
            {"role": "user", "content": prompt}
        ]
        
        return self.chat(messages)
    
    def generate_code(
        self,
        description: str,
        language: str = "python",
        context: str = ""
    ) -> str:
        """
        生成代码
        
        Args:
            description: 功能描述
            language: 目标语言
            context: 上下文代码
            
        Returns:
            生成的代码
        """
        prompt = f"""请生成{language}代码，实现以下功能：

功能描述: {description}
"""
        
        if context:
            prompt += f"\n\n上下文代码:\n```{language}\n{context}\n```"
        
        prompt += "\n\n请直接提供代码，不需要过多解释。"
        
        messages = [
            {"role": "system", "content": self.system_prompt},
            {"role": "user", "content": prompt}
        ]
        
        return self.chat(messages, temperature=0.8)
    
    def suggest_refactor(
        self,
        code: str,
        language: str = "python"
    ) -> str:
        """
        提供重构建议
        
        Args:
            code: 代码内容
            language: 编程语言
            
        Returns:
            重构建议
        """
        prompt = f"""请分析以下{language}代码并提供重构建议：

代码:
```{language}
{code}
```

请给出：
1. 当前代码的问题
2. 重构后的代码
3. 重构的理由
"""
        
        messages = [
            {"role": "system", "content": self.system_prompt},
            {"role": "user", "content": prompt}
        ]
        
        return self.chat(messages, temperature=0.7)
    
    def generate_docstring(
        self,
        code: str,
        language: str = "python"
    ) -> str:
        """
        生成文档字符串
        
        Args:
            code: 代码内容
            language: 编程语言
            
        Returns:
            文档字符串
        """
        prompt = f"""请为以下{language}代码生成Google风格的docstring：

代码:
```{language}
{code}
```

只返回docstring代码，不需要其他内容。"""
        
        messages = [
            {"role": "system", "content": self.system_prompt},
            {"role": "user", "content": prompt}
        ]
        
        return self.chat(messages, temperature=0.3)
    
    def _offline_response(self, message: str) -> str:
        """离线模式响应"""
        return f"""⚠️ 离线模式

{message}

离线模式可用的功能：
- 本地代码语法分析
- 基础代码统计
- 简单的模式匹配

要使用AI功能，请配置API密钥。"""
    
    def _error_response(self, error: str) -> str:
        """错误响应"""
        return f"""❌ 请求失败

{error}

请检查：
1. API密钥是否正确
2. 网络连接是否正常
3. API额度是否充足

也可以使用 --verbose 参数查看详细信息。"""
