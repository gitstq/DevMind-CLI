#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
DevMind-CLI 工具模块 - 重构建议
"""

from pathlib import Path
from typing import Optional, Dict


class RefactorAdvisor:
    """代码重构顾问"""
    
    def __init__(self, llm_client):
        """
        初始化重构顾问
        
        Args:
            llm_client: LLM客户端
        """
        self.llm = llm_client
    
    def get_suggestions(
        self,
        file_path: str,
        function_name: Optional[str] = None,
        line_start: Optional[int] = None,
        line_end: Optional[int] = None
    ) -> str:
        """
        获取重构建议
        
        Args:
            file_path: 文件路径
            function_name: 函数名
            line_start: 起始行
            line_end: 结束行
            
        Returns:
            重构建议
        """
        path = Path(file_path)
        
        if not path.exists():
            return f"❌ 文件不存在: {file_path}"
        
        # 读取文件内容
        with open(path, "r", encoding="utf-8", errors="ignore") as f:
            content = f.read()
        
        # 根据参数提取代码片段
        if function_name:
            code = self._extract_function(content, function_name)
            if not code:
                return f"❌ 未找到函数: {function_name}"
        elif line_start and line_end:
            lines = content.splitlines()
            code = "\n".join(lines[line_start-1:line_end])
        else:
            code = content
        
        lang = self._detect_language(file_path)
        
        # 获取重构建议
        return self._get_refactor_advice(code, lang)
    
    def _extract_function(self, content: str, function_name: str) -> Optional[str]:
        """提取函数代码"""
        import re
        
        # 匹配函数定义
        patterns = [
            rf"def\s+{function_name}\s*\([^)]*\):.*?(?=\n(?:def |class |$))",
            rf"async\s+def\s+{function_name}\s*\([^)]*\):.*?(?=\n(?:def |class |$))",
            rf"function\s+{function_name}\s*\([^)]*\)\s*{{.*?(?=\n(?:function |class |}}|$))",
        ]
        
        for pattern in patterns:
            match = re.search(pattern, content, re.DOTALL)
            if match:
                return match.group(0)
        
        return None
    
    def _get_refactor_advice(self, code: str, language: str) -> str:
        """获取重构建议"""
        prompt = f"""请分析以下{language}代码，提供重构建议：

```{language}
{code}
```

请按以下格式回复：

## 📋 当前问题
- 问题1
- 问题2

## 🔧 重构方案
```refactored_{language}
重构后的代码
```

## 💡 重构理由
- 理由1
- 理由2
"""
        
        messages = [
            {"role": "system", "content": "你是一个专业的代码重构专家，请提供实用的重构建议。"},
            {"role": "user", "content": prompt}
        ]
        
        try:
            result = self.llm.chat(messages)
            
            report = []
            report.append("=" * 60)
            report.append("🔧 DevMind-CLI 重构建议")
            report.append("=" * 60)
            report.append("")
            report.append(result)
            report.append("")
            report.append("=" * 60)
            
            return "\n".join(report)
        except Exception as e:
            return f"❌ 获取建议失败: {str(e)}"
    
    def _detect_language(self, file_path: str) -> str:
        """检测编程语言"""
        ext = Path(file_path).suffix.lower()
        
        lang_map = {
            ".py": "python",
            ".js": "javascript",
            ".ts": "typescript",
            ".go": "go",
            ".java": "java",
            ".c": "c",
            ".cpp": "cpp",
            ".rs": "rust",
            ".rb": "ruby",
            ".php": "php"
        }
        
        return lang_map.get(ext, "text")
