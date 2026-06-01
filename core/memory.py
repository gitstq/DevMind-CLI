#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
DevMind-CLI 核心模块 - 项目记忆管理
"""

import json
import os
from pathlib import Path
from typing import Dict, List, Optional, Any
from datetime import datetime


class ProjectMemory:
    """项目记忆管理器"""
    
    def __init__(self, project_path: Optional[str] = None):
        """
        初始化记忆管理器
        
        Args:
            project_path: 项目路径
        """
        self.project_path = Path(project_path) if project_path else Path.cwd()
        self.memory_dir = self.project_path / ".devmind"
        self.memory_file = self.memory_dir / "memory.json"
        self.stats_file = self.memory_dir / "stats.json"
        
        self._ensure_memory_dir()
        self.memory = self._load_memory()
    
    def _ensure_memory_dir(self) -> None:
        """确保记忆目录存在"""
        self.memory_dir.mkdir(parents=True, exist_ok=True)
    
    def _load_memory(self) -> Dict:
        """加载记忆数据"""
        if self.memory_file.exists():
            try:
                with open(self.memory_file, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception:
                pass
        
        return {
            "version": "1.0",
            "created_at": datetime.now().isoformat(),
            "last_updated": datetime.now().isoformat(),
            "code_patterns": [],
            "custom_rules": [],
            "context": {},
            "insights": []
        }
    
    def _save_memory(self) -> None:
        """保存记忆数据"""
        self.memory["last_updated"] = datetime.now().isoformat()
        
        with open(self.memory_file, "w", encoding="utf-8") as f:
            json.dump(self.memory, f, indent=2, ensure_ascii=False)
    
    def learn_pattern(self, pattern: str, context: str, result: str) -> None:
        """
        学习代码模式
        
        Args:
            pattern: 代码模式
            context: 上下文
            result: 处理结果
        """
        entry = {
            "pattern": pattern,
            "context": context,
            "result": result,
            "learned_at": datetime.now().isoformat(),
            "use_count": 0,
            "success_rate": 1.0
        }
        
        self.memory["code_patterns"].append(entry)
        self._save_memory()
    
    def get_context(self, key: str) -> Optional[Any]:
        """
        获取上下文信息
        
        Args:
            key: 上下文键
            
        Returns:
            上下文值
        """
        return self.memory.get("context", {}).get(key)
    
    def set_context(self, key: str, value: Any) -> None:
        """
        设置上下文信息
        
        Args:
            key: 上下文键
            value: 上下文值
        """
        if "context" not in self.memory:
            self.memory["context"] = {}
        
        self.memory["context"][key] = value
        self._save_memory()
    
    def add_insight(self, insight: str, category: str = "general") -> None:
        """
        添加洞察
        
        Args:
            insight: 洞察内容
            category: 分类
        """
        entry = {
            "category": category,
            "content": insight,
            "created_at": datetime.now().isoformat()
        }
        
        self.memory["insights"].append(entry)
        self._save_memory()
    
    def get_recent_insights(self, limit: int = 10) -> List[Dict]:
        """
        获取最近的洞察
        
        Args:
            limit: 数量限制
            
        Returns:
            洞察列表
        """
        insights = self.memory.get("insights", [])
        return sorted(insights, key=lambda x: x.get("created_at", ""), reverse=True)[:limit]
    
    def search_patterns(self, keyword: str) -> List[Dict]:
        """
        搜索代码模式
        
        Args:
            keyword: 关键词
            
        Returns:
            匹配的模式列表
        """
        results = []
        
        for pattern in self.memory.get("code_patterns", []):
            if keyword.lower() in pattern.get("pattern", "").lower():
                results.append(pattern)
        
        return results
    
    def increment_pattern_usage(self, pattern_idx: int) -> None:
        """
        增加模式使用次数
        
        Args:
            pattern_idx: 模式索引
        """
        patterns = self.memory.get("code_patterns", [])
        
        if 0 <= pattern_idx < len(patterns):
            patterns[pattern_idx]["use_count"] += 1
            self._save_memory()
    
    def get_statistics(self) -> Dict:
        """
        获取统计信息
        
        Returns:
            统计字典
        """
        patterns = self.memory.get("code_patterns", [])
        insights = self.memory.get("insights", [])
        
        return {
            "total_patterns": len(patterns),
            "total_insights": len(insights),
            "total_uses": sum(p.get("use_count", 0) for p in patterns),
            "context_keys": list(self.memory.get("context", {}).keys()),
            "last_updated": self.memory.get("last_updated"),
            "created_at": self.memory.get("created_at")
        }
    
    def export_memory(self, output_path: str) -> bool:
        """
        导出记忆
        
        Args:
            output_path: 输出路径
            
        Returns:
            是否成功
        """
        try:
            with open(output_path, "w", encoding="utf-8") as f:
                json.dump(self.memory, f, indent=2, ensure_ascii=False)
            return True
        except Exception:
            return False
    
    def import_memory(self, input_path: str) -> bool:
        """
        导入记忆
        
        Args:
            input_path: 输入路径
            
        Returns:
            是否成功
        """
        try:
            with open(input_path, "r", encoding="utf-8") as f:
                imported = json.load(f)
            
            self.memory = imported
            self._save_memory()
            return True
        except Exception:
            return False
    
    def clear(self) -> None:
        """清空记忆"""
        self.memory = {
            "version": "1.0",
            "created_at": datetime.now().isoformat(),
            "last_updated": datetime.now().isoformat(),
            "code_patterns": [],
            "custom_rules": [],
            "context": {},
            "insights": []
        }
        self._save_memory()
    
    def __repr__(self) -> str:
        """字符串表示"""
        stats = self.get_statistics()
        return f"ProjectMemory(project={self.project_path}, patterns={stats['total_patterns']}, insights={stats['total_insights']})"
