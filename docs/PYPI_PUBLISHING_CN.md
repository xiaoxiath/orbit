# PyPI 包发布指南

> **Orbit macOS 自动化工具包**
> 版本: 1.0.0

本指南说明如何将 `orbit-macos` 包发布到 PyPI (Python Package Index)。

---

## 前置条件

### 1. 安装 Poetry

Poetry 用于依赖管理和打包。

```bash
curl -sSL https://install.python-poetry.org | python3 -
```

验证安装:
```bash
poetry --version
```

### 2. 安装 Twine

Twine 用于安全上传包到 PyPI。

```bash
pip install twine
```

### 3. PyPI 账户

你需要 PyPI 账户:
- **生产环境**: https://pypi.org/account/register/
- **测试环境**: https://test.pypi.org/account/register/

**重要提示**: 启用双因素认证并创建 API token 用于认证。

---

## 发布流程

### 步骤 1: 更新版本号（如需要）

编辑 `pyproject.toml`:

```toml
[tool.poetry]
name = "orbit-macos"
version = "1.0.0"  # 更新此版本号
```

### 步骤 2: 构建包

```bash
# 清理旧的构建文件
rm -rf dist/ build/ *.egg-info

# 使用 Poetry 构建
poetry build
```

这将创建:
- `dist/orbit-macos-1.0.0.tar.gz` - 源码分发
- `dist/orbit_macos-1.0.0-py3-none-any.whl` - Wheel 分发

### 步骤 3: 检查包

验证包元数据:
```bash
twine check dist/*
```

期望输出:
```
Checking orbit-macos-1.0.0.tar.gz: PASSED
Checking orbit_macos-1.0.0-py3-none-any.whl: PASSED
```

### 步骤 4: 测试发布（推荐）

先发布到 TestPyPI 验证一切正常:

```bash
# 在 ~/.pypirc 中配置 TestPyPI 凭证
twine upload --repository testpypi dist/*
```

从 TestPyPI 测试安装:
```bash
pip install --index-url https://test.pypi.org/simple/ orbit-macos
```

### 步骤 5: 发布到 PyPI

测试成功后，发布到生产 PyPI:

```bash
twine upload dist/*
```

---

## 认证方式

### 方式 1: API Token（推荐）

1. 访问 https://pypi.org/manage/account/token/
2. 创建新 token，权限选择 "Entire account"
3. 使用用户名 `__token__` 和 token 作为密码

```bash
twine upload dist/* --username __token__ --password <your-token>
```

### 方式 2: ~/.pypirc 配置

创建 `~/.pypirc`:

```ini
[distutils]
index-servers =
    pypi
    testpypi

[pypi]
username = __token__
password = <your-pypi-token>

[testpypi]
username = __token__
password = <your-testpypi-token>
repository = https://test.pypi.org/legacy/
```

然后无需提示即可上传:
```bash
twine upload dist*  # PyPI
twine upload --repository testpypi dist*  # TestPyPI
```

---

## 自动化脚本

使用提供的脚本进行自动化发布:

```bash
./scripts/publish_to_pypi.sh
```

脚本功能:
- ✅ 检查前置条件 (Poetry, Twine)
- ✅ 显示当前版本
- ✅ 清理旧构建文件
- ✅ 使用 Poetry 构建包
- ✅ 使用 Twine 检查包
- ✅ 提示选择目标 (TestPyPI/PyPI)
- ✅ 上传到选定仓库
- ✅ 显示安装说明

---

## 验证

发布后，验证包:

### 检查 PyPI 页面
- **生产环境**: https://pypi.org/project/orbit-macos/
- **测试环境**: https://test.pypi.org/project/orbit-macos/

### 测试安装

```bash
# 创建虚拟环境
python -m venv test_env
source test_env/bin/activate  # Windows: test_env\Scripts\activate

# 从 PyPI 安装
pip install orbit-macos

# 测试导入
python -c "from orbit import MissionControl; print('✅ 导入成功')"

# 测试 CLI
orbit --version

# 清理
deactivate
rm -rf test_env
```

