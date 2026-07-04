# AI 硬件故障诊断助手

## 📖 项目简介

基于大语言模型（DeepSeek）的智能硬件故障诊断系统。硬件工程师只需输入故障现象，AI 即可给出结构化的故障分析、排查步骤和解决方案。

**适合场景：** 嵌入式开发、模拟电路调试、数字电路排错、电源问题诊断等。

## ✨ 功能特点

- 🔬 **专业诊断**：结合测控专业知识，给出深度故障分析
- 📋 **结构化输出**：故障分析 → 排查步骤 → 解决方案 → 注意事项
- ⚡ **快捷场景**：内置 6 个常见故障场景，一键填充
- 🎨 **现代 UI**：基于 Streamlit 的暗色主题界面

## 🚀 快速开始

### 1. 安装依赖

```bash
pip install streamlit openai python-dotenv
```

### 2. 配置 API Key

在项目根目录创建 `.env` 文件：

```
DEEPSEEK_API_KEY=你的DeepSeek_API_Key
DEEPSEEK_API_BASE=https://api.deepseek.com
MODEL_NAME=deepseek-chat
```

> 💡 DeepSeek API Key 获取：访问 [platform.deepseek.com](https://platform.deepseek.com) 注册即可，新用户有免费额度。

### 3. 运行

```bash
streamlit run app.py
```

浏览器打开 `http://localhost:8501` 即可使用。

## 🛠️ 技术栈

| 技术 | 用途 |
|------|------|
| Python | 后端语言 |
| Streamlit | Web 界面框架 |
| DeepSeek API | 大语言模型推理 |
| OpenAI SDK | API 调用 |

## 📸 界面预览

- 左侧：故障现象输入区 + 快捷场景选择
- 右侧：AI 诊断结果展示区
- 暗色主题，专业工业风

## 👤 作者

钟睿恒 | 深圳大学 物理与光电工程学院 | 测控技术与仪器 2024级

---

*本项目为个人学习项目，用于展示 AI + 硬件交叉领域的应用能力。*
