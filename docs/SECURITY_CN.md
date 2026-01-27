# Orbit 安全模型

> **版本：** 1.0
> **最后更新：** 2026-01-27

---

## 🛡️ 概述

Orbit 的安全模型旨在保护您的 Mac，同时实现强大的自动化功能。**防护罩系统**提供多层安全控制，无需对每个操作进行明确批准。

---

## 🔐 安全架构

### 四级安全系统

每个卫星被归类为四个安全等级之一：

| 等级 | 描述 | 示例 | 默认操作 |
|------|------|------|----------|
| **SAFE（安全）** | 只读操作，无副作用 | 获取系统信息、读取剪贴板、列出文件 | ✅ 允许 |
| **MODERATE（中等）** | 创建/修改操作，数据变更 | 创建笔记、设置剪贴板、写入文件 | ⚠️ 确认 |
| **DANGEROUS（危险）** | 删除操作，不可逆 | 删除文件、清空废纸篓、删除笔记 | ⚠️ 确认 |
| **CRITICAL（严重）** | 系统级操作 | 终端执行、系统文件修改 | 🚫 阻止 |

### 按类别的安全分类

```
系统遥测：
  └─ 大多数操作：SAFE
  └─ 系统更改：MODERATE

文件通讯：
  ├─ 读取操作：SAFE
  ├─ 写入操作：MODERATE
  └─ 删除操作：DANGEROUS

应用站点：
  ├─ 读取/列出：SAFE
  ├─ 创建/更新：MODERATE
  └─ 删除：DANGEROUS

网络：
  └─ 所有操作：MODERATE

应用控制：
  ├─ 列出：SAFE
  └─ 启动/退出：MODERATE
```

---

## 🚦 防护罩配置

### 默认行为

```python
from orbit import MissionControl

# 使用默认防护罩配置
mission = MissionControl()

# 默认规则：
# SAFE       -> 允许
# MODERATE   -> 需要确认
# DANGEROUS  -> 需要确认
# CRITICAL   -> 阻止
```

### 自定义规则

```python
from orbit import MissionControl, SafetyShield, SafetyLevel

# 严格模式：仅允许 SAFE 级别
strict_shield = SafetyShield(
    rules={
        SafetyLevel.SAFE: "allow",
        SafetyLevel.MODERATE: "deny",
        SafetyLevel.DANGEROUS: "deny",
        SafetyLevel.CRITICAL: "deny"
    }
)

mission = MissionControl(safety_shield=strict_shield)
```

### 宽松模式（仅开发环境）

```python
# 允许所有操作（不推荐用于生产环境）
permissive_shield = SafetyShield(
    rules={
        SafetyLevel.SAFE: "allow",
        SafetyLevel.MODERATE: "allow",
        SafetyLevel.DANGEROUS: "allow",
        SafetyLevel.CRITICAL: "allow"
    }
)

mission = MissionControl(safety_shield=permissive_shield)
```

---

## ✅ 用户确认

### 内置确认回调

```python
from orbit import SafetyShield

def confirm_mission(satellite, parameters):
    """交互式确认提示"""
    print(f"\n{'='*60}")
    print(f"🛰️  卫星: {satellite.name}")
    print(f"📋 描述: {satellite.description}")
    print(f"⚠️  安全等级: {satellite.safety_level.value}")
    print(f"📝 参数:")
    for key, value in parameters.items():
        print(f"   - {key}: {value}")
    print(f"{'='*60}")

    response = input("允许此任务？ (y/n): ").lower().strip()
    return response == 'y'

shield = SafetyShield(
    confirmation_callback=confirm_mission
)
```

### 编程式确认

```python
def auto_approve_safe(satellite, parameters):
    """自动批准 SAFE 级别，确认其他"""
    if satellite.safety_level == SafetyLevel.SAFE:
        return True
    return ask_user(satellite, parameters)

shield = SafetyShield(confirmation_callback=auto_approve_safe)
```

### GUI 确认（高级）

```python
import tkinter as tk
from tkinter import messagebox

def gui_confirmation(satellite, parameters):
    """显示 GUI 确认对话框"""
    root = tk.Tk()
    root.withdraw()  # 隐藏主窗口

    title = f"Orbit 防护罩 - {satellite.safety_level.value.upper()}"
    message = f"允许卫星 '{satellite.name}'？\n\n参数:\n"
    for key, value in parameters.items():
        message += f"  {key}: {value}\n"

    result = messagebox.askyesno(title, message)
    root.destroy()
    return result

shield = SafetyShield(confirmation_callback=gui_confirmation)
```

---

## 🚫 受保护资源

### 默认受保护路径

以下路径默认受保护：

```python
PROTECTED_PATHS = [
    "/",              # 根目录
    "/System",        # 系统文件
    "/Library",       # 库目录
    "/usr",           # Unix 工具
    "/bin",           # 二进制文件
    "/sbin",          # 系统二进制文件
    "/etc",           # 配置文件
]
```

### 自定义受保护路径

```python
from pathlib import Path
from orbit import SafetyShield

shield = SafetyShield(
    protected_paths=[
        Path("/"),
        Path("/System"),
        Path("/Library"),
        Path("/usr"),
        Path("~/Documents"),      # 保护文档
        Path("~/Desktop"),        # 保护桌面
        Path("~/Pictures"),       # 保护图片
    ]
)
```

### 添加/移除受保护路径

```python
shield = SafetyShield()

# 添加额外保护
shield.add_protected_path("~/Projects")
shield.add_protected_path("~/Important")

# 移除保护（谨慎使用）
shield.remove_protected_path("~/Desktop")
```

---

## ⚠️ 危险命令检测

### 默认阻止命令

