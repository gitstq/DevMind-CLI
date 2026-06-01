#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
DevMind-CLI 测试套件
"""

import sys
import os

# 添加项目根目录到路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.llm import GLMClient
from core.analyzer import CodeAnalyzer, PythonAnalyzer
from core.memory import ProjectMemory
from core.scanner import CodeScanner
from tools.reviewer import CodeReviewer
from tools.refactor import RefactorAdvisor
from tools.docgen import DocGenerator

import pytest


class TestGLMClient:
    """测试GLM客户端"""
    
    def test_init_without_api_key(self):
        """测试无API密钥初始化"""
        client = GLMClient()
        assert client.api_key is None
        assert client.model == "glm-5-0520"
    
    def test_init_with_api_key(self):
        """测试带API密钥初始化"""
        client = GLMClient(api_key="test-key")
        assert client.api_key == "test-key"
    
    def test_offline_response(self):
        """测试离线响应"""
        client = GLMClient()
        response = client._offline_response("测试消息")
        assert "离线模式" in response


class TestCodeAnalyzer:
    """测试代码分析器"""
    
    def test_init(self):
        """测试初始化"""
        client = GLMClient()
        analyzer = CodeAnalyzer(client)
        assert analyzer.llm is not None
    
    def test_detect_language(self):
        """测试语言检测"""
        analyzer = CodeAnalyzer(None)
        
        assert analyzer._detect_language("test.py") == "python"
        assert analyzer._detect_language("test.js") == "javascript"
        assert analyzer._detect_language("test.go") == "go"
        assert analyzer._detect_language("test.java") == "java"
        assert analyzer._detect_language("test.rs") == "rust"


class TestPythonAnalyzer:
    """测试Python专用分析器"""
    
    def test_parse_valid_code(self):
        """测试解析有效代码"""
        analyzer = PythonAnalyzer()
        code = """
def hello():
    print("Hello, World!")

class MyClass:
    def __init__(self):
        pass
"""
        assert analyzer.parse(code) is True
    
    def test_parse_invalid_code(self):
        """测试解析无效代码"""
        analyzer = PythonAnalyzer()
        code = "def hello(:"
        assert analyzer.parse(code) is False
    
    def test_get_functions(self):
        """测试获取函数"""
        analyzer = PythonAnalyzer()
        code = """
def func1():
    pass

async def func2():
    pass
"""
        analyzer.parse(code)
        functions = analyzer.get_functions()
        assert len(functions) == 2
        assert functions[0]["name"] == "func1"
        assert functions[1]["name"] == "func2"
        assert functions[1]["is_async"] is True
    
    def test_get_classes(self):
        """测试获取类"""
        analyzer = PythonAnalyzer()
        code = """
class MyClass:
    def method1(self):
        pass
"""
        analyzer.parse(code)
        classes = analyzer.get_classes()
        assert len(classes) == 1
        assert classes[0]["name"] == "MyClass"


class TestProjectMemory:
    """测试项目记忆"""
    
    def test_init(self, tmp_path):
        """测试初始化"""
        memory = ProjectMemory(str(tmp_path))
        assert memory.project_path == tmp_path
        assert "code_patterns" in memory.memory
    
    def test_learn_pattern(self, tmp_path):
        """测试学习模式"""
        memory = ProjectMemory(str(tmp_path))
        memory.learn_pattern("test", "context", "result")
        assert len(memory.memory["code_patterns"]) == 1
    
    def test_set_context(self, tmp_path):
        """测试设置上下文"""
        memory = ProjectMemory(str(tmp_path))
        memory.set_context("key", "value")
        assert memory.get_context("key") == "value"
    
    def test_add_insight(self, tmp_path):
        """测试添加洞察"""
        memory = ProjectMemory(str(tmp_path))
        memory.add_insight("test insight", "test")
        assert len(memory.memory["insights"]) == 1
    
    def test_statistics(self, tmp_path):
        """测试统计信息"""
        memory = ProjectMemory(str(tmp_path))
        memory.learn_pattern("test", "context", "result")
        stats = memory.get_statistics()
        assert stats["total_patterns"] == 1
        assert stats["total_insights"] == 0


class TestCodeScanner:
    """测试代码扫描器"""
    
    def test_init(self):
        """测试初始化"""
        scanner = CodeScanner()
        assert scanner.results == []
        assert scanner.stats == {}
    
    def test_supported_extensions(self):
        """测试支持的文件扩展名"""
        assert ".py" in CodeScanner.SUPPORTED_EXTENSIONS
        assert ".js" in CodeScanner.SUPPORTED_EXTENSIONS
        assert ".go" in CodeScanner.SUPPORTED_EXTENSIONS


class TestCodeReviewer:
    """测试代码审查器"""
    
    def test_init(self):
        """测试初始化"""
        client = GLMClient()
        reviewer = CodeReviewer(client)
        assert reviewer.llm is not None
    
    def test_detect_language(self):
        """测试语言检测"""
        reviewer = CodeReviewer(None)
        assert reviewer._detect_language("test.py") == "python"
        assert reviewer._detect_language("test.js") == "javascript"


class TestRefactorAdvisor:
    """测试重构顾问"""
    
    def test_init(self):
        """测试初始化"""
        client = GLMClient()
        advisor = RefactorAdvisor(client)
        assert advisor.llm is not None


class TestDocGenerator:
    """测试文档生成器"""
    
    def test_init(self):
        """测试初始化"""
        client = GLMClient()
        generator = DocGenerator(client)
        assert generator.llm is not None


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
