# 🧠 DevMind-CLI

> 開發者智慧助手 | Developer Intelligence Assistant powered by **GLM-5.1**

[English](./README_en.md) | [简体中文](./README.md) | [繁體中文](./README_zh_tw.md)

---

<div align="center">

![Python Version](https://img.shields.io/badge/Python-3.8+-blue.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)
![Stars](https://img.shields.io/github/stars/gitstq/DevMind-CLI?style=flat)
![Forks](https://img.shields.io/github/forks/gitstq/DevMind-CLI?style=flat)

**🦞 零依賴 | 輕量級 | 開箱即用**

*DevMind-CLI 是一款由 GLM-5.1 大模型驅動的開發者智慧助手，提供程式碼分析、審查、重構建議等功能。*

**[功能展示](#-核心功能)** ·
**[快速開始](#-快速開始)** ·
**[詳細文檔](#-詳細使用指南)** ·
**[貢獻指南](./CONTRIBUTING.md)** ·
**[更新日誌](./CHANGELOG.md)**

</div>

---

## 🎯 專案介紹

### 🤔 這是什麼？

DevMind-CLI 是一款**命令列開發者智慧助手**，由 **GLM-5.1** 大模型驅動。它不是普通的程式碼補全工具，而是一個能夠**主動分析程式碼**、**發現潛在問題**、**提供智慧建議**的開發者夥伴。

### 💡 解決什麼問題？

- 🔍 **程式碼分析困難** - 面對陌生程式碼無從下手？DevMind幫你快速理解
- 🐛 **Bug 難以定位** - 程式碼運行報錯？智慧調試建議助你快速定位
- 🔧 **重構無從下手** - 想要優化程式碼結構？專業重構方案供參考
- 📚 **文檔缺失** - 缺少註釋和文檔？自動生成規範的程式碼文檔
- 🛡️ **安全隱患** - 擔心程式碼安全問題？自動掃描安全漏洞

### 🚀 自研差異化亮點

| 特性 | DevMind-CLI | 其他工具 |
|------|-------------|----------|
| 🤖 驅動模型 | GLM-5.1（長程任務） | GPT/Claude |
| 📦 依賴數量 | **零依賴** | 需要安裝多個包 |
| ⚡ 啟動速度 | **即時響應** | 依賴加載時間 |
| 🔧 功能範圍 | 程式碼分析+審查+重構 | 僅程式碼補全 |
| 💾 記憶功能 | 支持專案記憶學習 | 無 |

### 🐉 設計理念

> "不是等待詢問，而是主動幫助"

DevMind 遵循 **OpenClaw** 精神，主打**主動式智慧**：
- 不是被動的問答機器
- 能夠主動掃描專案發現問題
- 跨專案學習開發者習慣，提供個人化建議

---

## ✨ 核心功能

### 📊 程式碼分析器
- 🔎 多語言程式碼結構分析
- 📈 程式碼統計（檔案數、行數、語言分布）
- 🎯 複雜度評估
- 💾 專案記憶學習

### 🔍 程式碼審查器
- 🛡️ 安全漏洞檢測
- ⚡ 效能問題識別
- 🎨 程式碼風格檢查
- 📝 最佳實踐建議

### 🔧 重構顧問
- 💡 智慧重構方案
- 📋 問題程式碼定位
- ✅ 重構前後對比
- 💬 重構理由說明

### 📚 文檔生成器
- 📄 自動生成 docstring
- 📖 Markdown 文檔
- 🌐 多語言支持
- 🎯 使用範例生成

### 🔮 互動式 TUI
- 💬 自然語言對話
- 📝 程式碼片段分析
- ⚡ 快速命令執行
- 📜 歷史記錄查看

---

## 🚀 快速開始

### 📋 環境要求

- **Python**: 3.8 或更高版本
- **網路**: 需要訪問 GLM-5.1 API（或配置本地模型）
- **系統**: Windows / macOS / Linux

### ⚡ 安裝方式

#### 方式一：pip 安裝（推薦）

```bash
pip install devmind-cli
```

#### 方式二：從原始碼安裝

```bash
# 克隆倉庫
git clone https://github.com/gitstq/DevMind-CLI.git
cd DevMind-CLI

# 安裝
pip install -e .
```

#### 方式三：直接運行

```bash
# 下載專案
git clone https://github.com/gitstq/DevMind-CLI.git
cd DevMind-CLI

# 直接運行
python main.py --help
```

### 🔑 配置 API 金鑰

#### 環境變數方式

```bash
# Linux/macOS
export GLM_API_KEY="你的API金鑰"

# Windows
set GLM_API_KEY=你的API金鑰
```

#### 命令列參數方式

```bash
devmind --api-key "你的API金鑰" chat
```

### 🎯 快速使用

#### 1. 分析程式碼目錄

```bash
devmind analyze ./src
```

#### 2. 審查程式碼檔案

```bash
devmind review -f main.py
```

#### 3. 獲取重構建議

```bash
devmind refactor -f utils.py --function process_data
```

#### 4. 生成程式碼文檔

```bash
devmind docgen -f module.py -o README.md
```

#### 5. 掃描安全問題

```bash
devmind scan --path ./project --report
```

#### 6. 啟動互動式聊天

```bash
devmind chat
```

### 📖 詳細使用指南

#### 命令列參數說明

```bash
# 全域參數
--api-key       GLM-5.1 API金鑰
--api-url       API位址（預設：https://open.bigmodel.cn/api/paas/v4）
--model         使用的模型（預設：glm-5-0520）
--offline       離線模式（僅基礎功能）
--verbose       詳細輸出模式

# analyze 命令
devmind analyze <路徑> [選項]
  -r, --recursive    遞迴分析子目錄
  -o, --output       輸出檔案路徑
  --format           輸出格式（text/json/markdown）

# review 命令
devmind review [選項]
  -f, --file         審查單個檔案
  -d, --dir          審查目錄
  --strict           嚴格審查模式
  -o, --output       輸出檔案路徑

# refactor 命令
devmind refactor -f <檔案> [選項]
  --function         指定函數名
  --line-start       起始行號
  --line-end         結束行號

# docgen 命令
devmind docgen [選項]
  -m, --module       模組名
  -f, --file         檔案路徑
  -o, --output       輸出檔案路徑
  --format           輸出格式（markdown/html/rst）

# scan 命令
devmind scan -p <路徑> [選項]
  --exclude          排除的目錄
  -r, --report       生成報告
```

#### TUI 互動模式

```bash
# 啟動 TUI
devmind chat

# 在 TUI 中的可用命令
analyze <路徑>   - 分析程式碼
scan <路徑>      - 掃描專案
!命令            - 執行系統命令
history          - 查看歷史
clear            - 清屏
help             - 顯示幫助
exit             - 退出
```

---

## 💡 設計思路與迭代規劃

### 🎨 設計理念

1. **零依賴設計** - 核心功能僅使用 Python 標準庫，降低使用門檻
2. **輕量高效** - 無需安裝額外依賴，下載即用
3. **模組化架構** - 核心模組獨立，方便擴展和定制
4. **隱私優先** - 支持本地模式，數據不上傳雲端

### 🔧 技術選型

| 組件 | 技術選型 | 理由 |
|------|----------|------|
| 程式語言 | Python 3.8+ | 生態豐富、易於擴展 |
| LLM 接口 | REST API | 通用性強、易於集成 |
| TUI | 標準庫 | 零依賴、快速響應 |
| 配置管理 | 環境變數 + 檔案 | 靈活、安全 |

### 📅 迭代計劃

#### v1.1.0（規劃中）
- [ ] MCP 協議支持
- [ ] 支持本地 GGUF 模型
- [ ] 增強的 TUI 界面（使用 Rich）
- [ ] 多模型支持

#### v1.2.0（規劃中）
- [ ] Git 集成
- [ ] CI/CD 集成
- [ ] Web UI
- [ ] VSCode 插件

#### v2.0.0（遠期規劃）
- [ ] 多智慧體協作
- [ ] 專案級程式碼理解
- [ ] 自動測試生成
- [ ] 智慧程式碼審查團隊

---

## 📦 打包與部署

### 🐧 Linux/macOS

```bash
# 安裝後直接使用
devmind --help

# 或直接運行
python main.py --help
```

### 🪟 Windows

```powershell
# CMD 或 PowerShell
python main.py --help

# 或安裝後
devmind --help
```

### 🐳 Docker（可選）

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

## 📄 開源協議

本專案採用 **MIT 協議**開源。

詳細內容請查看 [LICENSE](./LICENSE) 檔案。

---

## 🙏 致謝

- **[GLM-5.1](https://github.com/zai-org/GLM-5)** - 智譜AI長程任務大模型
- **[OpenClaw](https://github.com/nicktorn89/openclaw)** - AI Agent 設計靈感
- 所有貢獻者和用戶

---

<div align="center">

**⭐ 如果這個專案對你有幫助，請給我們一個 Star！**

**📬 如有問題或建議，歡迎提交 Issue 或 PR**

**🦞</ 開發者智慧夥伴 - DevMind-CLI**

</div>
