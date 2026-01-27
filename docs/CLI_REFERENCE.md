# Orbit CLI - 命令行工具文档

**版本**: 1.0.0
**状态**: ✅ 已完成

---

## 📖 概述

Orbit CLI 是 Orbit macOS 自动化工具包的命令行接口，提供便捷的方式来使用 100+ 个卫星工具。

### 特性

- 🛸 **100+ 卫星工具**: 覆盖 12 个应用类别
- 🔍 **智能搜索**: 按名称、描述、类别搜索
- 🎯 **简单执行**: 一行命令执行复杂操作
- 💬 **交互模式**: REPL 环境进行连续操作
- 📤 **格式导出**: 导出 OpenAI Functions、JSON Schema 等
- 🎨 **彩色输出**: 清晰的终端显示

---

## 🚀 安装

### 从 PyPI 安装

```bash
pip install orbit-macos
```

### 从源码安装

```bash
git clone https://github.com/xiaoxiath/orbit.git
cd orbit
poetry install
poetry build
pip install dist/orbit_macos-1.0.0-py3-none-any.whl
```

### 验证安装

```bash
orbit --version
# 或
orbit test
```

---

## 📚 命令参考

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

#### 示例

```bash
# 列出前 20 个卫星
orbit list

# 列出所有系统卫星
orbit list -c system

# 只列出 SAFE 级别的卫星
orbit list -s safe

# 显示详细信息
orbit list -d

# 列出 50 个卫星
orbit list -n 50

# 组合过滤
orbit list -c music -s safe -d
```

#### 输出

```
📋 Satellites in 'system':

  system_get_info [SAFE] system
      Description: Get macOS system information
      Parameters: 0

  system_set_volume [MODERATE] system
      Description: Set system volume
      Parameters: 1
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

#### 示例

```bash
# 搜索包含 "safari" 的卫星
orbit search safari

# 搜索包含 "get info" 的卫星
orbit search "get info"

# 在音乐类别中搜索
orbit search play -c music

# 显示详细信息
orbit search create -d
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
| `--timeout` | 执行超时时间（秒） |

#### 参数格式

支持 3 种参数格式：

1. **JSON 格式**
```bash
orbit run file_set_content '{"path": "~/test.txt", "content": "Hello"}'
```

2. **Key=Value 格式**
```bash
orbit run system_set_volume level=50
```

3. **位置参数**
```bash
orbit run notes_create "My Note"
orbit run safari_open "https://github.com"
```

#### 示例

```bash
# 无参数执行
orbit run system_get_info

# JSON 参数
orbit run notes_create '{"name": "Meeting", "body": "Notes"}'
orbit run file_list '{"path": "~/Documents"}'

# Key=Value 参数
orbit run music_set_volume level=75

# 位置参数
orbit run safari_open "https://github.com"
orbit run notes_create "Quick Note"

# 组合使用
orbit run notes_create "Note" '{"body": "Content"}'
```

---

### 4. orbit interactive - 交互模式

启动交互式 REPL 环境。

#### 语法

```bash
orbit interactive [OPTIONS]
```

#### 选项

| 选项 | 简写 | 描述 |
|------|------|------|
| `--category` | `-c` | 启动时显示特定类别 |
| `--safe-only` | | 只显示 SAFE 级别卫星 |

#### 交互命令

进入交互模式后可使用以下命令：

| 命令 | 描述 | 示例 |
|------|------|------|
| `list` | 列出卫星 | `list -c system` |
| `search` | 搜索卫星 | `search safari` |
| `run` | 执行卫星 | `run system_get_info` |
| `info` | 显示卫星详情 | `info system_get_info` |
| `help` | 显示帮助 | `help` |
| `quit/exit/q` | 退出 | `quit` |

#### 示例

```bash
# 启动交互模式
orbit interactive

# 在交互模式中：
orbit> list
orbit> search safari
orbit> run system_get_info
orbit> info system_get_info
orbit> quit
```

#### 交互流程示例

```
$ orbit interactive

╔══════════════════════════════════════════════════════════╗
║  🛸  Orbit Interactive Mode                               ║
╚══════════════════════════════════════════════════════════╝

orbit> list -c music

📋 Satellites in 'music':
  music_play [MODERATE] music
  music_pause [MODERATE] music
  music_get_current [SAFE] music

orbit> run music_play

✅ Success!

orbit> info music_play

📋 music_play
  Description: Start or resume music playback
  Category: music
  Safety: moderate
  Parameters: (none)

orbit> quit
👋 Goodbye!
```