### 运行基本测试

```bash
# 安装后
python -c "
from orbit import MissionControl
from orbit.satellites import all_satellites

mission = MissionControl()
mission.register_constellation(all_satellites)

# 测试基础卫星
result = mission.launch('system_get_info', {})
print(f'macOS 版本: {result.get(\"version\", \"未知\")}')
print('✅ 所有测试通过!')
"
```

---

## 常见问题

### 问题: "Package already exists"

尝试上传已发布的版本时出现此错误。

**解决方法**: 在 `pyproject.toml` 中增加版本号并重新构建。

### 问题: "403 Forbidden"

认证失败。

**解决方法**:
1. 验证 API token 有效
2. 检查 `~/.pypirc` 配置
3. 使用 `__token__` 作为用户名

### 问题: "Invalid or missing authentication credentials"

Twine 找不到凭证。

**解决方法**: 创建 `~/.pypirc` 并填入你的 token (见认证方式部分)。

### 问题: 构建失败

Poetry 构建因错误而失败。

**解决方法**:
```bash
# 检查 poetry.lock 是否最新
poetry lock --no-update

# 验证 pyproject.toml
poetry check

# 再次尝试构建
poetry build
```

---

## 版本更新清单

发布新版本时:

- [ ] 更新 `pyproject.toml` 中的版本号
- [ ] 在 CHANGELOG.md 中添加发布说明
- [ ] 更新文档中的版本引用
- [ ] 运行完整测试套件: `poetry run pytest`
- [ ] 构建包: `poetry build`
- [ ] 本地测试: `pip install dist/orbit_macos-*.whl`
- [ ] 先上传到 TestPyPI
- [ ] 从 TestPyPI 安装并验证
- [ ] 上传到生产 PyPI
- [ ] 在 https://pypi.org/project/orbit-macos/ 验证
- [ ] 创建带标签的 GitHub 发布
- [ ] 发布公告

---

## 项目配置

当前 `pyproject.toml` 设置:

```toml
[tool.poetry]
name = "orbit-macos"
version = "1.0.0"
description = "🛸 Orbit: Your AI's Bridge to macOS - Framework-agnostic automation toolkit with 104+ satellites"

[tool.poetry.dependencies]
python = "^3.10"
jinja2 = "^3.1.0"
structlog = "^23.0.0"
pydantic = "^2.0.0"
click = "^8.1.0"
```

**关键点**:
- 包名: `orbit-macos` (使用 `pip install orbit-macos` 安装)
- 导入名: `orbit` (使用 `from orbit import MissionControl`)
- Python: 3.10+
- CLI 命令: `orbit`

---

## 发布后任务

成功发布后:

1. **在 Git 中标记版本**:
   ```bash
   git tag v1.0.0
   git push origin v1.0.0
   ```

2. **创建 GitHub Release**:
   - 访问: https://github.com/xiaoxiath/orbit/releases/new
   - 标签: `v1.0.0`
   - 标题: `🛸 Orbit v1.0.0 - Your AI's Bridge to macOS`
   - 描述: 从 CHANGELOG.md 复制

3. **更新文档**:
   - 更新安装说明指向 PyPI
   - 添加 badge 到 README: `[![PyPI version](https://badge.fury.io/py/orbit-macos.svg)](https://pypi.org/project/orbit-macos/)`

4. **发布公告**:
   - Twitter/X
   - 项目讨论区
   - 社区渠道

---

## 快速参考

```bash
# 完整发布流程
rm -rf dist/ build/ *.egg-info
poetry build
twine check dist/*
twine upload --repository testpypi dist/*  # 先测试
pip install --index-url https://test.pypi.org/simple/ orbit-macos  # 验证
twine upload dist*  # 生产环境
```

---

**最后更新**: 2026-01-27
**当前版本**: 1.0.0
**包 URL**: https://pypi.org/project/orbit-macos/
