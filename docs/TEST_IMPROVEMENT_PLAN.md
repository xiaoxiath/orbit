# Orbit 测试改进和 Bug 修复计划

> **目标**: 消除隐藏 bug，建立可靠的测试体系
> **日期**: 2026-01-27

---

## 🔍 问题诊断

### 当前测试体系的致命缺陷

1. **100% Mock 测试**
   - ❌ 不执行真实 AppleScript
   - ❌ 无法发现语法错误
   - ❌ 无法发现模板渲染问题
   - ❌ 无法发现 macOS 兼容性问题

2. **测试覆盖率虚高**
   - ✅ 代码覆盖率: 65%
   - ❌ 实际价值: 接近 0%
   - ❌ Mock 覆盖了所有真实执行路径

3. **缺少关键测试类型**
   - ❌ 无 AppleScript 语法测试
   - ❌ 无真实 macOS 执行测试
   - ❌ 无集成测试
   - ❌ 无端到端测试

---

## 📋 改进计划

### Phase 1: 立即行动（今天）

#### 1.1 创建静态检查脚本
```bash
scripts/check_satellites.sh
- 检查 AppleScript 语法
- 查找常见错误模式
- 验证模板语法
```

#### 1.2 修复已发现的 bug
- [x] launcher.py - satellite 参数
- [x] files.py - my_list() 函数
- [ ] files.py - {{ var|lower }} 语法
- [ ] 其他卫星的类似问题

#### 1.3 创建预提交钩子
```bash
.git/hooks/pre-commit
- 运行静态检查
- 运行快速测试
- 阻止有问题的代码提交
```

---

### Phase 2: 建立真实测试体系

#### 2.1 集成测试
```python
tests/integration/
├── test_applescript_execution.py
├── test_template_rendering.py
├── test_permission_handling.py
└── test_macos_compatibility.py
```

#### 2.2 语法验证测试
```python
def test_applescript_syntax():
    """验证所有卫星的 AppleScript 语法"""
    for satellite in all_satellites:
        script = render_template(satellite)
        assert can_compile_applescript(script)
```

#### 2.3 真实执行测试（标记为慢速）
```python
@pytest.mark.slow
@pytest.mark.requires_macos
def test_real_execution():
    """在真实 macOS 上执行"""
    # 测试关键卫星的实际执行
```

---

### Phase 3: 质量保证工具

#### 3.1 静态分析工具
```yaml
工具:
  - mypy: 类型检查
  - ruff: linting + 快速
  - pylint: 深度检查
  - bandit: 安全检查
```

#### 3.2 CI/CD 集成
```yaml
.github/workflows/test.yml
- 每次提交运行完整测试套件
- PR 必须通过所有检查
- 自动运行慢速测试（每周）
```

#### 3.3 覆盖率目标
- 语句覆盖率: 80%+
- 分支覆盖率: 70%+
- **真实执行覆盖率**: 50%+

---

## 🛠️ 具体实现

### Step 1: 静态分析工具配置

创建 `scripts/static_analysis.sh`:
```bash
#!/bin/bash
echo "🔍 Running static analysis..."

# Type checking
echo "1️⃣  Type checking (mypy)..."
mypy src/orbit/

# Linting
echo "2️⃣  Linting (ruff)..."
ruff check src/orbit/

# Security check
echo "3️⃣  Security check (bandit)..."
bandit -r src/orbit/

# AppleScript syntax check
echo "4️⃣  AppleScript syntax check..."
python3 scripts/check_applescript.py

echo "✅ Static analysis complete!"
```

### Step 2: 预提交钩子

创建 `.git/hooks/pre-commit`:
```bash
#!/bin/bash
echo "🔍 Pre-commit checks..."

# Run static analysis
bash scripts/static_analysis.sh

# Run quick tests
python3 -m pytest tests/test_parsers.py -v
python3 -m pytest tests/test_exceptions.py -v

# Check for common issues
python3 scripts/check_applescript.py

if [ $? -ne 0 ]; then
    echo "❌ Pre-commit checks failed!"
    echo "   Please fix the issues before committing."
    exit 1
fi

echo "✅ All checks passed!"
```

### Step 3: 改进的测试套件

