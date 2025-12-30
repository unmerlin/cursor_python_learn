# Git 操作快速指南

## 📋 目录
- [基本操作流程](#基本操作流程)
- [常用命令](#常用命令)
- [更新文件到GitHub](#更新文件到github)
- [常见问题](#常见问题)

---

## 基本操作流程

### 更新文件的标准流程

```bash
# 1. 查看当前状态（可选）
git status

# 2. 添加修改的文件
git add .

# 3. 提交更改
git commit -m "你的提交说明"

# 4. 推送到GitHub
git push
```

---

## 常用命令

### 查看状态
```bash
# 查看哪些文件被修改了
git status

# 查看具体修改内容
git diff

# 查看提交历史
git log --oneline
```

### 添加文件
```bash
# 添加所有修改的文件
git add .

# 添加单个文件
git add 文件名

# 添加多个文件
git add 文件1 文件2
```

### 提交更改
```bash
# 提交并添加说明
git commit -m "提交说明"

# 提交所有已暂存的文件（如果已经git add过）
git commit -m "更新内容描述"
```

### 推送到GitHub
```bash
# 推送到远程仓库
git push

# 如果是第一次推送新分支
git push -u origin main
```

### 从GitHub拉取更新
```bash
# 拉取远程仓库的最新更改
git pull
```

---

## 更新文件到GitHub

### 场景1：修改了现有文件

```bash
# 完整流程
git add .
git commit -m "更新pandas教程：添加数据清洗示例"
git push
```

### 场景2：添加了新文件

```bash
# 完整流程
git add .
git commit -m "新增：添加新的学习笔记"
git push
```

### 场景3：修改了多个文件

```bash
# 一次性提交所有修改
git add .
git commit -m "批量更新：更新多个教程文件"
git push
```

### 场景4：只想提交特定文件

```bash
# 只提交某个文件
git add 文件名.ipynb
git commit -m "更新：修改了某个文件"
git push
```

---

## 提交信息规范

好的提交信息应该：
- ✅ 清晰描述做了什么修改
- ✅ 使用中文或英文都可以
- ✅ 简洁明了

**示例：**
- ✅ `更新pandas教程：添加数据清洗示例`
- ✅ `修复：修正matplotlib图表显示问题`
- ✅ `新增：添加Flask路由示例`
- ✅ `更新：完善Python基础学习内容`
- ❌ `更新`（太简单）
- ❌ `asdf`（无意义）

---

## 常见问题

### Q1: 如何撤销未提交的修改？
```bash
# 撤销工作区的修改（危险：会丢失修改）
git checkout -- 文件名

# 或者使用新命令
git restore 文件名
```

### Q2: 如何撤销已暂存但未提交的文件？
```bash
# 从暂存区移除，但保留工作区修改
git reset HEAD 文件名

# 或者使用新命令
git restore --staged 文件名
```

### Q3: 如何查看远程仓库地址？
```bash
git remote -v
```

### Q4: 如何查看提交历史？
```bash
# 简洁版
git log --oneline

# 详细版
git log

# 图形化显示
git log --graph --oneline --all
```

### Q5: 推送时提示需要先拉取？
```bash
# 先拉取远程更改
git pull

# 解决可能的冲突后，再推送
git push
```

### Q6: 如何忽略某些文件（如临时文件）？
创建或编辑 `.gitignore` 文件，添加要忽略的文件模式：
```
# 忽略所有 .tmp 文件
*.tmp

# 忽略特定文件夹
__pycache__/
*.pyc
```

---

## 快速操作脚本

项目根目录提供了 `快速更新.bat` 脚本，可以一键完成更新操作。

**使用方法：**
1. 双击运行 `快速更新.bat`
2. 输入提交信息
3. 自动完成 add、commit、push 操作

---

## 注意事项

⚠️ **重要提醒：**
- 每次修改文件后，必须执行 `git add`、`git commit`、`git push` 三步
- 提交信息要清晰，方便以后查看历史
- 推送前建议先 `git status` 查看修改内容
- 如果多人协作，推送前先 `git pull` 拉取最新更改

---

## 仓库信息

- **远程仓库地址：** https://github.com/unmerlin/cursor_python_learn
- **主分支：** main
- **本地目录：** C:\Users\Administrator\Desktop\cursor_python_learn

---

*最后更新：2025-12-30*









