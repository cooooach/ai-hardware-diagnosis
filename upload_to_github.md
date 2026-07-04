# 上传项目到 GitHub 指南

请按以下步骤操作：

## 1. 在 GitHub 上创建新仓库

1. 打开 https://github.com/new （登录后会自动跳转）
2. 填写：
   - **Repository name**: `ai-hardware-diagnosis`
   - **Description**: `基于大语言模型的AI硬件故障诊断助手 | 深圳大学 测控技术与仪器`
   - 选择 **Public**（公开，面试官才能看到）
   - **不要勾选** Add a README file
3. 点 **Create repository**

## 2. 复制仓库地址

创建后会跳转到新页面，复制类似这样的地址：
`https://github.com/cocoaoh/ai-hardware-diagnosis.git`

## 3. 在 PowerShell 里执行以下命令

先按 `Ctrl+C` 停掉 streamlit 进程，然后执行：

```
cd C:\Users\彭于晏\CodeBuddy\20260704214337\ai-hardware-diagnosis
git init
git config user.name "cocoaoh"
git config user.email "你的邮箱@qq.com"
git add .
git commit -m "Initial commit: AI硬件故障诊断助手"
git branch -M main
git remote add origin https://github.com/cocoaoh/ai-hardware-diagnosis.git
git push -u origin main
```

注意：
- `git config user.email` 那行，**把邮箱换成你注册 GitHub 用的那个邮箱**
- 第一次 push 可能会弹出登录框，按提示用浏览器登录 GitHub 即可

---

完成之后访问 https://github.com/cocoaoh/ai-hardware-diagnosis 就能看到你的项目页面了！
