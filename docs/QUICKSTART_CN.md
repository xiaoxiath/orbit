# Orbit 快速入门指南

<img src="logo.png" alt="Orbit Logo" width="150"/>

> **5 分钟上手 Orbit**

---

## 🚀 安装

### 前置要求

- macOS 12.0+（Monterey 或更高版本）
- Python 3.10 或更高版本
- 管理员权限（某些 AppleScript 操作需要）

### 使用 pip 安装

```bash
pip install orbit-macos
```

### 从源码安装

```bash
git clone https://github.com/yourusername/orbit.git
cd orbit
pip install -e .
```

### 验证安装

```bash
python -c "from orbit import MissionControl; print('Orbit 安装成功！🛸')"
```

---

## ⚡ 第一次任务

### 基础示例

创建文件 `first_mission.py`：

```python
from orbit import MissionControl
from orbit.satellites import system_satellites

# 初始化任务控制中心
mission = MissionControl()

# 注册系统卫星
mission.register_constellation(system_satellites)

# 发射第一次任务
result = mission.launch(
    "system_get_info",
    parameters={}
)

print(f"macOS 版本: {result['version']}")
print(f"主机名: {result['hostname']}")
print(f"用户: {result['username']}")
print(f"架构: {result['architecture']}")
```

运行：

```bash
python first_mission.py
```

输出：

```
macOS 版本: 14.0
主机名: MacBook-Pro
用户: astronaut
架构: arm64
```

---

## 🛰️ 使用卫星工具

### 注册单个卫星

```python
from orbit import MissionControl
from orbit.satellites.system import info, clipboard

mission = MissionControl()

# 注册特定卫星
mission.register(info.system_get_info)
mission.register(clipboard.system_get_clipboard)

# 列出已注册卫星
for satellite in mission.constellation.list_all():
    print(f"🛰️  {satellite.name}: {satellite.description}")
```

### 注册所有卫星

```python
from orbit import MissionControl
from orbit.satellites import all_satellites

mission = MissionControl()
mission.register_constellation(all_satellites)

print(f"卫星总数: {len(mission.constellation.list_all())}")
print(f"类别: {mission.constellation.get_categories()}")
```

---

## 🛡️ 配置防护罩

### 默认安全设置

默认情况下，Orbit 使用保守的安全设置：

```python
from orbit import MissionControl, SafetyShield, SafetyLevel

# 默认行为：
# SAFE 操作：允许
# MODERATE 操作：需要确认
# DANGEROUS 操作：需要确认
# CRITICAL 操作：阻止

mission = MissionControl()  # 使用默认防护罩
```

### 自定义安全规则

```python
from orbit import MissionControl, SafetyShield, SafetyLevel

# 创建自定义防护罩
shield = SafetyShield(
    rules={
        SafetyLevel.SAFE: "allow",
        SafetyLevel.MODERATE: "allow",  # 自动允许中等操作
        SafetyLevel.DANGEROUS: "deny",   # 阻止危险操作
        SafetyLevel.CRITICAL: "deny"
    }
)

mission = MissionControl(safety_shield=shield)
```

### 添加确认回调

```python
from orbit import SafetyShield, SafetyLevel

def confirm_mission(satellite, parameters):
    """请求用户确认"""
    print(f"\n⚠️  卫星: {satellite.name}")
    print(f"   安全等级: {satellite.safety_level.value}")
    print(f"   参数: {parameters}")
    return input("允许此任务？ (y/n): ").lower() == "y"

shield = SafetyShield(
    confirmation_callback=confirm_mission
)

mission = MissionControl(safety_shield=shield)
```

---

## 🔌 框架集成

### OpenAI Functions

```python
import openai
from orbit import MissionControl
from orbit.satellites import all_satellites

# 设置
mission = MissionControl()
mission.register_constellation(all_satellites)

# 导出为 OpenAI Functions 格式
functions = mission.export_openai_functions()

# 使用 OpenAI API
response = openai.chat.completions.create(
    model="gpt-4",
    messages=[
        {"role": "user", "content": "我的 macOS 版本是多少？"}
    ],
    functions=functions,
    function_call="auto"
)

# 执行函数调用
if response.choices[0].message.function_call:
    result = mission.execute_function_call(
        response.choices[0].message.function_call
    )
    print(f"结果: {result}")
```

### LangChain

