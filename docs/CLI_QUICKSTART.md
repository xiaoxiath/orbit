# Orbit CLI 快速入门指南

**5 分钟上手 Orbit CLI 工具**

---

## 🚀 快速开始

### 安装

```bash
pip install orbit-macos
```

### 验证

```bash
orbit version
```

---

## 📋 5 个基础命令

### 1️⃣ 查看所有工具

```bash
orbit list
```

**输出示例**:
```
Total: 104 satellites | Categories: 12

  system_get_info [SAFE] system
  system_set_clipboard [MODERATE] system
  ...
```

---

### 2️⃣ 搜索工具

```bash
orbit search safari
```

**常用搜索**:
```bash
orbit search "get info"     # 按描述搜索
orbit search music -c music  # 在音乐类别搜索
```

---

### 3️⃣ 执行工具

```bash
# 获取系统信息
orbit run system_get_info

# 创建笔记
orbit run notes_create "Meeting Notes"

# 打开网页
orbit run safari_open "https://github.com"

# 设置音量
orbit run system_set_volume level=50
```

---

### 4️⃣ 交互模式

```bash
orbit interactive
```

**交互命令**:
```
orbit> list
orbit> search safari
orbit> run system_get_info
orbit> quit
```

---

### 5️⃣ 导出配置

```bash
# 导出 OpenAI Functions
orbit export openai -o tools.json

# 查看统计
orbit export stats
```

---

## 💡 实用示例

### 日常自动化

```bash
# 创建工作笔记
orbit run notes_create "$(date '+%Y-%m-%d') 日常工作会议"

# 发送提醒
orbit run system_send_notification '{"title": "会议提醒", "message": "5分钟后开始"}'

# 音乐控制
orbit run music_play
orbit run music_set_volume level=50
```

### 文件管理

```bash
# 查看下载文件夹
orbit run file_list '{"path": "~/Downloads"}'

# 创建备份目录
orbit run file_create_directory '{"name": "Backup", "location": "~/Documents"}'

# 清空废纸篓（危险操作！）
orbit run finder_empty_trash
```

### 网页自动化

```bash
# 搜索网页
orbit run safari_open "https://github.com"
orbit run safari_search "Orbit macOS"

# 查看当前标签
orbit run safari_list_tabs
```

---

## 🎯 常用别名

添加到 `~/.bashrc` 或 `~/.zshrc`:

```bash
# Orbit CLI 别名
alias orbit-sys='orbit run system_get_info'
alias orbit-note='orbit run notes_create'
alias notify='orbit run system_send_notification'
alias vol='orbit run system_set_volume'
alias music='orbit run music_play'
```

使用示例:

```bash
orbit-sys              # 获取系统信息
notify "Hello World"   # 发送通知
vol 50                 # 设置音量
music                  # 播放音乐
```

---

## 📚 更多帮助

### 查看帮助

```bash
orbit --help
orbit list --help
orbit run --help
```

### 查看卫星详情

```bash
orbit interactive
orbit> info <satellite_name>
```

### 完整文档

- **CLI 参考**: `docs/CLI_REFERENCE.md`
- **API 文档**: `docs/API_REFERENCE.md`
- **示例代码**: `examples/cli_examples.md`

---

## ⚡ 速查表

| 任务 | 命令 |
|------|------|
| 列出工具 | `orbit list` |
| 搜索工具 | `orbit search <keyword>` |
| 执行工具 | `orbit run <satellite> [args]` |
| 交互模式 | `orbit interactive` |
| 导出配置 | `orbit export openai` |
| 查看版本 | `orbit version` |
| 测试安装 | `orbit test` |

---

## ✨ 下一步

1. ✅ 安装 Orbit: `pip install orbit-macos`
2. ✅ 运行测试: `orbit test`
3. ✅ 查看工具: `orbit list`
4. ✅ 试用交互: `orbit interactive`
5. 📖 阅读完整文档: `docs/CLI_REFERENCE.md`

---

**开始使用 Orbit CLI，自动化你的 macOS!** 🛸
