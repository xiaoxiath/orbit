# Orbit CLI 使用指南

> **版本**: 1.0.0
> **最后更新**: 2026-01-27

---

## 📋 目录

- [快速开始](#快速开始)
- [命令参考](#命令参考)
- [使用示例](#使用示例)
- [交互模式](#交互模式)
- [导出功能](#导出功能)
- [常见问题](#常见问题)

---

## 快速开始

### 安装

```bash
pip install orbit-macos
```

### 验证安装

```bash
orbit --version
# 输出: orbit, version 1.0.0

orbit test
# 测试所有功能
```

---

## 命令参考

### 1. orbit list - 列出卫星

列出所有可用的卫星工具。

#### 语法

```bash
orbit list [OPTIONS]
```

#### 选项

| 选项 | 简写 | 描述 | 默认值 |
|------|------|------|--------|
| `--category` | `-c` | 按类别过滤 | 全部 |
| `--safety` | `-s` | 按安全级别过滤 | 全部 |
| `--details` | `-d` | 显示详细信息 | 否 |
| `--count` | `-n` | 显示数量 | 20 |

#### 安全级别选项

- `safe` - 只显示 SAFE 级别
- `moderate` - 只显示 MODERATE 级别
- `dangerous` - 只显示 DANGEROUS 级别
- `critical` - 只显示 CRITICAL 级别

#### 使用示例

```bash
# 列出前 20 个卫星（默认）
orbit list

# 列出系统类卫星
orbit list -c system

# 只列出 SAFE 级别的卫星
orbit list -s safe

# 显示详细信息
orbit list -d

# 列出 50 个卫星
orbit list -n 50

# 组合过滤：列出系统类 SAFE 级别的卫星
orbit list -c system -s safe -d
```

#### 输出示例

```
Total: 104 satellites | Categories: 12

  system_get_info [SAFE] system
  system_get_clipboard [SAFE] system
  system_set_clipboard [MODERATE] system
  system_send_notification [SAFE] system
  system_take_screenshot [SAFE] system
```

---

### 2. orbit search - 搜索卫星

按名称或描述搜索卫星。

#### 语法

```bash
orbit search QUERY [OPTIONS]
```

#### 选项

| 选项 | 简写 | 描述 |
|------|------|------|
| `--category` | `-c` | 在指定类别中搜索 |
| `--details` | `-d` | 显示详细信息 |

#### 使用示例

```bash
# 搜索包含 "safari" 的卫星
orbit search safari

# 搜索包含 "clipboard" 的卫星
orbit search clipboard

# 在音乐类别中搜索
orbit search play -c music

# 显示详细信息
orbit search create -d

# 搜索多个关键词
orbit search "get info"
```

#### 输出示例

```
🔍 Search results for 'clipboard':

  system_get_clipboard [SAFE] system
  system_set_clipboard [MODERATE] system
  system_get_clipboard_history [SAFE] system
  system_clear_clipboard [MODERATE] system
```

---

### 3. orbit run - 执行卫星

执行指定的卫星工具。

#### 语法

```bash
orbit run SATELLITE_NAME [PARAMETERS] [OPTIONS]
```

#### 选项

| 选项 | 描述 |
|------|------|
| `--bypass-shield` | 绕过安全检查（不推荐） |
| `-t, --timeout` | 执行超时时间（秒） |

#### 参数格式

支持三种参数格式：

1. **JSON 格式**（推荐）
```bash
orbit run system_set_clipboard '{"content": "Hello"}'
```

2. **Key=Value 格式**
```bash
orbit run system_set_clipboard content="Hello"
orbit run file_list path=~/Documents recursive=false
```

3. **位置参数**
```bash
orbit run safari_open "https://github.com"
```

#### 使用示例

```bash
# 无参数执行
orbit run system_get_clipboard

# JSON 格式参数
orbit run system_set_volume '{"level": 50}'

# Key=Value 格式
orbit run notes_create title="我的笔记" body="内容在这里"

# 位置参数
orbit run safari_open "https://github.com/xiaoxiath/orbit"

# 绕过安全检查（不推荐）
orbit run file_delete path=~/test.txt --bypass-shield

# 设置超时
orbit run system_get_info -t 10
```

#### 输出示例

```
🚀 Running: system_get_clipboard

✅ Success!
Hello from Orbit!
```

---

### 4. orbit interactive - 交互模式

启动交互式 REPL 环境。

#### 语法

```bash
orbit interactive [OPTIONS]
```

#### 选项

| 选项 | 描述 |
|------|------|
| `--category` | `-c` | 从指定类别开始 |
| `--safe-only` | 只显示 SAFE 级别的卫星 |

#### 交互命令

在交互模式中，你可以使用以下命令：

| 命令 | 描述 |
|------|------|
| `help` | 显示帮助信息 |
| `list` | 列出可用卫星 |
| `search <query>` | 搜索卫星 |
| `run <satellite>` | 运行卫星 |
| `info <satellite>` | 显示卫星详细信息 |
| `quit` 或 `exit` | 退出交互模式 |

#### 使用示例

```bash
# 启动交互模式
orbit interactive

# 启动并只显示 SAFE 级别
orbit interactive --safe-only

# 启动并从系统类别开始
orbit interactive -c system
```

#### 交互示例

```
╔══════════════════════════════════════════════════════════╗
║  🛸  Orbit Interactive Mode                               ║
║                                                          ║
║  Commands:                                               ║
║    • help        - Show this help                        ║
║    • list        - List available satellites             ║
║    • search      - Search satellites                     ║
║    • run <sat>   - Run a satellite                      ║
║    • info <sat>  - Show satellite info                   ║
║    • quit/exit   - Exit interactive mode                 ║
║                                                          ║
╚══════════════════════════════════════════════════════════╝

orbit> list
  system_get_info [SAFE] system
  system_get_clipboard [SAFE] system
  ...

orbit> run system_get_clipboard
✅ Success!
Hello from Orbit!

orbit> search clipboard
  system_get_clipboard [SAFE] system
  system_set_clipboard [MODERATE] system

orbit> quit
👋 Goodbye!
```

---

### 5. orbit export - 导出功能

导出卫星数据到不同格式。

#### 语法

```bash
orbit export FORMAT [OPTIONS]
```

#### 支持的格式

- `openai` - OpenAI Functions 格式
- `json` - JSON 格式
- `json-schema` - JSON Schema 格式
- `stats` - 统计信息

#### 选项

| 选项 | 简写 | 描述 |
|------|------|------|
| `--output` | `-o` | 输出文件路径 |
| `--category` | `-c` | 导出特定类别 |
| `--indent` | `-i` | JSON 缩进（默认 2） |

#### 使用示例

```bash
# 导出统计信息
orbit export stats

# 导出为 OpenAI Functions 格式
orbit export openai

# 保存到文件
orbit export openai -o tools.json

# 只导出系统类
orbit export json -c system

# 自定义缩进
orbit export json -i 4

# 导出 JSON Schema
orbit export json-schema -o schema.json
```

#### 输出示例

```bash
$ orbit export stats

📊 Orbit Statistics:
{
  "total_satellites": 104,
  "categories": 12,
  "by_safety": {
    "safe": 51,
    "moderate": 44,
    "dangerous": 7,
    "critical": 2
  },
  "by_category": {
    "system": 24,
    "files": 10,
    "notes": 7,
    ...
  }
}
```

---

## 实用场景示例

### 场景 1: 系统信息收集

```bash
# 获取系统信息
orbit run system_get_info

# 获取剪贴板内容
orbit run system_get_clipboard

# 获取当前音量
orbit run system_get_volume

# 获取屏幕亮度
orbit run system_get_brightness
```

### 场景 2: 文件操作

```bash
# 列出文件（使用 Key=Value 格式）
orbit run file_list path=~/Documents recursive=false

# 读取文件
orbit run file_read path=~/Documents/notes.txt

# 写入文件（使用 JSON 格式）
orbit run file_write '{"path": "~/test.txt", "content": "Hello"}'

# 搜索文件
orbit run file_search path=~ query=orbit file_type=txt
```

### 场景 3: Safari 自动化

```bash
# 打开网页
orbit run safari_open "https://github.com"

# 获取当前 URL
orbit run safari_get_url

# 列出所有标签页
orbit run safari_list_tabs

# 搜索网页
orbit run safari_search "Orbit macOS"

# 刷新页面
orbit run safari_refresh
```

### 场景 4: 音乐控制

```bash
# 播放音乐
orbit run music_play

# 暂停
orbit run music_pause

# 下一曲
orbit run music_next

# 获取当前曲目
orbit run music_get_current

# 设置音量
orbit run music_set_volume '{"level": 70}'
```

### 场景 5: 应用管理

```bash
# 列出所有应用
orbit run app_list

# 启动应用
orbit run app_launch name=Safari

# 退出应用
orbit run app_quit name=Calculator

# 获取运行中的应用
orbit run app_get_running

# 激活应用到前台
orbit run app_activate name=Finder
```

---

## 安全级别说明

### SAFE (51 个卫星，49%)

- ✅ 读取操作
- ✅ 无需确认
- ✅ 无副作用

示例：
- `system_get_info` - 获取系统信息
- `system_get_clipboard` - 读取剪贴板
- `file_list` - 列出文件

### MODERATE (44 个卫星，42%)

- ⚠️ 非破坏性修改
- ⚠️ 建议确认
- ⚠️ 有数据变更

示例：
- `system_set_clipboard` - 设置剪贴板
- `file_write` - 写入文件
- `notes_create` - 创建笔记

### DANGEROUS (7 个卫星，7%)

- 🔴 破坏性操作
- 🔴 需要明确批准
- 🔴 可能导致数据丢失

示例：
- `file_delete` - 删除文件
- `notes_delete` - 删除笔记
- `finder_empty_trash` - 清空废纸篓

### CRITICAL (2 个卫星，2%)

- 🚨 系统级别操作
- 🚨 极度谨慎
- 🚨 影响系统运行

示例：
- `system_reboot` - 重启系统
- `system_shutdown` - 关闭系统

---

## 类别参考

| 类别 | 卫星数量 | SAFE 级别 | 常用命令 |
|------|---------|----------|---------|
| **system** | 24 | 11 | `system_get_info`, `system_send_notification` |
| **files** | 10 | 4 | `file_list`, `file_read`, `file_write` |
| **safari** | 12 | 10 | `safari_open`, `safari_get_url` |
| **music** | 11 | 4 | `music_play`, `music_pause` |
| **notes** | 7 | 4 | `notes_create`, `notes_list` |
| **apps** | 8 | 3 | `app_launch`, `app_quit` |
| **finder** | 6 | 4 | `finder_open_folder`, `finder_reveal` |
| **calendar** | 4 | 2 | `calendar_get_events`, `calendar_create_event` |
| **mail** | 6 | 2 | `mail_list_inbox`, `mail_send` |
| **reminders** | 6 | 2 | `reminders_list`, `reminders_create` |
| **wifi** | 6 | 2 | `wifi_list`, `wifi_current` |
| **contacts** | 4 | 3 | `contacts_search`, `contacts_get` |

---

## 常见问题

### Q1: 如何绕过安全检查？

使用 `--bypass-shield` 选项（不推荐）：

```bash
orbit run file_delete path=~/test.txt --bypass-shield
```

⚠️ **警告**: 仅在完全信任的操作中使用此选项。

### Q2: isinstance() 错误是什么？

执行命令时可能会看到：
```
❌ Error: isinstance() arg 2 must be a type...
✅ Success!
```

这是已知的显示问题，不影响功能。操作实际执行成功了。

### Q3: 如何传递复杂参数？

使用 JSON 格式：

```bash
orbit run file_write '{
  "path": "~/test.txt",
  "content": "Multi\nline\ncontent"
}'
```

### Q4: 命令执行太慢怎么办？

设置超时时间：

```bash
orbit run system_get_info -t 5
```

### Q5: 如何查看可用的卫星？

使用 list 或 search：

```bash
# 列出所有
orbit list

# 搜索特定功能
orbit search "screenshot"

# 按类别查看
orbit list -c safari
```

---

## 技巧与窍门

### 1. 使用 Tab 补全

如果你的 shell 支持 tab 补全：
```bash
orbit sys<TAB>  # 补全为 system
orbit run system_get_<TAB>  # 显示所有 system_get_* 卫星
```

### 2. 链式命令

```bash
# 获取剪贴板并保存
orbit run system_get_clipboard > clipboard.txt

# 统计系统卫星数量
orbit list -c system | grep "system_" | wc -l
```

### 3. 别名设置

在 `~/.bashrc` 或 `~/.zshrc` 中添加：
```bash
alias oli='orbit list'
alias ors='orbit search'
alias orr='orbit run'
alias ori='orbit interactive'
```

### 4. 批处理脚本

```bash
#!/bin/bash
# daily_tasks.sh

echo "Starting daily tasks..."

# 发送通知
orbit run system_send_notification title="Daily Tasks" message="Starting automation..."

# 备份文件
orbit run file_copy source=~/Documents dest=~/Backup

# 创建笔记
orbit run notes_create title="Daily Log" body="Tasks completed"

echo "Done!"
```

---

## 配置文件

### 创建配置文件

创建 `~/.orbit/config.json`：

```json
{
  "default_category": "system",
  "safe_only": false,
  "timeout": 30,
  "auto_bypass": false
}
```

### 环境变量

```bash
export ORBIT_SAFE_ONLY=true
export ORBIT_TIMEOUT=60
export ORBIT_DEFAULT_CATEGORY=system
```

---

## 集成示例

### 与 Shell 脚本集成

```bash
#!/bin/bash

# 检查系统状态
version=$(orbit run system_get_info | jq -r '.version')
echo "macOS Version: $version"

# 获取剪贴板
clipboard=$(orbit run system_get_clipboard)
echo "Clipboard: $clipboard"
```

### 与 Python 脚本集成

```python
import subprocess
import json

# 执行 CLI 命令
result = subprocess.run(
    ['orbit', 'run', 'system_get_info'],
    capture_output=True,
    text=True
)

# 解析 JSON 输出
info = json.loads(result.stdout)
print(f"Version: {info['version']}")
```

### 与 make/just 集成

```makefile
# Makefile
.PHONY: info backup

info:
	orbit run system_get_info

backup:
	orbit run file_copy source=~/Documents dest=~/Backup

notify:
	orbit run system_send_notification title="Build Complete" message="Your project is ready"
```

---

## 故障排除

### 问题：命令未找到

```bash
# 检查安装
which orbit

# 重新安装
pip install --upgrade orbit-macos
```

### 问题：权限错误

```bash
# 确保终端有辅助功能权限
# 系统设置 → 隐私与安全性 → 辅助功能
```

### 问题：AppleScript 错误

某些卫星可能需要额外的系统权限。确保：
- 终端有完整的磁盘访问权限
- 目标应用（如 Safari、音乐）有自动化权限

---

## 更多资源

- **GitHub**: https://github.com/xiaoxiath/orbit
- **PyPI**: https://pypi.org/project/orbit-macos/
- **完整文档**: https://github.com/xiaoxiath/orbit/tree/main/docs
- **问题反馈**: https://github.com/xiaoxiath/orbit/issues

---

**最后更新**: 2026-01-27
**版本**: 1.0.0
**总卫星数**: 104
**类别数**: 12
