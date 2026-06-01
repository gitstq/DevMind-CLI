#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
DevMind-CLI UI模块 - 交互式TUI界面
"""

import sys
import os
from typing import Optional, List, Dict
from pathlib import Path


class DevMindTUI:
    """交互式TUI界面"""
    
    # 颜色定义
    COLORS = {
        "header": "\033[1;36m",      # 青色
        "success": "\033[1;32m",     # 绿色
        "error": "\033[1;31m",       # 红色
        "warning": "\033[1;33m",     # 黄色
        "info": "\033[1;34m",        # 蓝色
        "prompt": "\033[1;35m",      # 紫色
        "reset": "\033[0m"
    }
    
    def __init__(self, llm_client, context_path: Optional[str] = None):
        """
        初始化TUI
        
        Args:
            llm_client: LLM客户端
            context_path: 上下文目录
        """
        self.llm = llm_client
        self.context_path = context_path
        self.history: List[Dict] = []
        self.system_prompt = self._get_system_prompt()
    
    def _get_system_prompt(self) -> str:
        """获取系统提示词"""
        return """你是一个专业的代码智能助手，名叫DevMind。

你的能力包括：
- 📝 代码分析与解释
- 🔍 Bug查找与调试建议
- 🔧 重构方案提供
- 📚 文档生成
- 💡 最佳实践建议
- 🛡️ 安全问题检测

请用简洁、专业的方式回答。如果需要查看代码，请告诉用户具体路径。"""
    
    def run(self) -> None:
        """运行TUI"""
        self._print_banner()
        self._print_help()
        
        # 主循环
        while True:
            try:
                user_input = input(f"\n{self.COLORS['prompt']}DevMind>{self.COLORS['reset']} ").strip()
                
                if not user_input:
                    continue
                
                # 处理命令
                if user_input.lower() in ["exit", "quit", "q"]:
                    self._print_exit()
                    break
                elif user_input.lower() in ["help", "h", "?"]:
                    self._print_help()
                elif user_input.lower() == "clear":
                    self._clear_screen()
                elif user_input.lower() == "history":
                    self._print_history()
                elif user_input.startswith("!"):
                    self._execute_command(user_input[1:])
                elif user_input.startswith("analyze "):
                    self._handle_analyze(user_input[8:])
                elif user_input.startswith("scan "):
                    self._handle_scan(user_input[5:])
                else:
                    self._chat(user_input)
                    
            except KeyboardInterrupt:
                print("\n")
                self._print_exit()
                break
            except EOFError:
                break
    
    def _print_banner(self) -> None:
        """打印横幅"""
        banner = f"""
{self.COLORS['header']}
╔═══════════════════════════════════════════════════════════╗
║                                                           ║
║   🧠 DevMind-CLI - 开发者智能助手                        ║
║   Powered by GLM-5.1                                      ║
║                                                           ║
║   输入 'help' 查看可用命令                                ║
║   输入 'exit' 退出                                        ║
║                                                           ║
╚═══════════════════════════════════════════════════════════╝
{self.COLORS['reset']}"""
        print(banner)
    
    def _print_help(self) -> None:
        """打印帮助"""
        help_text = f"""
{self.COLORS['info']}可用命令:{self.COLORS['reset']}

  {self.COLORS['success']}analyze <path>{self.COLORS['reset']}   - 分析代码文件或目录
  {self.COLORS['success']}scan <path>{self.COLORS['reset']}      - 扫描项目安全问题
  {self.COLORS['success']}!命令{self.COLORS['reset']}            - 执行系统命令
  {self.COLORS['success']}history{self.COLORS['reset']}          - 查看聊天历史
  {self.COLORS['success']}clear{self.COLORS['reset']}            - 清屏
  {self.COLORS['success']}help{self.COLORS['reset']}             - 显示帮助
  {self.COLORS['success']}exit{self.COLORS['reset']}             - 退出

{self.COLORS['info']}快捷提示:{self.COLORS['reset']}
  - 直接输入问题进行AI对话
  - 可以粘贴代码片段进行分析
  - 支持多行输入（Ctrl+D 结束）
"""
        print(help_text)
    
    def _print_exit(self) -> None:
        """打印退出信息"""
        print(f"{self.COLORS['info']}👋 再见！祝编码愉快！{self.COLORS['reset']}")
    
    def _clear_screen(self) -> None:
        """清屏"""
        os.system("cls" if os.name == "nt" else "clear")
        self._print_banner()
    
    def _print_history(self) -> None:
        """打印历史"""
        if not self.history:
            print(f"{self.COLORS['warning']}暂无历史记录{self.COLORS['reset']}")
            return
        
        print(f"\n{self.COLORS['info']}聊天历史:{self.COLORS['reset']}")
        print("-" * 50)
        
        for i, item in enumerate(self.history[-10:], 1):
            print(f"\n{i}. {self.COLORS['prompt']}你:{self.COLORS['reset']} {item['user'][:50]}...")
            print(f"   {self.COLORS['success']}DevMind:{self.COLORS['reset']} {item['assistant'][:50]}...")
        
        print("-" * 50)
    
    def _chat(self, user_input: str) -> None:
        """处理聊天"""
        print(f"\n{self.COLORS['info']}🤔 思考中...{self.COLORS['reset']}")
        
        messages = [
            {"role": "system", "content": self.system_prompt},
            {"role": "user", "content": user_input}
        ]
        
        try:
            response = self.llm.chat(messages)
            
            # 保存历史
            self.history.append({
                "user": user_input,
                "assistant": response
            })
            
            # 打印响应
            print(f"\n{self.COLORS['success']}DevMind:{self.COLORS['reset']}")
            print(response)
            
        except Exception as e:
            print(f"\n{self.COLORS['error']}❌ 错误: {str(e)}{self.COLORS['reset']}")
    
    def _execute_command(self, command: str) -> None:
        """执行系统命令"""
        try:
            import subprocess
            result = subprocess.run(
                command,
                shell=True,
                capture_output=True,
                text=True
            )
            
            if result.stdout:
                print(result.stdout)
            if result.stderr:
                print(f"{self.COLORS['error']}{result.stderr}{self.COLORS['reset']}")
                
        except Exception as e:
            print(f"{self.COLORS['error']}❌ 命令执行失败: {str(e)}{self.COLORS['reset']}")
    
    def _handle_analyze(self, path: str) -> None:
        """处理分析命令"""
        if not path:
            print(f"{self.COLORS['warning']}⚠️ 请指定路径{self.COLORS['reset']}")
            return
        
        from core.analyzer import CodeAnalyzer
        
        print(f"\n{self.COLORS['info']}🔍 正在分析...{self.COLORS['reset']}")
        
        analyzer = CodeAnalyzer(self.llm)
        result = analyzer.analyze(path)
        
        print(f"\n{result}")
    
    def _handle_scan(self, path: str) -> None:
        """处理扫描命令"""
        if not path:
            print(f"{self.COLORS['warning']}⚠️ 请指定路径{self.COLORS['reset']}")
            return
        
        from core.scanner import CodeScanner
        
        print(f"\n{self.COLORS['info']}🔍 正在扫描...{self.COLORS['reset']}")
        
        scanner = CodeScanner(self.llm)
        result = scanner.scan(path, report=True)
        
        print(f"\n{result}")


def run_tui(api_key: Optional[str] = None) -> None:
    """启动TUI"""
    from core.llm import GLMClient
    
    client = GLMClient(api_key=api_key)
    tui = DevMindTUI(client)
    tui.run()


if __name__ == "__main__":
    run_tui()
