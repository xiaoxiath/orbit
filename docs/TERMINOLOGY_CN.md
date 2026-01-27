# Orbit 术语对照表

> **版本：** 1.0
> **Orbit 术语系统**

---

## 📖 核心术语对照

| 英文术语 | 中文术语 | 传统术语 | 说明 |
|----------|----------|----------|------|
| **Orbit** | Orbit（轨道） | macagent-tools | 项目名称 |
| **Satellite** | 卫星 | Tool/工具 | 单个自动化工具 |
| **Constellation** | 星座 | Registry/注册表 | 工具注册表 |
| **Mission Control** | 任务控制中心 | Framework | 主入口类 |
| **Launcher** | 发射器 | Runner/运行器 | 执行器 |
| **Shield** | 防护罩 | Safety Checker/安全检查器 | 安全系统 |
| **Mission** | 任务 | Execution/执行 | 工具调用 |
| **Launch** | 发射 | Execute/执行 | 运行工具 |
| **Station** | 站点 | Category/分类 | 工具类别 |
| **Coordinates** | 坐标 | Parameters/参数 | 工具参数 |
| **Flight Log** | 飞行日志 | Documentation/文档 | 文档 |
| **Telemetry** | 遥测 | System Info/系统信息 | 系统数据 |

---

## 🎯 代码命名规范

### 包和模块

```python
# 包名
orbit/                    # 软件包

# 核心模块
orbit.core.satellite      # 卫星基类
orbit.core.constellation  # 星座注册表
orbit.core.launcher       # 发射器
orbit.core.shield         # 防护罩

# 卫星模块
orbit.satellites.system   # 系统卫星
orbit.satellites.files    # 文件卫星
orbit.satellites.apps     # 应用卫星
```

### 类命名

```python
# 核心类
MissionControl            # 任务控制中心（主入口）
Satellite                 # 卫星（工具）
Constellation             # 星座（注册表）
Launcher                  # 发射器（运行器）
SafetyShield              # 安全防护罩
```

### 函数和方法

```python
# 主要操作
mission.launch()          # 发射任务
mission.register()        # 注册卫星
constellation.list_all()  # 列出所有卫星
shield.validate()         # 验证安全性
```

### 常量和枚举

```python
# 安全等级
SafetyLevel.SAFE          # 安全
SafetyLevel.MODERATE      # 中等
SafetyLevel.DANGEROUS     # 危险
SafetyLevel.CRITICAL      # 严重

# 防护罩动作
ShieldAction.ALLOW                    # 允许
ShieldAction.DENY                     # 阻止
ShieldAction.REQUIRE_CONFIRMATION     # 需要确认
```

---

## 📚 术语使用示例

### 示例 1：基础使用

```python
from orbit import MissionControl

# 初始化任务控制中心
mission = MissionControl()

# 注册卫星
mission.register(system_satellite)

# 发射任务
result = mission.launch(
    "system_get_info",
    parameters={}
)
```

### 示例 2：星座管理

```python
# 列出所有卫星
all_satellites = mission.constellation.list_all()

# 按类别列出
system_satellites = mission.constellation.list_by_category("system")

# 按安全等级列出
safe_satellites = mission.constellation.list_by_safety(SafetyLevel.SAFE)
```

### 示例 3：防护罩配置

```python
from orbit import SafetyShield, SafetyLevel

# 创建防护罩
shield = SafetyShield(
    rules={
        SafetyLevel.SAFE: "allow",
        SafetyLevel.MODERATE: "confirm"
    }
)

mission = MissionControl(safety_shield=shield)
```

---

## 🎨 品牌术语

### 视觉元素

| 英文 | 中文 | 说明 |
|------|------|------|
| UFO emoji | UFO 表情 | 🛸 主要图标 |
| Deep Space Blue | 深空蓝 | #1E3A5F 主色 |
| Orbit Cyan | 轨道青 | #00D4FF 强调色 |
| Satellite Silver | 卫星银 | #E8E8E8 次要色 |
| Void Black | 虚空黑 | #0D1117 背景色 |
| Star White | 星光白 | #FFFFFF 主文本 |

