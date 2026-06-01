#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
DevMind-CLI 核心模块 - 代码分析器
"""

import os
import ast
import re
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from collections import defaultdict


class CodeAnalyzer:
    """代码静态分析器"""
    
    # 支持的语言及文件扩展名
    LANGUAGES = {
        "python": [".py"],
        "javascript": [".js", ".jsx", ".mjs"],
        "typescript": [".ts", ".tsx"],
        "java": [".java"],
        "c": [".c", ".h"],
        "cpp": [".cpp", ".hpp", ".cc", ".cxx"],
        "go": [".go"],
        "rust": [".rs"],
        "ruby": [".rb"],
        "php": [".php"],
    }
    
    def __init__(self, llm_client):
        """
        初始化分析器
        
        Args:
            llm_client: LLM客户端实例
        """
        self.llm = llm_client
        self.stats = defaultdict(int)
    
    def analyze(
        self,
        path: str,
        recursive: bool = True,
        output: Optional[str] = None,
        format: str = "text"
    ) -> str:
        """
        分析代码
        
        Args:
            path: 代码路径
            recursive: 是否递归
            output: 输出文件
            format: 输出格式
            
        Returns:
            分析结果
        """
        path_obj = Path(path)
        
        if not path_obj.exists():
            return f"❌ 路径不存在: {path}"
        
        # 收集所有代码文件
        code_files = self._collect_files(path_obj, recursive)
        
        if not code_files:
            return "⚠️ 未找到代码文件"
        
        # 统计分析
        self._collect_stats(code_files)
        
        # 生成报告
        if format == "json":
            return self._generate_json_report(code_files)
        elif format == "markdown":
            return self._generate_markdown_report(code_files)
        else:
            return self._generate_text_report(code_files)
    
    def _collect_files(
        self,
        path: Path,
        recursive: bool
    ) -> List[Path]:
        """收集代码文件"""
        files = []
        
        if path.is_file():
            if self._is_code_file(path):
                files.append(path)
        elif path.is_dir():
            pattern = "**/*" if recursive else "*"
            for ext_list in self.LANGUAGES.values():
                for ext in ext_list:
                    files.extend(path.glob(f"{pattern}{ext}"))
        
        return sorted(set(files))
    
    def _is_code_file(self, path: Path) -> bool:
        """判断是否为代码文件"""
        for ext_list in self.LANGUAGES.values():
            if path.suffix in ext_list:
                return True
        return False
    
    def _collect_stats(self, files: List[Path]) -> None:
        """收集统计数据"""
        self.stats.clear()
        
        total_lines = 0
        total_files = len(files)
        
        language_counts = defaultdict(int)
        language_lines = defaultdict(int)
        
        for file_path in files:
            try:
                with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                    content = f.read()
                    lines = len(content.splitlines())
                    total_lines += lines
                    
                    # 统计语言
                    lang = self._detect_language(file_path)
                    language_counts[lang] += 1
                    language_lines[lang] += lines
                    
            except Exception:
                continue
        
        self.stats["total_files"] = total_files
        self.stats["total_lines"] = total_lines
        self.stats["language_counts"] = dict(language_counts)
        self.stats["language_lines"] = dict(language_lines)
    
    def _detect_language(self, path) -> str:
        """检测编程语言"""
        if isinstance(path, str):
            path = Path(path)
        ext = path.suffix
        for lang, exts in self.LANGUAGES.items():
            if ext in exts:
                return lang
        return "unknown"
    
    def _generate_text_report(self, files: List[Path]) -> str:
        """生成文本报告"""
        report = []
        report.append("=" * 60)
        report.append("📊 DevMind-CLI 代码分析报告")
        report.append("=" * 60)
        report.append("")
        report.append(f"📁 分析文件数: {self.stats['total_files']}")
        report.append(f"📝 总代码行数: {self.stats['total_lines']:,}")
        report.append("")
        report.append("🔤 语言分布:")
        report.append("-" * 40)
        
        for lang, count in sorted(
            self.stats["language_counts"].items(),
            key=lambda x: x[1],
            reverse=True
        ):
            lines = self.stats["language_lines"][lang]
            pct = count / self.stats["total_files"] * 100
            report.append(f"  {lang:15} {count:3} 文件 ({pct:5.1f}%)  {lines:6,} 行")
        
        report.append("")
        report.append("📂 文件列表:")
        report.append("-" * 40)
        
        for i, file_path in enumerate(files[:50], 1):
            try:
                with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                    lines = len(f.read().splitlines())
                report.append(f"  {i:3}. {file_path} ({lines} 行)")
            except Exception:
                report.append(f"  {i:3}. {file_path}")
        
        if len(files) > 50:
            report.append(f"  ... 还有 {len(files) - 50} 个文件")
        
        report.append("")
        report.append("=" * 60)
        report.append("💡 提示: 使用 'devmind review' 获取详细代码审查")
        report.append("=" * 60)
        
        return "\n".join(report)
    
    def _generate_json_report(self, files: List[Path]) -> str:
        """生成JSON报告"""
        import json
        
        report = {
            "summary": {
                "total_files": self.stats["total_files"],
                "total_lines": self.stats["total_lines"],
                "languages": dict(self.stats["language_counts"])
            },
            "files": [
                {
                    "path": str(f),
                    "language": self._detect_language(f),
                    "lines": self._count_lines(f)
                }
                for f in files
            ]
        }
        
        return json.dumps(report, indent=2, ensure_ascii=False)
    
    def _generate_markdown_report(self, files: List[Path]) -> str:
        """生成Markdown报告"""
        report = []
        report.append("# 📊 DevMind-CLI 代码分析报告")
        report.append("")
        report.append("## 📈 统计概览")
        report.append("")
        report.append(f"| 指标 | 数值 |")
        report.append("|------|------|")
        report.append(f"| 文件数 | {self.stats['total_files']} |")
        report.append(f"| 代码行数 | {self.stats['total_lines']:,} |")
        report.append("")
        report.append("## 🔤 语言分布")
        report.append("")
        report.append("| 语言 | 文件数 | 行数 | 占比 |")
        report.append("|------|--------|------|------|")
        
        for lang in sorted(
            self.stats["language_counts"],
            key=lambda x: self.stats["language_counts"][x],
            reverse=True
        ):
            count = self.stats["language_counts"][lang]
            lines = self.stats["language_lines"][lang]
            pct = count / self.stats["total_files"] * 100
            report.append(f"| {lang} | {count} | {lines:,} | {pct:.1f}% |")
        
        return "\n".join(report)
    
    def _count_lines(self, path: Path) -> int:
        """计算文件行数"""
        try:
            with open(path, "r", encoding="utf-8", errors="ignore") as f:
                return len(f.read().splitlines())
        except Exception:
            return 0


class PythonAnalyzer:
    """Python专用分析器"""
    
    def __init__(self):
        self.tree = None
        self.source = ""
    
    def parse(self, source: str) -> bool:
        """解析Python代码"""
        try:
            self.source = source
            self.tree = ast.parse(source)
            return True
        except SyntaxError:
            return False
    
    def get_functions(self) -> List[Dict]:
        """获取所有函数"""
        functions = []
        
        for node in ast.walk(self.tree):
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                functions.append({
                    "name": node.name,
                    "lineno": node.lineno,
                    "end_lineno": node.end_lineno,
                    "args": [arg.arg for arg in node.args.args],
                    "is_async": isinstance(node, ast.AsyncFunctionDef),
                    "docstring": ast.get_docstring(node)
                })
        
        return functions
    
    def get_classes(self) -> List[Dict]:
        """获取所有类"""
        classes = []
        
        for node in ast.walk(self.tree):
            if isinstance(node, ast.ClassDef):
                methods = [
                    m.name for m in node.body
                    if isinstance(m, (ast.FunctionDef, ast.AsyncFunctionDef))
                ]
                classes.append({
                    "name": node.name,
                    "lineno": node.lineno,
                    "end_lineno": node.end_lineno,
                    "methods": methods,
                    "docstring": ast.get_docstring(node)
                })
        
        return classes
    
    def get_imports(self) -> List[Dict]:
        """获取所有导入"""
        imports = []
        
        for node in ast.walk(self.tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    imports.append({
                        "type": "import",
                        "name": alias.name,
                        "alias": alias.asname
                    })
            elif isinstance(node, ast.ImportFrom):
                module = node.module or ""
                for alias in node.names:
                    imports.append({
                        "type": "from",
                        "module": module,
                        "name": alias.name,
                        "alias": alias.asname
                    })
        
        return imports
