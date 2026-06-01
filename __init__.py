#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
DevMind-CLI - 基于GLM-5.1的开发者智能助手
DevMind-CLI - Developer Intelligence Assistant powered by GLM-5.1

A lightweight, zero-dependency CLI tool for code analysis, review, and AI-powered suggestions.
"""

__version__ = "1.0.0"
__author__ = "gitstq"
__license__ = "MIT"
__email__ = "gitstq@github.com"

from core.llm import GLMClient
from core.analyzer import CodeAnalyzer
from core.memory import ProjectMemory
from core.scanner import CodeScanner
from tools.reviewer import CodeReviewer
from tools.refactor import RefactorAdvisor
from tools.docgen import DocGenerator
from ui.tui import DevMindTUI

__all__ = [
    "GLMClient",
    "CodeAnalyzer",
    "ProjectMemory",
    "CodeScanner",
    "CodeReviewer",
    "RefactorAdvisor",
    "DocGenerator",
    "DevMindTUI",
]
