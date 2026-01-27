# 为 Orbit 贡献

> **版本：** 1.0.0
> **最后更新：** 2026-01-27

感谢您对 Orbit 的贡献兴趣！本文档提供了项目贡献的指南和说明。

---

## 📋 目录

1. [行为准则](#行为准则)
2. [快速开始](#快速开始)
3. [开发流程](#开发流程)
4. [代码规范](#代码规范)
5. [测试指南](#测试指南)
6. [文档编写](#文档编写)
7. [提交更改](#提交更改)

---

## 行为准则

### 我们的承诺

我们致力于为所有贡献者提供一个热情和包容的环境。请：

- 保持尊重和体贴
- 使用热情和包容的语言
- 在反馈中保持建设性
- 关注社区的最佳利益

### 报告问题

如果您遇到任何问题或有疑虑，请联系我们：
- GitHub Issues: https://github.com/xiaoxiath/orbit/issues
- Email: support@orbit.dev

---

## 快速开始

### 前置要求

- Python 3.10 或更高版本
- macOS 12.0+（用于测试）
- Git
- Poetry（依赖管理）

### 设置开发环境

```bash
# 克隆仓库
git clone https://github.com/xiaoxiath/orbit.git
cd orbit

# 安装依赖
poetry install --with dev

# 激活虚拟环境
poetry shell

# 运行测试
pytest

# 运行代码检查
ruff check .
black --check .
```

### 推荐工具

- **IDE**: VS Code、PyCharm 或任何支持类型提示的 Python IDE
- **Git 客户端**: GitHub Desktop、SourceTree 或命令行
- **测试工具**: pytest 和覆盖率报告

---

## 开发流程

### 1. Fork 和克隆

```bash
# 在 GitHub 上 fork 仓库
# 克隆您的 fork
git clone https://github.com/YOUR_USERNAME/orbit.git
cd orbit
```

### 2. 创建分支

```bash
git checkout -b feature/your-feature-name
# 或
git checkout -b fix/your-bug-fix
```

### 分支命名约定

- `feature/` - 新功能
- `fix/` - 错误修复
- `docs/` - 文档更新
- `refactor/` - 代码重构
- `test/` - 测试添加/更新

### 3. 进行更改

按照我们的编码规范（见下文）编辑代码。

### 4. 测试更改

```bash
# 运行所有测试
pytest

# 运行特定测试
pytest tests/core/test_satellite.py

# 运行并生成覆盖率报告
pytest --cov=orbit --cov-report=html

# 打开覆盖率报告
open htmlcov/index.html
```

### 5. 提交更改

```bash
git add .
git commit -m "feat: 添加 X 的新卫星"
```

### 提交消息格式

遵循约定式提交（Conventional Commits）：

```
<type>(<scope>): <subject>

<body>

<footer>
```

**类型：**
- `feat`: 新功能
- `fix`: 错误修复
- `docs`: 文档更改
- `refactor`: 代码重构
- `test`: 测试更改
- `chore`: 维护任务

**示例：**
```
feat(notes): 添加 notes_search 卫星

实现新的卫星用于搜索 Apple Notes 中的笔记。
该卫星支持按标题和正文内容搜索。

Closes #123
```

### 6. 推送并创建 PR

```bash
git push origin feature/your-feature-name
```

然后在 GitHub 上创建 Pull Request。

---

## 代码规范

### Python 风格指南

遵循 PEP 8 和我们的修改：

```python
# 好的示例
from orbit import MissionControl
from orbit.core import Satellite, SafetyLevel


def launch_mission(satellite_name: str, parameters: dict) -> Any:
    """使用给定卫星发射任务。

    Args:
        satellite_name: 要发射的卫星名称
        parameters: 任务参数

    Returns:
        任务结果

    Raises:
        SatelliteNotFoundError: 如果卫星未找到
    """
    mission = MissionControl()
    return mission.launch(satellite_name, parameters)
```

### 类型提示

所有函数必须具有类型提示：

```python
from typing import Optional, List, Dict, Any


def process_result(
    data: Dict[str, Any],
    parser: Optional[Callable] = None
) -> List[str]:
    ...
```

### 文档字符串

使用 Google 风格的文档字符串：

```python
def satellite_function(param1: str, param2: int) -> bool:
    """函数的简短描述。

    如果需要，更长的描述。

    Args:
        param1: param1 的描述
        param2: param2 的描述

    Returns:
        返回值的描述

    Raises:
        ValueError: 如果 param1 无效
    """
    pass
```

### 命名约定

- **模块**: `lowercase_with_underscores`
- **类**: `CapitalizedWords`
- **函数/方法**: `lowercase_with_underscores`
- **常量**: `UPPERCASE_WITH_UNDERSCORES`
- **私有**: `_leading_underscore`

---

## 测试指南

### 测试结构

```python
# tests/satellites/test_notes.py
import pytest
from orbit.satellites.notes import create
from orbit.core import SafetyLevel


class TestNotesCreate:
    """notes_create 卫星的测试。"""

    def test_launch_creates_note(self):
        """测试发射会创建笔记。"""
        satellite = create.notes_create
        assert satellite.name == "notes_create"
        assert satellite.safety_level == SafetyLevel.MODERATE

    def test_launch_with_title_only(self):
        """测试仅使用标题参数发射。"""
        # 测试实现
        pass

    @pytest.mark.integration
    def test_integration_with_notes_app(self):
        """与备忘录应用的集成测试。"""
        # 仅在使用 pytest -m integration 时运行
        pass
```

### 测试类别

- **单元测试**: 快速、隔离的测试
- **集成测试**: 需要 macOS/应用的测试
- **安全测试**: 安全验证测试

### 运行测试

```bash
# 仅单元测试
pytest tests/

# 集成测试
pytest -m integration

# 带覆盖率
pytest --cov=orbit --cov-report=term-missing
```

### 测试覆盖率

目标是 >80% 的代码覆盖率。检查覆盖率报告：

```bash
pytest --cov=orbit --cov-report=html
open htmlcov/index.html
```

---

## 文档编写

### 代码文档

所有代码必须包含：
- 类型提示
- 所有公共函数/类的文档字符串
- 复杂逻辑的内联注释

### 卫星文档

添加新卫星时：

1. 添加到 `docs/SATELLITES_CN.md`
2. 添加到 `docs/SATELLITES.md`
3. 包含使用示例
4. 记录安全等级

### 文档示例

```markdown
## 新卫星

### 卫星

| 卫星 | 安全等级 | 描述 |
|------|----------|------|
| `new_satellite` | SAFE | 描述它的作用 |

### 使用示例

```python
mission.launch("new_satellite", {"param": "value"})
```
```

---

## 提交更改

### Pull Request 检查清单

提交 PR 之前，确保：

- [ ] 代码遵循编码规范
- [ ] 所有测试通过
- [ ] 为新功能添加新测试
- [ ] 文档已更新
- [ ] 提交消息遵循约定
- [ ] PR 描述清楚地解释了更改

### Pull Request 模板

```markdown
## 描述
更改的简短描述

## 更改类型
- [ ] 错误修复
- [ ] 新功能
- [ ] 破坏性更改
- [ ] 文档更新

## 测试
如何测试此更改？

## 检查清单
- [ ] 测试通过
- [ ] 文档已更新
- [ ] 无破坏性更改（或已记录）
```

### 审查流程

1. 运行自动检查（测试、代码检查）
2. 维护者审查代码
3. 提供反馈（如果有）
4. 解决反馈
5. 批准并合并

---

## 添加卫星

### 卫星模板

```python
from orbit.core import Satellite, SatelliteParameter, SafetyLevel

my_satellite = Satellite(
    name="category_action",
    description="清楚地描述这个卫星的作用",
    category="category",
    parameters=[
        SatelliteParameter(
            name="param_name",
            type="string",
            description="参数描述",
            required=True
        )
    ],
    safety_level=SafetyLevel.SAFE,
    applescript_template="""
    tell application "AppName"
        {{ action_script }}
    end tell
    """,
    result_parser=lambda x: {"result": x},
    examples=[
        {
            "input": {"param": "value"},
            "output": {"result": "expected"}
        }
    ]
)
```

### 最佳实践

1. **安全优先**: 选择适当的安全等级
2. **清晰的描述**: 帮助 LLM 理解卫星
3. **错误处理**: 优雅地处理常见失败
4. **示例**: 提供清晰的使用示例
5. **测试**: 添加全面的测试

---

## 获取帮助

### 资源

- **文档**: [docs/INDEX_CN.md](docs/INDEX_CN.md)
- **API 参考**: [docs/API_REFERENCE_CN.md](docs/API_REFERENCE_CN.md)
- **问题**: https://github.com/xiaoxiath/orbit/issues
- **讨论**: https://github.com/xiaoxiath/orbit/discussions

### 联系方式

- **Email**: support@orbit.dev
- **GitHub**: @xiaoxiath

---

## 致谢

贡献者将：
- 在 CONTRIBUTORS.md 中列出
- 在发布说明中提及
- 邀请加入维护者（对于重大贡献）

感谢您为 Orbit 做出贡献！🛸

---

**贡献指南版本：** 1.0.0
**最后更新：** 2026-01-27