```python
DANGEROUS_COMMANDS = [
    "rm -rf /",            # 删除根目录
    "dd if=/dev/zero",     # 磁盘擦除
    ":(){ :|:& };:",       # Fork 炸弹
    "mkfs",                # 格式化文件系统
    "chmod 000",           # 移除权限
    "chown root",          # 更改所有者为 root
    "mv / System",         # 移动系统目录
]
```

### 自定义危险模式

```python
shield = SafetyShield(
    dangerous_commands=[
        "rm -rf",
        "dd if=/dev/zero",
        "mkfs",
        "chmod 000",
        "format",
        "del /Q",          # Windows
        "rmdir /S",        # Windows
    ]
)
```

---

## 🔒 权限要求

### macOS 权限

Orbit 根据使用的卫星需要各种 macOS 权限：

#### 辅助功能（必需）

**用于：** 应用控制、系统级操作

**如何启用：**
```
系统设置 → 隐私与安全性 → 辅助功能
→ 添加终端 / Python / 您的 IDE
```

#### 完全磁盘访问（可选）

**用于：** 访问所有文件（包括系统文件）

**如何启用：**
```
系统设置 → 隐私与安全性 → 完全磁盘访问
→ 添加终端 / Python
```

#### 自动化（应用特定）

**用于：** 控制特定应用

**如何启用：**
```
系统设置 → 隐私与安全性 → 自动化
→ 允许终端控制：
  - 备忘录
  - 日历
  - 提醒事项
  - 音乐
  - 等等
```

### 检查权限

```python
from orbit import MissionControl

mission = MissionControl()

# 检查是否授予所需权限
permissions = mission.check_permissions()

for permission, granted in permissions.items():
    status = "✅ 已授予" if granted else "❌ 缺失"
    print(f"{permission}: {status}")
```

---

## 🚨 安全最佳实践

### 1. 永不禁用防护罩

```python
# ❌ 错误：禁用安全
result = mission.launch("dangerous_operation", {...}, bypass_shield=True)

# ✅ 正确：保持防护罩启用
result = mission.launch("dangerous_operation", {...})
```

### 2. 生产环境使用确认

```python
# ✅ 正确：生产环境始终确认
shield = SafetyShield(
    confirmation_callback=production_confirmation_callback
)
```

### 3. 白名单批准操作

```python
# ✅ 正确：仅注册安全卫星
from orbit.satellites import system_satellites

mission = MissionControl()
for satellite in system_satellites:
    if satellite.safety_level == SafetyLevel.SAFE:
        mission.register(satellite)
```

### 4. 审计任务日志

```python
import logging
from orbit import MissionControl

# 启用日志
logging.basicConfig(level=logging.INFO)
mission = MissionControl()

# 所有任务都被记录
mission.launch("notes_create", {...})
# 输出: INFO:orbit.launcher:发射任务 'notes_create'，参数 {...}
```

### 5. 验证参数

```python
from orbit import MissionControl

def validate_parameters(satellite, parameters):
    """自定义参数验证"""
    if satellite.name == "file_delete":
        path = parameters.get("path", "")
        if path.startswith("/System"):
            raise ValueError("无法删除系统文件")
    return True

shield = SafetyShield(
    pre_validator=validate_parameters
)
```

---

## 🔄 安全审计

### 查看卫星分类

```python
from orbit import MissionControl
from orbit.satellites import all_satellites

mission = MissionControl()
mission.register_constellation(all_satellites)

# 按安全等级分组
for level in ["safe", "moderate", "dangerous", "critical"]:
    satellites = mission.constellation.list_by_safety(
        SafetyLevel[level.upper()]
    )
    print(f"\n{level.upper()} ({len(satellites)} 个卫星):")
    for sat in satellites:
        print(f"  - {sat.name}")
```

### 安全报告

```python
from orbit import MissionControl
from orbit.satellites import all_satellites

mission = MissionControl()
mission.register_constellation(all_satellites)

# 生成安全报告
report = mission.constellation.get_stats()

print("Orbit 安全报告")
print("=" * 60)
print(f"卫星总数: {report['total_satellites']}")
print(f"类别数: {report['categories']}")
print("\n按安全等级:")
for level, count in report['by_safety'].items():
    print(f"  {level}: {count}")
```

---

## 🐛 安全测试

### 测试防护罩行为

```python
import pytest
from orbit import SafetyShield, SafetyLevel
from orbit.core.exceptions import ShieldError

def test_protected_path_blocking():
    shield = SafetyShield()

    # 尝试访问受保护路径
    with pytest.raises(ShieldError):
        shield._check_path("/System")

def test_dangerous_command_blocking():
    shield = SafetyShield()

    # 尝试执行危险命令
    with pytest.raises(ShieldError):
        shield._check_command("rm -rf /")

def test_safety_level_enforcement():
    from orbit.satellites import Satellite

    # 创建 CRITICAL 级别卫星
    critical_sat = Satellite(
        name="critical_operation",
        description="严重测试",
        category="test",
        parameters=[],
        safety_level=SafetyLevel.CRITICAL,
        applescript_template=""
    )

    shield = SafetyShield()  # 默认 CRITICAL -> DENY

    with pytest.raises(ShieldError):
        shield.validate(critical_sat, {})
```

---

## 📖 参考资料

- [防护罩 API 参考](API_REFERENCE_CN.md#防护罩)
- [异常处理](API_REFERENCE_CN.md#异常)
- [权限设置指南](TROUBLESHOOTING_CN.md#权限)
- [安全最佳实践](https://owasp.org/)

---

**安全模型版本：** 1.0
**最后更新：** 2026-01-27

🛡️ 保持安全，安全运行！
