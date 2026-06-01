#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
DevMind-CLI 核心模块 - 代码扫描器
"""

import os
import re
from pathlib import Path
from typing import Dict, List, Set, Optional, Tuple
from collections import defaultdict


class CodeScanner:
    """代码扫描器 - 检测潜在问题"""
    
    # 扫描规则定义
    RULES = {
        "security": [
            {
                "id": "SEC001",
                "name": "硬编码密码",
                "pattern": r"(password|passwd|pwd|secret|api_key|apikey|token)\s*=\s*['\"][^'\"]{4,}['\"]",
                "severity": "high",
                "message": "发现硬编码的敏感信息，请使用环境变量或配置文件"
            },
            {
                "id": "SEC002",
                "name": "SQL注入风险",
                "pattern": r"(execute|cursor\.execute)\s*\(\s*['\"].*\%.*['\"]",
                "severity": "high",
                "message": "可能存在SQL注入风险，建议使用参数化查询"
            },
            {
                "id": "SEC003",
                "name": "命令注入风险",
                "pattern": r"(os\.system|os\.popen|subprocess\.call|subprocess\.run)\s*\(",
                "severity": "medium",
                "message": "可能存在命令注入风险，请确保输入已验证"
            }
        ],
        "quality": [
            {
                "id": "QUAL001",
                "name": "过长函数",
                "pattern": r"^.{100,}$",
                "severity": "low",
                "message": "行长度超过100字符，建议拆分"
            },
            {
                "id": "QUAL002",
                "name": "TODO注释",
                "pattern": r"#\s*(TODO|FIXME|HACK|XXX|NOTE):",
                "severity": "info",
                "message": "发现TODO标记，需要后续处理"
            },
            {
                "id": "QUAL003",
                "name": "调试代码",
                "pattern": r"(print|console\.log|logger\.debug)\s*\(",
                "severity": "info",
                "message": "发现调试代码，生产环境应移除"
            }
        ],
        "style": [
            {
                "id": "STYLE001",
                "name": "长函数",
                "pattern": r"def\s+\w+\([^)]*\):",
                "max_lines": 50,
                "severity": "low",
                "message": "函数可能过长，建议拆分"
            },
            {
                "id": "STYLE002",
                "name": "嵌套过深",
                "pattern": r"(if|for|while|with).*(if|for|while|with).*(if|for|while|with).*(if|for|while|with)",
                "severity": "medium",
                "message": "嵌套层级过深，建议使用函数或早期返回"
            }
        ]
    }
    
    # 支持的文件类型
    SUPPORTED_EXTENSIONS = [
        ".py", ".js", ".ts", ".jsx", ".tsx",
        ".java", ".c", ".cpp", ".h", ".hpp",
        ".go", ".rs", ".rb", ".php", ".cs"
    ]
    
    # 排除的目录
    EXCLUDE_DIRS = [
        "node_modules", "__pycache__", ".git", ".venv",
        "venv", "env", ".idea", ".vscode", "dist",
        "build", "target", "bin", "obj"
    ]
    
    def __init__(self, llm_client=None):
        """
        初始化扫描器
        
        Args:
            llm_client: LLM客户端（用于智能分析）
        """
        self.llm = llm_client
        self.results = []
        self.stats = defaultdict(int)
    
    def scan(
        self,
        path: str,
        exclude: List[str] = None,
        report: bool = False
    ) -> str:
        """
        扫描代码
        
        Args:
            path: 扫描路径
            exclude: 排除的目录
            report: 是否生成报告
            
        Returns:
            扫描结果
        """
        path_obj = Path(path)
        
        if not path_obj.exists():
            return f"❌ 路径不存在: {path}"
        
        # 收集要扫描的文件
        files = self._collect_files(path_obj, exclude or [])
        
        if not files:
            return "⚠️ 未找到可扫描的文件"
        
        # 执行扫描
        self.results = []
        self._scan_files(files)
        
        # 生成报告
        return self._generate_report(files, report)
    
    def _collect_files(
        self,
        path: Path,
        exclude: List[str]
    ) -> List[Path]:
        """收集要扫描的文件"""
        files = []
        exclude_set = set(self.EXCLUDE_DIRS + exclude)
        
        for root, dirs, filenames in os.walk(path):
            # 排除目录
            dirs[:] = [d for d in dirs if d not in exclude_set]
            
            for filename in filenames:
                file_path = Path(root) / filename
                
                if file_path.suffix in self.SUPPORTED_EXTENSIONS:
                    files.append(file_path)
        
        return files
    
    def _scan_files(self, files: List[Path]) -> None:
        """扫描所有文件"""
        for file_path in files:
            self._scan_file(file_path)
    
    def _scan_file(self, file_path: Path) -> None:
        """扫描单个文件"""
        try:
            with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                lines = f.readlines()
                content = f.read()
            
            # 逐行扫描
            for i, line in enumerate(lines, 1):
                line = line.strip()
                
                for category, rules in self.RULES.items():
                    for rule in rules:
                        if self._check_rule(rule, line, content, i):
                            self.results.append({
                                "file": str(file_path),
                                "line": i,
                                "content": line.strip(),
                                "rule_id": rule["id"],
                                "rule_name": rule["name"],
                                "category": category,
                                "severity": rule["severity"],
                                "message": rule["message"]
                            })
                            self.stats[category] += 1
                            self.stats[rule["severity"]] += 1
            
            # 统计函数长度
            self._check_function_length(content, str(file_path))
            
        except Exception as e:
            pass
    
    def _check_rule(
        self,
        rule: Dict,
        line: str,
        content: str,
        line_num: int
    ) -> bool:
        """检查规则"""
        pattern = rule.get("pattern")
        
        if pattern:
            return bool(re.search(pattern, line, re.IGNORECASE))
        
        return False
    
    def _check_function_length(
        self,
        content: str,
        file_path: str
    ) -> None:
        """检查函数长度"""
        if not content:
            return
        
        # 简单的函数长度检查
        in_function = False
        function_lines = 0
        function_start = 0
        
        for i, line in enumerate(content.splitlines(), 1):
            stripped = line.strip()
            
            # 检测函数定义
            if re.match(r"^(def |async def |function |func |public |private )", stripped):
                if in_function and function_lines > 50:
                    self.results.append({
                        "file": file_path,
                        "line": function_start,
                        "content": f"[函数长度: {function_lines} 行]",
                        "rule_id": "STYLE001",
                        "rule_name": "长函数",
                        "category": "style",
                        "severity": "low",
                        "message": f"函数长度 {function_lines} 行，建议拆分为更小的函数"
                    })
                    self.stats["style"] += 1
                    self.stats["low"] += 1
                
                in_function = True
                function_lines = 1
                function_start = i
            elif in_function:
                # 检查缩进判断函数结束
                if line and not line[0].isspace():
                    in_function = False
        
        # 检查最后一个函数
        if in_function and function_lines > 50:
            self.results.append({
                "file": file_path,
                "line": function_start,
                "content": f"[函数长度: {function_lines} 行]",
                "rule_id": "STYLE001",
                "rule_name": "长函数",
                "category": "style",
                "severity": "low",
                "message": f"函数长度 {function_lines} 行，建议拆分"
            })
            self.stats["style"] += 1
            self.stats["low"] += 1
    
    def _generate_report(
        self,
        files: List[Path],
        detailed: bool
    ) -> str:
        """生成扫描报告"""
        report = []
        report.append("=" * 60)
        report.append("🔍 DevMind-CLI 安全扫描报告")
        report.append("=" * 60)
        report.append("")
        report.append(f"📂 扫描文件数: {len(files)}")
        report.append(f"⚠️  发现问题数: {len(self.results)}")
        report.append("")
        
        # 按严重性统计
        report.append("📊 问题分布:")
        report.append("-" * 40)
        report.append(f"  🔴 高危: {self.stats.get('high', 0)}")
        report.append(f"  🟡 中危: {self.stats.get('medium', 0)}")
        report.append(f"  🟢 低危: {self.stats.get('low', 0)}")
        report.append(f"  🔵 信息: {self.stats.get('info', 0)}")
        report.append("")
        
        # 按类别统计
        report.append("📁 类别分布:")
        report.append("-" * 40)
        report.append(f"  安全: {self.stats.get('security', 0)}")
        report.append(f"  质量: {self.stats.get('quality', 0)}")
        report.append(f"  风格: {self.stats.get('style', 0)}")
        report.append("")
        
        # 详细问题列表
        if self.results and detailed:
            report.append("📋 详细问题列表:")
            report.append("-" * 40)
            
            # 按文件分组
            by_file = defaultdict(list)
            for r in self.results:
                by_file[r["file"]].append(r)
            
            for file_path, issues in sorted(by_file.items()):
                report.append(f"\n📁 {file_path}")
                
                for issue in issues:
                    severity_icon = {
                        "high": "🔴",
                        "medium": "🟡",
                        "low": "🟢",
                        "info": "🔵"
                    }.get(issue["severity"], "⚪")
                    
                    report.append(f"  {severity_icon} 第{issue['line']}行: [{issue['rule_id']}] {issue['message']}")
        
        report.append("")
        report.append("=" * 60)
        report.append("💡 提示: 使用 'devmind review --file <path>' 获取AI代码审查")
        report.append("=" * 60)
        
        return "\n".join(report)
    
    def get_results(self) -> List[Dict]:
        """获取扫描结果"""
        return self.results
    
    def export_json(self, output_path: str) -> bool:
        """导出JSON格式结果"""
        import json
        
        try:
            with open(output_path, "w", encoding="utf-8") as f:
                json.dump({
                    "summary": dict(self.stats),
                    "results": self.results
                }, f, indent=2, ensure_ascii=False)
            return True
        except Exception:
            return False
