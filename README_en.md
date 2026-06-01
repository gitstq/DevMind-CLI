# 🧠 DevMind-CLI

> Developer Intelligence Assistant powered by **GLM-5.1** | 基于 GLM-5.1 的开发者智能助手

[English](./README_en.md) | [简体中文](./README.md) | [繁體中文](./README_zh_tw.md)

---

<div align="center">

![Python Version](https://img.shields.io/badge/Python-3.8+-blue.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)
![Stars](https://img.shields.io/github/stars/gitstq/DevMind-CLI?style=flat)
![Forks](https://img.shields.io/github/forks/gitstq/DevMind-CLI?style=flat)

**🦞 Zero Dependencies | Lightweight | Ready to Use**

*DevMind-CLI is a developer intelligence assistant powered by GLM-5.1 LLM, providing code analysis, review, refactoring suggestions, and more.*

**[Demo](#-core-features)** ·
**[Quick Start](#-quick-start)** ·
**[Documentation](#-detailed-usage-guide)** ·
**[Contributing](./CONTRIBUTING.md)** ·
**[Changelog](./CHANGELOG.md)**

</div>

---

## 🎯 Introduction

### 🤔 What is this?

DevMind-CLI is a **command-line developer intelligence assistant** powered by **GLM-5.1** large language model. Unlike ordinary code completion tools, it's a developer companion that can **actively analyze code**, **discover potential issues**, and **provide intelligent suggestions**.

### 💡 What problems does it solve?

- 🔍 **Difficult code analysis** - Don't know where to start with unfamiliar code? DevMind helps you understand quickly
- 🐛 **Hard to locate bugs** - Code running with errors? Intelligent debugging suggestions help you locate issues fast
- 🔧 **No idea how to refactor** - Want to optimize code structure? Professional refactoring plans for reference
- 📚 **Missing documentation** - Lack of comments and docs? Auto-generate standardized code documentation
- 🛡️ **Security concerns** - Worried about code security? Automatic security vulnerability scanning

### 🚀 Key Differentiators

| Feature | DevMind-CLI | Other Tools |
|---------|-------------|-------------|
| 🤖 Powered by | GLM-5.1 (Long-horizon) | GPT/Claude |
| 📦 Dependencies | **Zero** | Multiple packages |
| ⚡ Startup | **Instant** | Loading time |
| 🔧 Functionality | Analysis+Review+Refactor | Code completion only |
| 💾 Memory | Project learning support | None |

### 🐉 Design Philosophy

> "Not waiting for questions, but actively helping"

DevMind follows the **OpenClaw** spirit, focusing on **proactive intelligence**:
- Not a passive Q&A machine
- Can actively scan projects for issues
- Learns developer habits across projects for personalized suggestions

---

## ✨ Core Features

### 📊 Code Analyzer
- 🔎 Multi-language code structure analysis
- 📈 Code statistics (files, lines, language distribution)
- 🎯 Complexity assessment
- 💾 Project memory learning

### 🔍 Code Reviewer
- 🛡️ Security vulnerability detection
- ⚡ Performance issue identification
- 🎨 Code style checking
- 📝 Best practice suggestions

### 🔧 Refactor Advisor
- 💡 Intelligent refactoring plans
- 📋 Problematic code location
- ✅ Before/after refactoring comparison
- 💬 Refactoring rationale

### 📚 Documentation Generator
- 📄 Auto-generate docstrings
- 📖 Markdown documentation
- 🌐 Multi-language support
- 🎯 Usage example generation

### 🔮 Interactive TUI
- 💬 Natural language conversation
- 📝 Code snippet analysis
- ⚡ Quick command execution
- 📜 History viewing

---

## 🚀 Quick Start

### 📋 Requirements

- **Python**: 3.8 or higher
- **Network**: Access to GLM-5.1 API (or configure local model)
- **OS**: Windows / macOS / Linux

### ⚡ Installation

#### Method 1: pip install (Recommended)

```bash
pip install devmind-cli
```

#### Method 2: From source

```bash
# Clone repository
git clone https://github.com/gitstq/DevMind-CLI.git
cd DevMind-CLI

# Install
pip install -e .
```

#### Method 3: Direct run

```bash
# Download project
git clone https://github.com/gitstq/DevMind-CLI.git
cd DevMind-CLI

# Run directly
python main.py --help
```

### 🔑 Configure API Key

#### Environment variable

```bash
# Linux/macOS
export GLM_API_KEY="your-api-key"

# Windows
set GLM_API_KEY=your-api-key
```

#### Command line argument

```bash
devmind --api-key "your-api-key" chat
```

### 🎯 Quick Usage

#### 1. Analyze code directory

```bash
devmind analyze ./src
```

#### 2. Review code file

```bash
devmind review -f main.py
```

#### 3. Get refactoring suggestions

```bash
devmind refactor -f utils.py --function process_data
```

#### 4. Generate code documentation

```bash
devmind docgen -f module.py -o README.md
```

#### 5. Scan for security issues

```bash
devmind scan --path ./project --report
```

#### 6. Start interactive chat

```bash
devmind chat
```

### 📖 Detailed Usage Guide

#### Command Line Arguments

```bash
# Global arguments
--api-key       GLM-5.1 API key
--api-url       API URL (default: https://open.bigmodel.cn/api/paas/v4)
--model         Model to use (default: glm-5-0520)
--offline       Offline mode (basic features only)
--verbose       Verbose output mode

# analyze command
devmind analyze <path> [options]
  -r, --recursive    Recursively analyze subdirectories
  -o, --output       Output file path
  --format           Output format (text/json/markdown)

# review command
devmind review [options]
  -f, --file          Review single file
  -d, --dir           Review directory
  --strict            Strict review mode
  -o, --output        Output file path

# refactor command
devmind refactor -f <file> [options]
  --function          Specify function name
  --line-start        Start line number
  --line-end          End line number

# docgen command
devmind docgen [options]
  -m, --module        Module name
  -f, --file          File path
  -o, --output        Output file path
  --format            Output format (markdown/html/rst)

# scan command
devmind scan -p <path> [options]
  --exclude           Excluded directories
  -r, --report        Generate report
```

#### TUI Interactive Mode

```bash
# Start TUI
devmind chat

# Available commands in TUI
analyze <path>   - Analyze code
scan <path>      - Scan project
!command         - Execute system command
history          - View history
clear            - Clear screen
help             - Show help
exit             - Exit
```

---

## 💡 Design Philosophy & Roadmap

### 🎨 Design Principles

1. **Zero dependencies** - Core functionality uses only Python standard library
2. **Lightweight & efficient** - No extra dependencies needed, ready to use
3. **Modular architecture** - Independent core modules for easy extension
4. **Privacy-first** - Local mode supported, data stays local

### 🔧 Tech Stack

| Component | Choice | Reason |
|-----------|--------|--------|
| Language | Python 3.8+ | Rich ecosystem, easy to extend |
| LLM Interface | REST API | Universal, easy to integrate |
| TUI | Standard library | Zero dependencies, fast response |
| Config | Env vars + files | Flexible, secure |

### 📅 Roadmap

#### v1.1.0 (Planned)
- [ ] MCP protocol support
- [ ] Local GGUF model support
- [ ] Enhanced TUI (using Rich)
- [ ] Multi-model support

#### v1.2.0 (Planned)
- [ ] Git integration
- [ ] CI/CD integration
- [ ] Web UI
- [ ] VSCode plugin

#### v2.0.0 (Long-term)
- [ ] Multi-agent collaboration
- [ ] Project-level code understanding
- [ ] Auto test generation
- [ ] Smart code review team

---

## 📦 Packaging & Deployment

### 🐧 Linux/macOS

```bash
# After installation
devmind --help

# Or run directly
python main.py --help
```

### 🪟 Windows

```powershell
# CMD or PowerShell
python main.py --help

# Or after installation
devmind --help
```

### 🐳 Docker (Optional)

```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY . /app
RUN pip install -e .
CMD ["devmind", "chat"]
```

### ☁️ CI/CD Integration

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

## 📄 License

This project is open-source under the **MIT License**.

See [LICENSE](./LICENSE) for details.

---

## 🙏 Acknowledgments

- **[GLM-5.1](https://github.com/zai-org/GLM-5)** - Zhipu AI Long-horizon LLM
- **[OpenClaw](https://github.com/nicktorn89/openclaw)** - AI Agent design inspiration
- All contributors and users

---

<div align="center">

**⭐ If this project helps you, please give us a Star!**

**📬 For issues or suggestions, welcome to submit Issue or PR**

**🦞</ Developer Intelligence Companion - DevMind-CLI**

</div>
