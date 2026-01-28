# 📅 Orbit 日历功能使用指南

## 概述

Orbit 提供了 4 个日历相关的卫星：

| 卫星 | 安全级别 | 功能 |
|------|----------|------|
| `calendar_list_calendars` | SAFE | 列出所有日历 |
| `calendar_get_events` | SAFE | 获取指定日期范围的事件 |
| `calendar_create_event` | MODERATE | 创建新事件 |
| `calendar_delete_event` | DANGEROUS | 删除事件 |

---

## 🎯 快速开始

### 1. 查看所有日历

```bash
orbit run calendar_list_calendars
```

**返回示例**：
```json
[
  {
    "name": "工作",
    "writable": "true",
    "subscribed": "false"
  },
  {
    "name": "个人",
    "writable": "true",
    "subscribed": "false"
  }
]
```

---

### 2. 获取日历事件

#### 基本语法

```bash
orbit run calendar_get_events '{"start_date": "开始日期", "end_date": "结束日期"}'
```

#### 参数说明

| 参数 | 类型 | 必需 | 默认值 | 说明 |
|------|------|------|--------|------|
| `start_date` | string | ✅ | 无 | 开始日期 (YYYY-MM-DD) |
| `end_date` | string | ❌ | start_date + 7 天 | 结束日期 (YYYY-MM-DD) |
| `calendar` | string | ❌ | 所有日历 | 特定日历名称 |

---

### 3. 使用示例

#### 示例 1: 获取今天未来 7 天的事件

```bash
# 方法 1: 自动计算（推荐）
orbit run calendar_get_events '{"start_date": "2026-01-28"}'

# 方法 2: 指定日期范围
orbit run calendar_get_events '{"start_date": "2026-01-28", "end_date": "2026-02-03"}'
```

#### 示例 2: 获取特定日历的事件

```bash
# 只获取"工作"日历
orbit run calendar_get_events '{
  "start_date": "2026-01-28",
  "calendar": "工作"
}'
```

#### 示例 3: 获取指定日期范围

```bash
orbit run calendar_get_events '{
  "start_date": "2026-01-28",
  "end_date": "2026-02-15"
}'
```

---

## ⚠️ 注意事项

### 1. 日期格式

✅ **推荐格式**: `YYYY-MM-DD` (如 `2026-01-28`)

❌ **不支持的格式**:
- `MM/DD/YYYY` (如 `01/28/2026`)
- `DD-MM-YYYY` (如 `28-01-2026`)
- 中文日期 (如 `2026年1月28日`)

### 2. 系统要求

**macOS 版本**: macOS 10.15+

**日历应用**: 需要安装并至少打开一次日历应用

**权限**: 无需特殊权限（SAFE 级别）

### 3. 中文系统问题

如果你的系统是中文，可能会遇到以下错误：

```
❌ Error: 不能获得"every event whose start date ≥ date..."
```

**解决方案**:

1. **方法 1**: 使用未来日期
```bash
# 尝试获取未来 30 天的事件
orbit run calendar_get_events '{"start_date": "2026-02-01", "end_date": "2026-03-01"}'
```

2. **方法 2**: 指定具体的日历
```bash
orbit run calendar_get_events '{
  "start_date": "2026-01-28",
  "calendar": "工作"
}'
```

3. **方法 3**: 使用 macOS 日历应用的 Python 接口（如果 AppleScript 失败）

---

## 📝 输出格式

### calendar_get_events 返回

```json
[
  {
    "summary": "会议名称",
    "start": "Monday, January 28, 2026 at 2:00:00 PM",
    "end": "Monday, January 28, 2026 at 3:00:00 PM",
    "location": "会议室 A",
    "status": "",
    "calendar": "工作"
  }
]
```

### 字段说明

| 字段 | 说明 | 可能值 |
|------|------|--------|
| `summary` | 事件标题 | 字符串 |
| `start` | 开始时间 | 日期字符串 |
| `end` | 结束时间 | 日期字符串 |
| `location` | 地点 | 字符串（可能为空） |
| `status` | 状态 | 可能包含状态信息 |
| `calendar` | 日历名称 | 来自日历列表 |

---

## 🔧 高级用法

### 1. JSON 格式化输出

```bash
# 使用 jq 美化输出
orbit run calendar_get_events '{"start_date": "2026-01-28"}' | jq '.'
```

### 2. 保存到文件

```bash
# 保存事件到文件
orbit run calendar_get_events '{"start_date": "2026-01-28"}' > my_events.json

# 美化输出
cat my_events.json | jq '.'
```

### 3. 只显示事件标题

```bash
orbit run calendar_get_events '{"start_date": "2026-01-28"}' | jq -r '.[].summary'
```

---

## 🛠️ 故障排除

### 问题 1: 返回空结果

**可能原因**:
- 指定日期范围内没有事件
- 日期格式错误
- 需要授予权限

**解决方案**:
```bash
# 1. 检查日期格式
orbit run calendar_get_events '{"start_date": "2026-01-28"}'

# 2. 尝试更大的日期范围
orbit run calendar_get_events '{"start_date": "2026-01-01", "end_date": "2026-12-31"}'

# 3. 不指定日历（搜索所有）
orbit run calendar_get_events '{"start_date": "2026-01-28"}'
```

### 问题 2: 语法错误

**错误**: `execution error: 不能获得...`

**原因**:
- 日期格式不正确
- 日历应用未打开
- 系统语言问题

**解决方案**:
```bash
# 1. 验证日期格式（YYYY-MM-DD）
# 2. 先打开日历应用
open /System/Applications/Calendar.app
# 3. 等待几秒后重试
sleep 3
orbit run calendar_get_events '{"start_date": "2026-01-28"}'
```

### 问题 3: 权限错误

**如果遇到权限错误**：

1. 打开"系统设置"
2. 进入"隐私与安全性"
3. 进入"自动化"
4. 确保"终端"或你的 IDE 有日历应用的权限

---

## 💡 实用技巧

### 1. 查看今天的事件

```bash
# 获取今天的日期
TODAY=$(date +%Y-%m-%d)

# 获取今天和未来7天的事件
orbit run calendar_get_events "{\"start_date\": \"$TODAY\"}"
```

### 2. 查看本月的事件

```bash
# 获取本月第一天和最后一天
YEAR_MONTH=$(date +%Y-%m)
FIRST_DAY="${YEAR_MONTH}-01"
LAST_DAY="${YEAR_MONTH}-31"

orbit run calendar_get_events "{\"start_date\": \"$FIRST_DAY\", \"end_date\": \"$LAST_DAY\"}"
```

### 3. 导出为 CSV

```bash
# 提取事件信息并保存为 CSV
orbit run calendar_get_events '{"start_date": "2026-01-28"}' | \
  jq -r '.[] | [.summary, .start, .end, .location] | \
  awk 'BEGIN{print "Summary,Start,End,Location"} {print $1","$2","$3","$4"}' \
  > events.csv
```

---

## 📚 更多信息

- **所有卫星列表**: `orbit list`
- **搜索日历卫星**: `orbit search calendar`
- **帮助文档**: `orbit run calendar_get_events --help`

---

**提示**: 如果 AppleScript 遇到问题，可以尝试使用 Python 的日历 API 作为替代方案！

🛸 **Orbit - 你的 macOS 自动化助手**