```python
from langchain.agents import initialize_agent, AgentType
from langchain_openai import ChatOpenAI
from langchain.tools import StructuredTool
from orbit import MissionControl
from orbit.satellites import all_satellites

# 设置
mission = MissionControl()
mission.register_constellation(all_satellites)

# 转换为 LangChain 工具
langchain_tools = [
    StructuredTool.from_function(
        func=lambda **kwargs: mission.launch(sat.name, kwargs),
        name=sat.name,
        description=sat.description,
    )
    for sat in mission.constellation.list_all()
]

# 创建代理
llm = ChatOpenAI(model="gpt-4")
agent = initialize_agent(
    langchain_tools,
    llm,
    agent=AgentType.OPENAI_FUNCTIONS,
    verbose=True
)

# 运行代理
agent.run("为明天下午3点的会议创建一个笔记")
```

---

## 📋 常用操作

### 系统信息

```python
from orbit import MissionControl
from orbit.satellites import system_satellites

mission = MissionControl()
mission.register_constellation(system_satellites)

# 获取系统信息
info = mission.launch("system_get_info", {})

# 获取剪贴板
clipboard = mission.launch("system_get_clipboard", {})

# 发送通知
mission.launch("system_send_notification", {
    "title": "来自 Orbit 的问候",
    "message": "任务完成！"
})

# 截屏
mission.launch("system_take_screenshot", {
    "path": "~/Desktop/screenshot.png"
})
```

### 文件操作

```python
from orbit import MissionControl
from orbit.satellites import file_satellites

mission = MissionControl()
mission.register_constellation(file_satellites)

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

### 备忘录操作

```python
from orbit import MissionControl
from orbit.satellites import notes_satellites

mission = MissionControl()
mission.register_constellation(notes_satellites)

# 列出笔记
notes = mission.launch("notes_list", {
    "folder": "Notes"
})

# 创建笔记
mission.launch("notes_create", {
    "title": "会议记录",
    "body": "<h1>讨论要点</h1><ul><li>要点 1</li><li>要点 2</li></ul>",
    "folder": "工作"
})

# 搜索笔记
results = mission.launch("notes_search", {
    "query": "会议"
})
```

---

## 🔍 搜索和发现

### 搜索卫星

```python
from orbit import MissionControl
from orbit.satellites import all_satellites

mission = MissionControl()
mission.register_constellation(all_satellites)

# 按关键词搜索
results = mission.constellation.search("剪贴板")

for satellite in results:
    print(f"🛰️  {satellite.name}")
    print(f"   {satellite.description}")
    print(f"   类别: {satellite.category}")
    print()
```

### 按类别列出

```python
# 列出所有系统卫星
system_sats = mission.constellation.list_by_category("system")

for satellite in system_sats:
    print(f"🛰️  {satellite.name}: {satellite.description}")
```

### 按安全等级列出

```python
from orbit.satellites import SafetyLevel

# 列出所有安全卫星（只读）
safe_sats = mission.constellation.list_by_safety(SafetyLevel.SAFE)

print(f"安全卫星: {len(safe_sats)}")
```

---

## 🐛 故障排除

### 权限错误

如果遇到权限错误：

```bash
# 授予终端/系统终端辅助功能权限
# 系统设置 → 隐私与安全性 → 辅助功能
```

### AppleScript 错误

如果 AppleScript 失败：

1. 检查脚本语法
2. 验证目标应用正在运行
3. 检查应用权限

```python
from orbit.core.exceptions import AppleScriptError

try:
    result = mission.launch("notes_create", {...})
except AppleScriptError as e:
    print(f"脚本错误: {e}")
    print(f"脚本: {e.script}")
    print(f"返回码: {e.return_code}")
```

### 防护罩阻止操作

```python
from orbit.core.exceptions import ShieldError

try:
    result = mission.launch("file_delete", {"path": "/System/..."})
except ShieldError as e:
    print(f"安全阻止: {e}")
    # 如果确定要执行，使用 bypass_shield=True（不推荐）
    # result = mission.launch("file_delete", {...}, bypass_shield=True)
```

---

## 📚 下一步

- **[完整 API 参考文档](API_REFERENCE_CN.md)** - 完整 API 文档
- **[所有卫星](SATELLITES_CN.md)** - 100+ 卫星完整列表
- **[安全模型](SECURITY_CN.md)** - 安全系统深度解析
- **[框架集成示例](../examples/)** - 流行框架的代码示例

---

## 💡 提示

1. **从安全卫星开始**：先使用 `SAFE` 级别的卫星来了解系统
2. **使用防护罩**：在生产环境中始终启用安全防护罩
3. **阅读示例**：查看 `examples/` 目录中的完整工作示例
4. **处理错误**：始终用 try-except 块包装任务发射
5. **记录任务**：启用日志以跟踪任务执行

---

## 需要帮助？

- GitHub Issues: https://github.com/yourusername/orbit/issues
- Discord: https://discord.gg/orbit
- Email: support@orbit.dev

🛸 祝您运行愉快！
