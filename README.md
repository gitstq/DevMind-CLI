# 🧠 DevMind-CLI

> 基于 **GLM-5.1** 的开发者智能助手 | Developer Intelligence Assistant powered by GLM-5.1

[English](./README_en.md) | [简体中文](./README.md) | [繁體中文](./README_zh_tw.md)

---

<div align="center">

![Python Version](https://img.shields.io/badge/Python-3.8+-blue.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)
![Stars](https://img.shields.io/github/stars/gitstq/DevMind-CLI?style=flat)
![Forks](https://img.shields.io/github/forks/gitstq/DevMind-CLI?style=flat)

**🦞 零依赖 | 轻量级 | 开箱即用**

*DevMind-CLI 是一个基于 GLM-5.1 大模型的开发者智能助手，提供代码分析、审查、重构建议等功能。*

**[功能演示](#-核心功能)** ·
**[快速开始](#-快速开始)** ·
**[详细文档](#-详细使用指南)** ·
**[贡献指南](./CONTRIBUTING.md)** ·
**[更新日志](./CHANGELOG.md)**

</div>

---

## 🎯 项目介绍

### 🤔 这是什么？

DevMind-CLI 是一款**命令行开发者智能助手**，由 **GLM-5.1** 大模型驱动。它不是普通的代码补全工具，而是一个能够**主动分析代码**、**发现潜在问题**、**提供智能建议**的开发者伙伴。

### 💡 解决什么问题？

- 🔍 **代码分析困难** - 面对陌生代码无从下手？DevMind帮你快速理解
- 🐛 **Bug 难以定位** - 代码运行报错？智能调试建议助你快速定位
- 🔧 **重构无从下手** - 想要优化代码结构？专业重构方案供参考
- 📚 **文档缺失** - 缺少注释和文档？自动生成规范的代码文档
- 🛡️ **安全隐患** - 担心代码安全问题？自动扫描安全漏洞

### 🚀 自研差异化亮点

| 特性 | DevMind-CLI | 其他工具 |
|------|-------------|----------|
| 🤖 驱动模型 | GLM-5.1（长程任务） | GPT/Claude |
| 📦 依赖数量 | **零依赖** | 需要安装多个包 |
| ⚡ 启动速度 | **即时响应** | 依赖加载时间 |
| 🔧 功能范围 | 代码分析+审查+重构 | 仅代码补全 |
| 💾 记忆功能 | 支持项目记忆学习 | 无 |

### 🐉 设计理念

> "不是等待询问，而是主动帮助"

DevMind 遵循 **OpenClaw** 精神，主打**主动式智能**：
- 不是被动的问答机器
- 能够主动扫描项目发现问题
- 跨项目学习开发者习惯，提供个性化建议

---

## ✨ 核心功能

### 📊 代码分析器
- 🔎 多语言代码结构分析
- 📈 代码统计（文件数、行数、语言分布）
- 🎯 复杂度评估
- 💾 项目记忆学习

### 🔍 代码审查器
- 🛡️ 安全漏洞检测
- ⚡ 性能问题识别
- 🎨 代码风格检查
- 📝 最佳实践建议

### 🔧 重构顾问
- 💡 智能重构方案
- 📋 问题代码定位
- ✅ 重构前后对比
- 💬 重构理由说明

### 📚 文档生成器
- 📄 自动生成 docstring
- 📖 Markdown 文档
- 🌐 多语言支持
- 🎯 使用示例生成

### 🔮 交互式 TUI
- 💬 自然语言对话
- 📝 代码片段分析
- ⚡ 快速命令执行
- 📜 历史记录查看

---

## 🚀 快速开始

### 📋 环境要求

- **Python**: 3.8 或更高版本
- **网络**: 需要访问 GLM-5.1 API（或配置本地模型）
- **系统**: Windows / macOS / Linux

### ⚡ 安装方式

#### 方式一：pip 安装（推荐）

```bash
pip install devmind-cli
```

#### 方式二：从源码安装

```bash
# 克隆仓库
git clone https://github.com/gitstq/DevMind-CLI.git
cd DevMind-CLI

# 安装
pip install -e .
```

#### 方式三：直接运行

```bash
# 下载项目
git clone https://github.com/gitstq/DevMind-CLI.git
cd DevMind-CLI

# 直接运行
python main.py --help
```

### 🔑 配置 API 密钥

#### 环境变量方式

```bash
# Linux/macOS
export GLM_API_KEY="你的API密钥"

# Windows
set GLM_API_KEY=你的API密钥
```

#### 命令行参数方式

```bash
devmind --api-key "你的API密钥" chat
```

### 🎯 快速使用

#### 1. 分析代码目录

```bash
devmind analyze ./src
```

#### 2. 审查代码文件

```bash
devmind review -f main.py
```

#### 3. 获取重构建议

```bash
devmind refactor -f utils.py --function process_data
```

#### 4. 生成代码文档

```bash
devmind docgen -f module.py -o README.md
```

#### 5. 扫描安全问题

```bash
devmind scan --path ./project --report
```

#### 6. 启动交互式聊天

```bash
devmind chat
```

### 📖 详细使用指南

#### 命令行参数说明

```bash
# 全局参数
--api-key       GLM-5.1 API密钥
--api-url       API地址（默认：https://open.bigmodel.cn/api/paas/v4）
--model         使用的模型（默认：glm-5-0520）
--offline       离线模式（仅基础功能）
--verbose       详细输出模式

# analyze 命令
devmind analyze <path> [选项]
  -r, --recursive    递归分析子目录
  -o, --output       输出文件路径
  --format           输出格式（text/json/markdown）

# review 命令
devmind review [选项]
  -f, --file         审查单个文件
  -d, --dir          审查目录
  --strict           严格审查模式
  -o, --output       输出文件路径

# refactor 命令
devmind refactor -f <file> [选项]
  --function         指定函数名
  --line-start       起始行号
  --line-end         结束行号

# docgen 命令
devmind docgen [选项]
  -m, --module       模块名
  -f, --file         文件路径
  -o, --output       输出文件路径
  --format           输出格式（markdown/html/rst）

# scan 命令
devmind scan -p <path> [选项]
  --exclude          排除的目录
  -r, --report       生成报告
```

#### TUI 交互模式

```bash
# 启动 TUI
devmind chat

# 在 TUI 中的可用命令
analyze <path>   - 分析代码
scan <path>      - 扫描项目
!命令            - 执行系统命令
history          - 查看历史
clear            - 清屏
help             - 显示帮助
exit             - 退出
```

---

## 💡 设计思路与迭代规划

### 🎨 设计理念

1. **零依赖设计** - 核心功能仅使用 Python 标准库，降低使用门槛
2. **轻量高效** - 无需安装额外依赖，下载即用
3. **模块化架构** - 核心模块独立，方便扩展和定制
4. **隐私优先** - 支持本地模式，数据不上传云端

### 🔧 技术选型

| 组件 | 技术选型 | 理由 |
|------|----------|------|
| 编程语言 | Python 3.8+ | 生态丰富、易于扩展 |
| LLM 接口 | REST API | 通用性强、易于集成 |
| TUI | 标准库 | 零依赖、快速响应 |
| 配置管理 | 环境变量 + 文件 | 灵活、安全 |

### 📅 迭代计划

#### v1.1.0（规划中）
- [ ] MCP 协议支持
- [ ] 支持本地 GGUF 模型
- [ ] 增强的 TUI 界面（使用 Rich）
- [ ] 多模型支持

#### v1.2.0（规划中）
- [ ] Git 集成
- [ ] CI/CD 集成
- [ ] Web UI
- [ ] VSCode 插件

#### v2.0.0（远期规划）
- [ ] 多智能体协作
- [ ] 项目级代码理解
- [ ] 自动测试生成
- [ ] 智能代码审查团队

---

## 📦 打包与部署

### 🐧 Linux/macOS

```bash
# 安装后直接使用
devmind --help

# 或直接运行
python main.py --help
```

### 🪟 Windows

```powershell
# CMD 或 PowerShell
python main.py --help

# 或安装后
devmind --help
```

### 🐳 Docker（可选）

```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY . /app
RUN pip install -e .
CMD ["devmind", "chat"]
```

### ☁️ CI/CD 集成

#### GitHub Actions

```yaml
- name: Run DevMind Code Review
  run: |
    pip install devmind-cli
    devmind review -f ${{ matrix.file }} --strict
  env:
    GLM_API_KEY: ${{ secrets.GLM_API_KEY }}
```

---

## 📄 开源协议

本项目采用 **MIT 许可证**开源。

详细内容请查看 [LICENSE](./LICENSE) 文件。

---

## 🙏 致谢

- **[GLM-5.1](https://github.com/zai-org/GLM-5)** - 智谱AI长程任务大模型
- **[OpenClaw](https://github.com/nicktorn89/openclaw)** - AI Agent 设计灵感
- 所有贡献者和用户

---

<div align="center">

**⭐ 如果这个项目对您有帮助，请给我们一个 Star！**

**📬 如有问题或建议，欢迎提交 Issue 或 PR**

**🦞</ 开发者智能伙伴 - DevMind-CLI**

</div>
