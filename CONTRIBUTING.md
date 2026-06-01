# 🤝 贡献指南

感谢您对 DevMind-CLI 的关注！我们欢迎各种形式的贡献。

## 📋 贡献方式

### 🐛 报告问题
- 使用 GitHub Issues 报告 Bug
- 提供详细的问题描述和复现步骤
- 如果可能，提供错误日志和截图

### 💡 提出建议
- 通过 GitHub Issues 提出新功能建议
- 描述您的使用场景和需求
- 解释为什么这个功能对您有价值

### 🔧 提交代码

#### 工作流程
1. **Fork** 本仓库
2. **Clone** 您 Fork 的仓库
   ```bash
   git clone https://github.com/你的用户名/DevMind-CLI.git
   cd DevMind-CLI
   ```
3. **创建分支**
   ```bash
   git checkout -b feature/你的功能名
   # 或
   git checkout -b fix/你修复的问题
   ```
4. **进行开发**
   - 编写代码
   - 添加测试
   - 更新文档
5. **提交更改**
   ```bash
   git add .
   git commit -m "feat: 添加新功能"
   ```
6. **推送分支**
   ```bash
   git push origin feature/你的功能名
   ```
7. **创建 Pull Request**

#### 提交规范
我们使用 Conventional Commits 规范：

- `feat:` 新功能
- `fix:` 修复问题
- `docs:` 文档更新
- `style:` 代码格式调整
- `refactor:` 代码重构
- `test:` 添加测试
- `chore:` 构建过程或辅助工具的变动

示例：
```
feat: 添加代码扫描功能
fix: 修复TUI界面在Windows下的显示问题
docs: 更新README多语言版本
```

## 🧪 测试

在提交之前，请确保：

```bash
# 运行所有测试
python -m pytest tests/

# 运行特定测试
python -m pytest tests/test_analyzer.py
```

## 📐 代码规范

- 遵循 PEP 8 风格指南
- 使用有意义的变量和函数名
- 添加必要的注释和文档字符串
- 保持代码简洁和可读

## ❓ 问题解答

如果您有任何疑问，请随时通过以下方式联系我们：
- GitHub Issues
- 提交 Discussion

## 📜 许可证

通过贡献代码，您同意您的代码将按照 MIT 许可证开源。

---

再次感谢您的贡献！ 🎉
