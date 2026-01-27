# Orbit Terminology

> **Version:** 1.0
> **Last Updated:** 2026-01-27

---

## 📖 Core Terminology

| English | Chinese | Traditional | Notes |
|---------|---------|-------------|-------|
| **Orbit** | Orbit | macagent-tools | Project name |
| **Satellite** | 卫星 | Tool/工具 | Single automation tool |
| **Constellation** | 星座 | Registry/注册表 | Tool registry |
| **Mission Control** | 任务控制中心 | Framework | Main entry class |
| **Launcher** | 发射器 | Runner/运行器 | Executor |
| **Shield** | 防护罩 | Safety Checker/安全检查器 | Safety system |
| **Mission** | 任务 | Execution/执行 | Tool call |
| **Launch** | 发射 | Execute/运行 | Run tool |
| **Station** | 站点 | Category/分类 | Tool category |
| **Coordinates** | 坐标 | Parameters/参数 | Tool parameters |
| **Telemetry** | 遥测 | System Info/系统信息 | System data |

---

## 🎯 Code Naming Conventions

### Package and Modules

```python
# Package name
orbit/                    # Software package

# Core modules
orbit.core.satellite      # Satellite base class
orbit.core.constellation  # Constellation registry
orbit.core.launcher       # Launcher
orbit.core.shield         # Safety shield

# Satellite modules
orbit.satellites.system   # System satellites
orbit.satellites.files    # File satellites
orbit.satellites.apps     # Application satellites
```

### Class Naming

```python
# Core classes
MissionControl            # Mission Control Center
Satellite                 # Satellite (tool)
Constellation             # Constellation (registry)
Launcher                  # Launcher (runner)
SafetyShield              # Safety Shield
```

### Function and Methods

```python
# Main operations
mission.launch()          # Launch a mission
mission.register()        # Register a satellite
constellation.list_all()  # List all satellites
shield.validate()         # Validate safety
```

### Constants and Enums

```python
# Safety levels
SafetyLevel.SAFE          # Safe
SafetyLevel.MODERATE      # Moderate
SafetyLevel.DANGEROUS     # Dangerous
SafetyLevel.CRITICAL      # Critical

# Shield actions
ShieldAction.ALLOW                    # Allow
ShieldAction.DENY                     # Deny
ShieldAction.REQUIRE_CONFIRMATION     # Require confirmation
```

---

## 🎨 Brand Terms

### Visual Elements

| English | Chinese | Notes |
|---------|---------|-------|
| UFO emoji | UFO 表情 | 🛸 Primary icon |
| Deep Space Blue | 深空蓝 | #1E3A5F Primary color |
| Orbit Cyan | 轨道青 | #00D4FF Accent color |
| Satellite Silver | 卫星银 | #E8E8E8 Secondary color |
| Void Black | 虚空黑 | #0D1117 Background color |
| Star White | 星光白 | #FFFFFF Primary text color |

### Slogans and Taglines

| English | Chinese |
|---------|---------|
| "Put macOS automation in orbit" | "让 macOS 自动化进入轨道" |
| "Your AI's bridge to macOS" | "您的 AI 桥接到 macOS" |
| "macOS automation, orbiting perfectly" | "macOS 自动化，完美运行" |

---

## 🛠️ Technical Terms

### Satellite Categories

| English | Chinese | Description |
|---------|---------|-------------|
| System Telemetry | 系统遥测 | System information tools |
| File Communications | 文件通讯 | File operation tools |
| App Stations | 应用站点 | Application-specific tools |
| Network | 网络 | Network/WiFi tools |
| Application Control | 应用控制 | Application lifecycle management |

### Safety Related

| English | Chinese | Notes |
|---------|---------|-------|
| Safety Level | 安全等级 | SAFE/MODERATE/DANGEROUS/CRITICAL |
| Shield Action | 防护动作 | ALLOW/DENY/REQUIRE_CONFIRMATION |
| Protected Path | 受保护路径 | Forbidden operation paths |
| Dangerous Command | 危险命令 | Forbidden command patterns |
| Confirmation Callback | 确认回调 | User confirmation function |

### Operation Related

| English | Chinese | Notes |
|---------|---------|-------|
| Launch Mission | 发射任务 | Execute tool |
| Register Satellite | 注册卫星 | Add tool to registry |
| Constellation | 星座 | Tool collection |
| Orbit | 轨道 | Project name |
| Telemetry | 遥测 | System data collection |

---

## 📝 Documentation Writing Guidelines

### DO (Recommended Practices)

✅ Use Orbit terminology:
```python
# Register satellite to constellation
mission.register_satellite(satellite)
```

✅ Use space theme:
```markdown
🛰️ Launch a satellite to get system information
```

✅ Keep consistency:
```python
MissionControl    # Mission Control Center
Constellation     # Constellation
Launcher          # Launcher
```

### DON'T (Avoid Practices)

❌ Don't use traditional terminology:
```python
# Avoid: register_tool()
# Recommended: register_satellite()
```

❌ Don't mix usage:
```python
# Avoid: mission.execute_tool()
# Recommended: mission.launch()
```

❌ Don't ignore branding:
```markdown
# Avoid: macOS Tools
# Recommended: Orbit - macOS Automation Toolkit
```

---

## 🌐 Localization Considerations

### Chinese-English Mixed Rules

1. **Code and terminology**: Keep in English
```python
from orbit import MissionControl  # Don't translate
```

2. **Comments and documentation**: Use Chinese
```python
# 发射任务获取系统信息
result = mission.launch("system_get_info", {})
```

3. **User interface**: Provide bilingual
```python
class MissionControl:
    """任务控制中心 - Mission Control Center"""
```

### Technical Document Translation

**English document structure:**
- README.md
- docs/DESIGN.md
- docs/QUICKSTART.md

**Chinese document structure:**
- README_CN.md
- docs/DESIGN_CN.md
- docs/QUICKSTART_CN.md

---

## 📖 Quick Reference

### Common Phrases

| English | Chinese |
|---------|---------|
| "Launch a satellite" | "发射卫星" |
| "Register constellation" | "注册星座" |
| "Shield validation" | "防护罩验证" |
| "Mission executed" | "任务执行完成" |
| "Safety level" | "安全等级" |
| "Protected path" | "受保护路径" |
| "Orbit your macOS" | "让您的 macOS 进入轨道" |

### Code Comment Template

```python
class MissionControl:
    """
    Mission Control Center

    Main entry point for Orbit. Manages satellite constellation
    and mission execution.

    Example:
        >>> mission = MissionControl()
        >>> mission.register_constellation(all_satellites)
        >>> result = mission.launch("system_get_info", {})
    """
```

---

## 🔄 Terminology Evolution

### Version History

| Version | Changes | Date |
|---------|---------|------|
| 1.0 | Initial terminology definitions | 2026-01-27 |

### Future Updates

This document will be updated as Orbit evolves. Suggestions for improvements are welcome.

---

**Terminology Version:** 1.0
**Last Updated:** 2026-01-27

🛸 Maintain consistent terminology to build a strong Orbit brand!