---

### 5. orbit export - 导出数据

导出卫星到各种格式。

#### 语法

```bash
orbit export FORMAT [OPTIONS]
```

#### 格式选项

| 格式 | 描述 |
|------|------|
| `openai` | OpenAI Functions 格式 |
| `json` | JSON 格式 |
| `json-schema` | JSON Schema 格式 |
| `stats` | 统计信息 |

#### 选项

| 选项 | 简写 | 描述 | 默认值 |
|------|------|------|--------|
| `--output` | `-o` | 输出文件路径 | stdout |
| `--category` | `-c` | 导出特定类别 | 全部 |
| `--indent` | `-i` | JSON 缩进 | 2 |

#### 示例

```bash
# 导出到 OpenAI Functions 格式（显示在终端）
orbit export openai

# 保存到文件
orbit export openai -o tools.json

# 只导出系统卫星
orbit export openai -c system -o system_tools.json

# 导出为 JSON Schema
orbit export json-schema

# 显示统计信息
orbit export stats

# 自定义缩进
orbit export json -i 4 -o pretty.json
```

#### OpenAI Functions 输出格式

```json
[
  {
    "type": "function",
    "function": {
      "name": "system_get_info",
      "description": "Get macOS system information",
      "parameters": {
        "type": "object",
        "properties": {},
        "required": []
      }
    }
  }
]
```

---

### 6. orbit test - 测试安装

测试 Orbit 安装和配置。

#### 语法

```bash
orbit test [OPTIONS]
```

#### 示例

```bash
# 完整测试
orbit test

# 测试特定类别
orbit test -c system
```

---

### 7. orbit version - 版本信息

显示 Orbit 版本和系统信息。

#### 语法

```bash
orbit version
```

#### 输出

```
🛸 Orbit - macOS Automation Toolkit

  Version: 1.0.0
  Python: 3.10
  Satellites: 104
  Categories: 12
```

---

## 🎯 实用场景

### 场景 1: 日常自动化

```bash
# 创建每日笔记
orbit run notes_create "Daily Notes $(date +%Y-%m-%d)"

# 发送通知提醒
orbit run system_send_notification '{"title": "Meeting", "message": "Starting in 5 min"}'

# 查看系统信息
orbit run system_get_info
```

### 场景 2: Web 研究

```bash
# 打开网页并搜索
orbit run safari_open "https://github.com"
orbit run safari_search "Orbit macOS automation"

# 获取页面文本
orbit run safari_get_text

# 保存笔记
orbit run notes_create "GitHub Research" "$(orbit run safari_get_text)"
```

### 场景 3: 文件管理

```bash
# 列出下载文件夹
orbit run file_list '{"path": "~/Downloads"}'

# 创建备份目录
orbit run file_create_directory '{"name": "Backup", "location": "~/Documents"}'

# 移动文件
orbit run file_move '{"source": "~/Downloads/file.txt", "destination": "~/Documents/Archive/"}'
```

### 场景 4: 音乐控制

```bash
# 播放音乐
orbit run music_play

# 设置音量
orbit run music_set_volume '{"level": 50}'

# 播放特定歌曲
orbit run music_play_track '{"name": "My Favorite Song"}'

# 查看当前播放
orbit run music_get_current
```

### 场景 5: 导出 AI 集成

```bash
# 导出 OpenAI Functions
orbit export openai -o orbit_tools.json

# 使用 Python 脚本
python << 'EOF'
import json
from openai import OpenAI

with open('orbit_tools.json') as f:
    tools = json.load(f)

client = OpenAI()
response = client.chat.completions.create(
    model="gpt-3.5-turbo-1106",
    messages=[{"role": "user", "content": "What's my macOS version?"}],
    tools=tools
)

print(response.choices[0].message)
EOF
```

---

## 💡 高级用法

### 1. 创建别名

在 `~/.bashrc` 或 `~/.zshrc` 中添加：

```bash
# Orbit CLI aliases
alias orbit-sys='orbit run system_get_info'
alias orbit-note='orbit run notes_create'
alias orbit-safari='orbit run safari_open'
alias orbit-music='orbit run music_play'
alias vol='orbit run system_set_volume'
alias notify='orbit run system_send_notification'
```