### 标语和口号

| 英文 | 中文 |
|------|------|
| "Put macOS automation in orbit" | "让 macOS 自动化进入轨道" |
| "Your AI's bridge to macOS" | "您的 AI 桥接到 macOS" |
| "macOS automation, orbiting perfectly" | "macOS 自动化，完美运行" |

---

## 🛠️ 技术术语翻译

### 卫星分类

| 英文类别 | 中文类别 | 说明 |
|----------|----------|------|
| System Telemetry | 系统遥测 | 系统信息类工具 |
| File Communications | 文件通讯 | 文件操作工具 |
| App Stations | 应用站点 | 应用特定工具 |
| Network | 网络 | 网络/WiFi 工具 |
| Application Control | 应用控制 | 应用生命周期管理 |

### 安全相关

| 英文 | 中文 | 说明 |
|------|------|------|
| Safety Level | 安全等级 | SAFE/MODERATE/DANGEROUS/CRITICAL |
| Shield Action | 防护动作 | ALLOW/DENY/REQUIRE_CONFIRMATION |
| Protected Path | 受保护路径 | 禁止操作的路径 |
| Dangerous Command | 危险命令 | 禁止执行的命令 |
| Confirmation Callback | 确认回调 | 用户确认函数 |

### 操作相关

| 英文 | 中文 | 说明 |
|------|------|------|
| Launch Mission | 发射任务 | 执行工具 |
| Register Satellite | 注册卫星 | 添加工具到注册表 |
| Constellation | 星座 | 工具集合 |
| Orbit | 轨道 | 项目名称 |
| Telemetry | 遥测 | 系统数据采集 |

---

## 📝 文档写作指南

### DO（推荐做法）

✅ 使用 Orbit 术语：
```python
# 注册卫星到星座
mission.register_satellite(satellite)
```

✅ 使用太空主题：
```markdown
🛰️ 发射卫星获取系统信息
```

✅ 保持一致性：
```python
MissionControl    # 任务控制中心
Constellation     # 星座
Launcher          # 发射器
```

### DON'T（避免做法）

❌ 不要使用传统术语：
```python
# 避免：register_tool
# 推荐：register_satellite
```

❌ 不要混合使用：
```python
# 避免：mission.execute_tool()
# 推荐：mission.launch()
```

❌ 不要忽略品牌：
```markdown
# 避免：macOS Tools
# 推荐：Orbit - macOS Automation Toolkit
```

---

## 🌐 本地化注意事项

### 中英文混排规则

1. **代码和术语**：保持英文
```python
from orbit import MissionControl  # 不翻译
```

2. **注释和文档**：使用中文
```python
# 发射任务获取系统信息
result = mission.launch("system_get_info", {})
```

3. **用户界面**：提供双语
```python
class MissionControl:
    """任务控制中心 - Mission Control Center"""
```

### 技术文档翻译

**英文文档结构：**
- README_ORBIT.md
- docs/DESIGN.md
- docs/QUICKSTART.md

**中文文档结构：**
- README_CN.md
- docs/DESIGN_CN.md
- docs/QUICKSTART_CN.md

---

## 📖 快速参考

### 常用短语对照

| English | 中文 |
|---------|------|
| "Launch a satellite" | "发射卫星" |
| "Register constellation" | "注册星座" |
| "Shield validation" | "防护罩验证" |
| "Mission executed" | "任务执行完成" |
| "Safety level" | "安全等级" |
| "Protected path" | "受保护路径" |
| "Orbit your macOS" | "让您的 macOS 进入轨道" |

### 代码注释模板

```python
class MissionControl:
    """
    任务控制中心

    Orbit 的主入口类，管理卫星星座和任务发射。

    Example:
        >>> mission = MissionControl()
        >>> mission.register_constellation(all_satellites)
        >>> result = mission.launch("system_get_info", {})
    """
```

---

**术语表版本：** 1.0
**最后更新：** 2026-01-27

🛸 保持术语一致，建立强大的 Orbit 品牌！
