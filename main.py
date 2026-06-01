#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
DevMind-CLI - 基于GLM-5.1的开发者智能助手
DevMind-CLI - Developer Intelligence Assistant powered by GLM-5.1

@author: gitstq
@version: 1.0.0
@license: MIT
"""

import sys
import argparse
from pathlib import Path
from typing import Optional

# 版本信息
__version__ = "1.0.0"
__author__ = "gitstq"
__license__ = "MIT"

# 导入核心模块
from core.llm import GLMClient
from core.analyzer import CodeAnalyzer
from core.memory import ProjectMemory
from core.scanner import CodeScanner
from tools.reviewer import CodeReviewer
from tools.refactor import RefactorAdvisor
from tools.docgen import DocGenerator
from ui.tui import DevMindTUI


def create_parser() -> argparse.ArgumentParser:
    """创建命令行参数解析器"""
    parser = argparse.ArgumentParser(
        prog="devmind",
        description="🧠 DevMind-CLI - 基于GLM-5.1的开发者智能助手",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例用法:
  devmind analyze ./src              # 分析代码目录
  devmind review --file main.py       # 审查代码文件
  devmind refactor --function foo     # 获取重构建议
  devmind docgen --module utils       # 生成文档
  devmind scan --path ./project       # 扫描项目
  devmind chat                        # 启动交互式聊天

更多信息请访问: https://github.com/gitstq/DevMind-CLI
        """
    )
    
    # 主命令
    subparsers = parser.add_subparsers(dest="command", help="可用命令")
    
    # 全局参数
    parser.add_argument("--version", action="version", version=f"%(prog)s {__version__}")
    parser.add_argument("--api-key", type=str, help="GLM-5.1 API密钥")
    parser.add_argument("--api-url", type=str, default="https://open.bigmodel.cn/api/paas/v4",
                        help="GLM API地址")
    parser.add_argument("--model", type=str, default="glm-5-0520", help="使用的模型")
    parser.add_argument("--offline", action="store_true", help="离线模式（仅基础功能）")
    parser.add_argument("--verbose", "-v", action="store_true", help="详细输出")
    parser.add_argument("--config", type=str, help="配置文件路径")
    
    # analyze 命令
    analyze_parser = subparsers.add_parser("analyze", help="分析代码")
    analyze_parser.add_argument("path", type=str, help="代码路径")
    analyze_parser.add_argument("--recursive", "-r", action="store_true", help="递归分析")
    analyze_parser.add_argument("--output", "-o", type=str, help="输出文件路径")
    analyze_parser.add_argument("--format", choices=["text", "json", "markdown"], 
                                default="text", help="输出格式")
    
    # review 命令
    review_parser = subparsers.add_parser("review", help="代码审查")
    review_parser.add_argument("--file", "-f", type=str, help="单个文件")
    review_parser.add_argument("--dir", "-d", type=str, help="目录")
    review_parser.add_argument("--strict", action="store_true", help="严格模式")
    review_parser.add_argument("--output", "-o", type=str, help="输出文件")
    
    # refactor 命令
    refactor_parser = subparsers.add_parser("refactor", help="重构建议")
    refactor_parser.add_argument("--file", "-f", required=True, help="代码文件")
    refactor_parser.add_argument("--function", type=str, help="指定函数名")
    refactor_parser.add_argument("--line-start", type=int, help="起始行号")
    refactor_parser.add_argument("--line-end", type=int, help="结束行号")
    
    # docgen 命令
    docgen_parser = subparsers.add_parser("docgen", help="生成文档")
    docgen_parser.add_argument("--module", "-m", type=str, help="模块名")
    docgen_parser.add_argument("--file", "-f", type=str, help="文件路径")
    docgen_parser.add_argument("--output", "-o", type=str, help="输出文件")
    docgen_parser.add_argument("--format", choices=["markdown", "html", "rst"], 
                               default="markdown", help="输出格式")
    
    # scan 命令
    scan_parser = subparsers.add_parser("scan", help="扫描项目")
    scan_parser.add_argument("--path", "-p", required=True, help="项目路径")
    scan_parser.add_argument("--exclude", nargs="+", help="排除的目录")
    scan_parser.add_argument("--report", "-r", action="store_true", help="生成报告")
    
    # chat 命令
    chat_parser = subparsers.add_parser("chat", help="交互式聊天")
    chat_parser.add_argument("--context", "-c", type=str, help="上下文目录")
    
    return parser


def main():
    """主入口函数"""
    parser = create_parser()
    args = parser.parse_args()
    
    # 如果没有命令，显示帮助
    if not args.command:
        parser.print_help()
        print("\n💡 提示: 使用 'devmind <command> --help' 查看命令详细帮助")
        return 0
    
    # 初始化客户端
    client = GLMClient(
        api_key=args.api_key,
        api_url=args.api_url,
        model=args.model,
        verbose=args.verbose
    )
    
    # 根据命令执行相应操作
    try:
        if args.command == "analyze":
            analyzer = CodeAnalyzer(client)
            result = analyzer.analyze(
                path=args.path,
                recursive=args.recursive,
                output=args.output,
                format=args.format
            )
            print(result)
            
        elif args.command == "review":
            reviewer = CodeReviewer(client)
            result = reviewer.review(
                file_path=args.file,
                dir_path=args.dir,
                strict=args.strict,
                output=args.output
            )
            print(result)
            
        elif args.command == "refactor":
            advisor = RefactorAdvisor(client)
            result = advisor.get_suggestions(
                file_path=args.file,
                function_name=args.function,
                line_start=args.line_start,
                line_end=args.line_end
            )
            print(result)
            
        elif args.command == "docgen":
            generator = DocGenerator(client)
            result = generator.generate(
                module_name=args.module,
                file_path=args.file,
                output=args.output,
                format=args.format
            )
            print(result)
            
        elif args.command == "scan":
            scanner = CodeScanner(client)
            result = scanner.scan(
                path=args.path,
                exclude=args.exclude or [],
                report=args.report
            )
            print(result)
            
        elif args.command == "chat":
            tui = DevMindTUI(client, context_path=args.context)
            tui.run()
            
    except KeyboardInterrupt:
        print("\n👋 已退出 DevMind-CLI")
        return 0
    except Exception as e:
        print(f"❌ 错误: {e}", file=sys.stderr)
        if args.verbose:
            import traceback
            traceback.print_exc()
        return 1
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
