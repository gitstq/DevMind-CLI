#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
DevMind-CLI 工具模块 - 代码审查
"""

import os
from pathlib import Path
from typing import Optional, List, Dict


class CodeReviewer:
    """AI代码审查器"""
    
    def __init__(self, llm_client):
        """
        初始化审查器
        
        Args:
            llm_client: LLM客户端
        """
        self.llm = llm_client
    
    def review(
        self,
        file_path: Optional[str] = None,
        dir_path: Optional[str] = None,
        strict: bool = False,
        output: Optional[str] = None
    ) -> str:
        """
        审查代码
        
        Args:
            file_path: 文件路径
            dir_path: 目录路径
            strict: 严格模式
            output: 输出文件
            
        Returns:
            审查结果
        """
        # 收集代码文件
        files_to_review = []
        
        if file_path:
            path = Path(file_path)
            if path.exists():
                files_to_review.append(path)
        
        if dir_path:
            dir_obj = Path(dir_path)
            if dir_obj.is_dir():
                for ext in [".py", ".js", ".ts", ".go", ".java"]:
                    files_to_review.extend(dir_obj.rglob(f"*{ext}"))
        
        if not files_to_review:
            return "❌ 未找到要审查的文件"
        
        # 读取代码
        code_contents = []
        for file_path in files_to_review[:5]:  # 限制文件数量
            try:
                with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                    content = f.read()
                    if len(content) > 0:
                        code_contents.append({
                            "file": str(file_path),
                            "content": content[:2000]  # 限制长度
                        })
            except Exception:
                continue
        
        if not code_contents:
            return "❌ 无法读取文件内容"
        
        # 生成审查报告
        report = self._generate_review_report(code_contents, strict)
        
        # 保存输出
        if output:
            self._save_report(report, output)
        
        return report
    
    def _generate_review_report(
        self,
        code_contents: List[Dict],
        strict: bool
    ) -> str:
        """生成审查报告"""
        report = []
        report.append("=" * 60)
        report.append("🔍 DevMind-CLI AI代码审查报告")
        report.append("=" * 60)
        report.append("")
        
        mode = "严格模式" if strict else "标准模式"
        report.append(f"📋 审查模式: {mode}")
        report.append(f"📁 审查文件数: {len(code_contents)}")
        report.append("")
        
        # 对每个文件进行审查
        for item in code_contents:
            file_path = item["file"]
            content = item["content"]
            lang = self._detect_language(file_path)
            
            report.append(f"📄 文件: {file_path}")
            report.append("-" * 40)
            
            # 使用AI审查
            prompt = f"""请审查以下{lang}代码，关注：
1. 代码风格和最佳实践
2. 潜在的Bug和安全问题
3. 性能优化建议
4. 可维护性问题

代码:
```{lang}
{content}
```

请用简洁的要点格式回复，每个方面不超过3条建议。"""
            
            if strict:
                prompt += "\n\n注意：严格模式下请更关注潜在问题。"
            
            messages = [
                {"role": "system", "content": "你是一个专业的代码审查专家，请给出客观、具体的建议。"},
                {"role": "user", "content": prompt}
            ]
            
            try:
                result = self.llm.chat(messages)
                report.append(result)
            except Exception as e:
                report.append(f"⚠️ 审查失败: {str(e)}")
            
            report.append("")
        
        report.append("=" * 60)
        report.append("💡 提示: 使用 'devmind refactor --file <path>' 获取重构建议")
        report.append("=" * 60)
        
        return "\n".join(report)
    
    def _detect_language(self, file_path: str) -> str:
        """检测编程语言"""
        ext = Path(file_path).suffix.lower()
        
        lang_map = {
            ".py": "python",
            ".js": "javascript",
            ".ts": "typescript",
            ".jsx": "javascript",
            ".tsx": "typescript",
            ".go": "go",
            ".java": "java",
            ".c": "c",
            ".cpp": "cpp",
            ".rs": "rust",
            ".rb": "ruby",
            ".php": "php"
        }
        
        return lang_map.get(ext, "text")
    
    def _save_report(self, report: str, output_path: str) -> None:
        """保存报告到文件"""
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(report)
