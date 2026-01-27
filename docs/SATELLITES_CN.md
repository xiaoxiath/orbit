# Orbit 卫星参考手册

> **版本：** 1.0.0
> **最后更新：** 2026-01-27

> Orbit 星座中所有 100+ 卫星的完整参考。

---

## 📑 目录

- [系统遥测](#系统遥测)
- [文件通讯](#文件通讯)
- [备忘录站点](#备忘录站点)
- [提醒事项站点](#提醒事项站点)
- [日历站点](#日历站点)
- [邮件站点](#邮件站点)
- [Safari 站点](#safari-站点)
- [音乐站点](#音乐站点)
- [Finder 操作](#finder-操作)
- [通讯录](#通讯录)
- [WiFi 管理](#wifi-管理)
- [应用控制](#应用控制)

---

## 系统遥测

系统级操作和信息采集。

### 卫星列表

| 卫星 | 安全等级 | 描述 |
|------|----------|------|
| `system_get_info` | SAFE | 获取 macOS 系统信息（版本、主机名、硬件详情） |
| `system_get_clipboard` | SAFE | 读取当前剪贴板内容 |
| `system_set_clipboard` | MODERATE | 设置剪贴板内容 |
| `system_send_notification` | SAFE | 发送系统通知 |
| `system_take_screenshot` | SAFE | 截屏到文件 |
| `system_get_volume` | SAFE | 获取当前系统音量（0-100） |
| `system_set_volume` | MODERATE | 设置系统音量（0-100） |
| `system_get_brightness` | SAFE | 获取屏幕亮度（0-100） |
| `system_set_brightness` | MODERATE | 设置屏幕亮度（0-100） |

### 使用示例

```python
from orbit import MissionControl

mission = MissionControl()

# 获取系统信息
info = mission.launch("system_get_info", {})
print(f"macOS {info['version']}")

# 截屏
mission.launch("system_take_screenshot", {
    "path": "~/Desktop/screenshot.png"
})

# 设置音量
mission.launch("system_set_volume", {"level": 50})
```

---

## 文件通讯

文件系统操作。

### 卫星列表

| 卫星 | 安全等级 | 描述 |
|------|----------|------|
| `file_list` | SAFE | 列出目录文件 |
| `file_read` | SAFE | 读取文件内容 |
| `file_write` | MODERATE | 写入文件内容 |
| `file_delete` | DANGEROUS | 删除文件 |
| `file_move` | MODERATE | 移动文件 |
| `file_copy` | MODERATE | 复制文件 |
| `file_search` | SAFE | 搜索文件 |
| `file_empty_trash` | DANGEROUS | 清空废纸篓 |

### 使用示例

```python
# 列出文件
files = mission.launch("file_list", {
    "path": "~",
    "recursive": False
})

# 读取文件
content = mission.launch("file_read", {
    "path": "~/Documents/notes.txt"
})

# 写入文件
mission.launch("file_write", {
    "path": "~/Documents/new_note.txt",
    "content": "由 Orbit 创建 🛸"
})

# 搜索文件
results = mission.launch("file_search", {
    "path": "~",
    "query": "orbit",
    "file_type": "txt"
})
```

---

## 备忘录站点

Apple 备忘录应用操作。

### 卫星列表

| 卫星 | 安全等级 | 描述 |
|------|----------|------|
| `notes_list` | SAFE | 列出文件夹中的所有笔记 |
| `notes_get` | SAFE | 按 ID 获取笔记内容 |
| `notes_create` | MODERATE | 创建新笔记 |
| `notes_update` | MODERATE | 更新现有笔记 |
| `notes_delete` | DANGEROUS | 删除笔记 |
| `notes_search` | SAFE | 搜索笔记 |
| `notes_list_folders` | SAFE | 列出所有文件夹 |

### 使用示例

```python
# 列出笔记
notes = mission.launch("notes_list", {"folder": "Notes"})

# 创建笔记
mission.launch("notes_create", {
    "title": "会议记录",
    "body": "<h1>讨论要点</h1><ul><li>要点 1</li></ul>",
    "folder": "工作"
})

# 搜索笔记
results = mission.launch("notes_search", {"query": "会议"})
```

---

## 提醒事项站点

Apple 提醒事项应用操作。

### 卫星列表

| 卫星 | 安全等级 | 描述 |
|------|----------|------|
| `reminders_list` | SAFE | 列出所有提醒 |
| `reminders_list_lists` | SAFE | 列出所有提醒列表 |
| `reminders_create` | MODERATE | 创建新提醒 |
| `reminders_complete` | MODERATE | 标记提醒为完成 |
| `reminders_delete` | DANGEROUS | 删除提醒 |

### 使用示例

```python
# 列出提醒
reminders = mission.launch("reminders_list", {})

# 创建提醒
mission.launch("reminders_create", {
    "name": "明天下午3点开会",
    "due_date": "2026-01-28",
    "list": "工作"
})

# 完成提醒
mission.launch("reminders_complete", {"id": "reminder-id"})
```

---

## 日历站点

Apple 日历应用操作。

### 卫星列表

| 卫星 | 安全等级 | 描述 |
|------|----------|------|
| `calendar_list_calendars` | SAFE | 列出所有日历 |
| `calendar_get_events` | SAFE | 获取日期范围内的事件 |
| `calendar_create_event` | MODERATE | 创建新事件 |
| `calendar_delete_event` | DANGEROUS | 删除事件 |

### 使用示例

```python
# 列出日历
calendars = mission.launch("calendar_list_calendars", {})

# 获取事件
events = mission.launch("calendar_get_events", {
    "start_date": "2026-01-27",
    "end_date": "2026-01-28"
})

# 创建事件
mission.launch("calendar_create_event", {
    "summary": "团队会议",
    "start_date": "2026-01-28 15:00",
    "end_date": "2026-01-28 16:00",
    "calendar": "工作"
})
```

---

## 邮件站点

Apple 邮件应用操作。

### 卫星列表

| 卫星 | 安全等级 | 描述 |
|------|----------|------|
| `mail_send` | MODERATE | 发送邮件 |
| `mail_list_inbox` | SAFE | 列出收件箱邮件 |
| `mail_get` | SAFE | 获取邮件内容 |
| `mail_delete` | DANGEROUS | 删除邮件 |

### 使用示例

```python
# 列出收件箱
emails = mission.launch("mail_list_inbox", {"limit": 10})

# 发送邮件
mission.launch("mail_send", {
    "to": "user@example.com",
    "subject": "会议记录",
    "body": "以下是今天会议的记录..."
})
```

---

## Safari 站点

Safari 浏览器操作。

### 卫星列表

| 卫星 | 安全等级 | 描述 |
|------|----------|------|
| `safari_open` | SAFE | 在 Safari 中打开 URL |
| `safari_get_url` | SAFE | 获取当前标签页 URL |
| `safari_get_text` | SAFE | 获取页面文本内容 |
| `safari_list_tabs` | SAFE | 列出所有打开的标签页 |
| `safari_search` | SAFE | 搜索网页 |

### 使用示例

```python
# 打开 URL
mission.launch("safari_open", {"url": "https://github.com"})

# 获取当前 URL
url = mission.launch("safari_get_url", {})

# 列出标签页
tabs = mission.launch("safari_list_tabs", {})
```

---

## 音乐站点

Apple 音乐应用操作。

### 卫星列表

| 卫星 | 安全等级 | 描述 |
|------|----------|------|
| `music_play` | MODERATE | 开始或恢复播放 |
| `music_pause` | MODERATE | 暂停播放 |
| `music_next` | MODERATE | 跳到下一曲 |
| `music_previous` | MODERATE | 返回上一曲 |
| `music_play_track` | MODERATE | 播放指定曲目 |
| `music_get_current` | SAFE | 获取当前曲目信息 |

### 使用示例

```python
# 播放
mission.launch("music_play", {})

# 获取当前曲目
track = mission.launch("music_get_current", {})
print(f"正在播放：{track['name']}")

# 下一曲
mission.launch("music_next", {})
```

---

## Finder 操作

Finder 文件管理器操作。

### 卫星列表

| 卫星 | 安全等级 | 描述 |
|------|----------|------|
| `finder_open_folder` | SAFE | 在 Finder 中打开文件夹 |
| `finder_new_folder` | MODERATE | 创建新文件夹 |
| `finder_reveal` | SAFE | 在 Finder 中显示文件 |
| `finder_get_selection` | SAFE | 获取选中的文件 |

### 使用示例

```python
# 打开文件夹
mission.launch("finder_open_folder", {"path": "~/Documents"})

# 显示文件
mission.launch("finder_reveal", {"path": "~/Documents/file.txt"})
```

---

## 通讯录

通讯录应用操作。

### 卫星列表

| 卫星 | 安全等级 | 描述 |
|------|----------|------|
| `contacts_search` | SAFE | 搜索联系人 |
| `contacts_get` | SAFE | 获取联系人详情 |

### 使用示例

```python
# 搜索联系人
contacts = mission.launch("contacts_search", {
    "query": "张三"
})
```

---

## WiFi 管理

网络和 WiFi 操作。

### 卫星列表

| 卫星 | 安全等级 | 描述 |
|------|----------|------|
| `wifi_connect` | MODERATE | 连接到 WiFi 网络 |
| `wifi_disconnect` | MODERATE | 断开 WiFi |
| `wifi_list` | SAFE | 列出可用网络 |
| `wifi_current` | SAFE | 获取当前连接信息 |

### 使用示例

```python
# 列出网络
networks = mission.launch("wifi_list", {})

# 连接
mission.launch("wifi_connect", {"ssid": "网络名称"})

# 当前连接
current = mission.launch("wifi_current", {})
```

---

## 应用控制

应用生命周期管理。

### 卫星列表

| 卫星 | 安全等级 | 描述 |
|------|----------|------|
| `app_list` | SAFE | 列出已安装应用 |
| `app_launch` | MODERATE | 启动应用 |
| `app_quit` | MODERATE | 退出应用 |
| `app_activate` | SAFE | 激活应用到前台 |

### 使用示例

```python
# 列出应用
apps = mission.launch("app_list", {})

# 启动应用
mission.launch("app_launch", {"name": "Safari"})

# 退出应用
mission.launch("app_quit", {"name": "Safari"})
```

---

## 📊 统计信息

### 按类别统计

| 类别 | 卫星数量 |
|------|----------|
| 系统遥测 | 9 |
| 文件通讯 | 8 |
| 备忘录 | 7 |
| 提醒事项 | 5 |
| 日历 | 4 |
| 邮件 | 4 |
| Safari | 5 |
| 音乐 | 6 |
| Finder | 4 |
| 通讯录 | 2 |
| WiFi | 4 |
| 应用控制 | 4 |
| **总计** | **68+** |

### 按安全等级统计

| 等级 | 数量 | 百分比 |
|------|------|--------|
| SAFE | 35 | 51% |
| MODERATE | 28 | 41% |
| DANGEROUS | 6 | 9% |
| CRITICAL | 0 | 0% |

---

## 🔍 快速搜索

按关键词查找卫星：

**系统：** `system_`
**文件：** `file_`
**备忘录：** `notes_`
**提醒事项：** `reminders_`
**日历：** `calendar_`
**邮件：** `mail_`
**Safari：** `safari_`
**音乐：** `music_`
**Finder：** `finder_`
**通讯录：** `contacts_`
**WiFi：** `wifi_`
**应用：** `app_`

---

## 📝 命名规范

所有卫星遵循以下命名模式：
```
{类别}_{动作}_{可选对象}
```

示例：
- `system_get_info` - 类别：系统，动作：获取
- `notes_create` - 类别：备忘录，动作：创建
- `file_list` - 类别：文件，动作：列出
- `app_launch` - 类别：应用，动作：启动

---

**卫星参考版本：** 1.0.0
**最后更新：** 2026-01-27
**卫星总数：** 68+

🛸 探索星座！