创建 `tests/integration/test_applescript_real.py`:
```python
"""Test REAL AppleScript execution on macOS."""

import os
import pytest
import subprocess

pytestmark = pytest.mark.skipif(
    os.sys.platform != "darwin",
    reason="These tests require macOS"
)


class TestAppleScriptRealExecution:
    """Test actual AppleScript execution."""

    def test_simple_applescript(self):
        """Test that basic AppleScript works."""
        script = 'return "Hello from Orbit"'
        result = subprocess.run(
            ["osascript", "-e", script],
            capture_output=True,
            text=True,
            timeout=5
        )

        assert result.returncode == 0
        assert result.stdout.strip() == "Hello from Orbit"

    @pytest.mark.parametrize("satellite_name", [
        "system_get_clipboard",
        "system_get_info",
        "app_list",
    ])
    def test_critical_satellites_execution(self, satellite_name):
        """Test critical satellites can execute."""
        # Import here to avoid import errors
        from orbit import MissionControl
        from orbit.satellites.all_satellites import all_satellites
        from orbit.core import SafetyShield, SafetyLevel

        shield = SafetyShield(rules={
            SafetyLevel.SAFE: "allow",
            SafetyLevel.MODERATE: "allow",
            SafetyLevel.DANGEROUS: "allow",
            SafetyLevel.CRITICAL: "deny"
        })

        mission = MissionControl(safety_shield=shield)
        mission.register_constellation(all_satellites)

        satellite = mission.constellation.get(satellite_name)
        assert satellite is not None, f"Satellite {satellite_name} not found"

        # Get sample params
        params = {}
        for param in satellite.parameters:
            if param.default is not None:
                params[param.name] = param.default

        # Try execution (may fail due to permissions, but shouldn't crash)
        try:
            result = mission.launch(satellite_name, params)
            # If we got here without exception, the code works!
            assert True
        except Exception as e:
            # Permission errors are acceptable
            if "permission" not in str(e).lower():
                raise
```

---

## 📊 成功指标

### 测试质量指标

| 指标 | 当前 | 目标 | 如何测量 |
|------|------|------|---------|
| 代码覆盖率 | 65% | 80%+ | pytest-cov |
| 真实执行覆盖率 | ~0% | 50%+ | 新测试套件 |
| Mock 使用率 | 100% | <30% | 代码审查 |
| 静态分析 | 无 | 全面 | mypy, ruff |
| 预提交钩子 | 无 | 强制 | Git hooks |

### Bug 发现指标

| 类型 | 当前方法 | 发现率 | 改进后 |
|------|---------|--------|--------|
| 语法错误 | 用户报告 | 100% | 自动发现 |
| 运行时错误 | Mock 隐藏 | ~0% | 真实测试 |
| 类型错误 | 不检查 | 0% | mypy |
| 逻辑错误 | 偶然 | 低 | 集成测试 |

---

## 🎯 立即行动计划

### 今天（1-2 小时）

1. **创建检查脚本** (30 分钟)
   - [ ] `scripts/check_applescript.py`
   - [ ] `scripts/static_analysis.sh`
   - [ ] `scripts/pre_commit_hook.sh`

2. **修复已知 bug** (30 分钟)
   - [ ] files.py Jinja2 语法
   - [ ] 检查其他卫星的类似问题

3. **设置预提交钩子** (15 分钟)
   - [ ] 安装钩子
   - [ ] 测试钩子

4. **创建集成测试** (45 分钟)
   - [ ] `tests/integration/test_real_execution.py`
   - [ ] 测试关键卫星

### 本周（2-3 天）

1. **完善测试套件**
   - [ ] 为每个类别添加集成测试
   - [ ] 添加慢速测试（真实执行）
   - [ ] 设置 CI/CD

2. **文档更新**
   - [ ] 添加测试指南
   - [ ] 更新贡献指南
   - [ ] 添加 CI 徽章

3. **质量门禁**
   - [ ] PR 必须通过测试
   - [ ] 代码覆盖率不能下降
   - [ ] 静态分析必须通过

---

## 🚀 预期成果

### 短期（1 周）
- ✅ 自动发现 80% 的 AppleScript 语法错误
- ✅ 消除当前已知的所有 bug
- ✅ 建立基本的集成测试体系

### 中期（2-4 周）
- ✅ 测试覆盖率提升到 80%
- ✅ 真实执行测试覆盖关键卫星
- ✅ CI/CD 完全自动化

### 长期（1-2 月）
- ✅ 零 bug 代码库
- ✅ 测试驱动的开发文化
- ✅ 持续的质量保证体系

---

## 📝 关键原则

1. **真实执行优先**
   - 能用真实测试就不用 mock
   - 只 mock 外部依赖（如 GitHub API）

2. **快速反馈**
   - 预提交钩子 < 10 秒
   - CI 测试 < 5 分钟
   - 慢速测试每周运行

3. **渐进式改进**
   - 先建立基础
   - 再逐步完善
   - 持续迭代优化

---

**创建时间**: 2026-01-27
**负责人**: Orbit Team
**状态**: 🚧 进行中