使用：

```bash
orbit-sys                      # 获取系统信息
orbit-note "Quick idea"        # 创建笔记
orbit-safari "https://..."     # 打开网页
vol 75                         # 设置音量 75%
```

### 2. Shell 脚本集成

```bash
#!/bin/bash
# daily_workflow.sh

echo "Starting daily workflow..."

# 获取系统信息
orbit run system_get_info > system_info.json

# 创建日报笔记
orbit run notes_create "Daily Report $(date +%F)" "$(cat system_info.json)"

# 发送提醒
orbit run system_send_notification '{"title": "Workflow", "message": "Daily routine completed"}'

echo "Done!"
```

### 3. Cron 任务调度

```bash
# 编辑 crontab
crontab -e

# 添加任务
# 每天早上 9 点发送通知
0 9 * * * /usr/local/bin/orbit run system_send_notification '{"title": "Morning Briefing", "message": "Check your calendar"}'

# 每天晚上 6 点创建笔记
0 18 * * * /usr/local/bin/orbit run notes_create "Evening Notes" "End of day summary"

# 每小时备份提醒
0 * * * * /usr/local/bin/orbit run system_send_notification '{"title": "Backup", "message": "Time to backup your work"}'
```

### 4. 管道和重定向

```bash
# 复制系统信息到剪贴板
orbit run system_get_info | pbcopy

# 导出并过滤
orbit export openai | jq '.[] | select(.function.name | contains("system"))'

# 保存到文件
orbit run system_get_info > system_info.json

# 处理输出
orbit run file_list path=~/Desktop | grep ".txt"
```

### 5. 与其他工具集成

```python
# Python 脚本中使用
import subprocess
import json

# 获取系统信息
result = subprocess.run(
    ['orbit', 'run', 'system_get_info'],
    capture_output=True,
    text=True
)

if result.returncode == 0:
    info = json.loads(result.stdout)
    print(f"Hostname: {info.get('hostname')}")
```

---

## 🐛 故障排除

### 问题: 命令未找到

```bash
# 检查安装
which orbit

# 重新安装
pip install orbit-macos --upgrade

# 或使用 python -m
python -m orbit.cli list
```

### 问题: 卫星执行失败

```bash
# 测试 Orbit
orbit test

# 查看卫星信息
orbit interactive
orbit> info <satellite_name>

# 尝试绕过安全检查（不推荐）
orbit run <satellite> --bypass-shield
```

### 问题: AppleScript 执行错误

```bash
# 确认在 macOS 上运行
uname -s  # 应该是 Darwin

# 检查 osascript
which osascript
```

---

## 📊 性能优化

### 启动优化

CLI 会延迟加载卫星，只有首次使用时才注册，加快启动速度。

### 缓存机制

```bash
# 导出后缓存到文件
orbit export openai -o ~/.cache/orbit_tools.json

# 后续直接使用缓存
cat ~/.cache/orbit_tools.json
```

---

## 🔧 配置

### 环境变量

```bash
# 设置默认超时（秒）
export ORBIT_TIMEOUT=60

# 禁用颜色
export ORBIT_NO_COLOR=1

# 调试模式
export ORBIT_DEBUG=1
```

### 配置文件

创建 `~/.orbitrc.json`:

```json
{
  "default_timeout": 30,
  "safe_mode": true,
  "favorite_satellites": [
    "system_get_info",
    "notes_create",
    "safari_open"
  ]
}
```

---

## 📚 参考资源

- **完整示例**: `examples/cli_examples.md`
- **API 文档**: `docs/API_REFERENCE.md`
- **卫星目录**: `docs/SATELLITES.md`
- **GitHub**: https://github.com/xiaoxiath/orbit

---

## 🎓 最佳实践

1. **使用交互模式探索**: `orbit interactive`
2. **先搜索再执行**: `orbit search <keyword>`
3. **查看卫星信息**: `orbit info <satellite>` (在交互模式中)
4. **导出常用配置**: `orbit export openai -o tools.json`
5. **创建常用别名**: 简化日常操作

---

**文档版本**: 1.0.0
**更新时间**: 2026-01-27
**维护者**: Orbit Team
