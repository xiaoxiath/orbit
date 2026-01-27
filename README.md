# Orbit 🛸

<img src="docs/logo.png" alt="Orbit Logo" width="200"/>

> **Your AI's Bridge to macOS**
> **让您的 AI 桥接到 macOS**

---

## 🌍 Language / 语言

**[English](#english) | [简体中文](#中文)**

---

## English

**Orbit** is a framework-agnostic macOS automation toolkit that empowers AI agents to seamlessly interact with macOS through AppleScript.

### 🌟 Key Features

- **100+ Satellites** - Comprehensive macOS automation tools
- **4-Tier Safety** - Built-in security system (SAFE/MODERATE/DANGEROUS/CRITICAL)
- **Framework Agnostic** - Works with OpenAI, LangChain, Anthropic, and custom agents
- **CLI Tool Included** - Convenient terminal access to all satellites
- **Bilingual Docs** - Complete documentation in English and Chinese

### 🚀 Quick Start

```bash
# Install
pip install orbit-macos

# Basic usage
from orbit import MissionControl
from orbit.satellites import all_satellites

mission = MissionControl()
mission.register_constellation(all_satellites)
result = mission.launch("system_get_info", {})
```

### 📚 Documentation

#### Getting Started
- **[Quick Start Guide](docs/QUICKSTART.md)** - Get up and running in 5 minutes
- **[API Reference](docs/API_REFERENCE.md)** - Complete API documentation
- **[CLI Reference](docs/CLI_REFERENCE.md)** - Command-line tool documentation

#### Core Documentation
- **[Design Document](docs/DESIGN.md)** - Architecture and technical details
- **[Security Model](docs/SECURITY.md)** - Safety system and best practices
- **[Satellites Reference](docs/SATELLITES.md)** - Complete list of all 104 satellites

#### Guides
- **[Terminology](docs/TERMINOLOGY.md)** - Orbit naming conventions
- **[Contributing Guide](docs/CONTRIBUTING.md)** - How to contribute

#### Examples
- **[CLI Examples](examples/cli_examples.md)** - CLI usage examples
- **[Python Examples](examples/)** - Code examples for various frameworks

### 📦 Project Links

- **[GitHub](https://github.com/xiaoxiath/orbit)** - Source code
- **[Changelog](CHANGELOG.md)** - Version history
- **[License](LICENSE)** - MIT License

---

## 中文

**Orbit** 是一个框架无关的 macOS 自动化工具包，通过 AppleScript 赋能 AI 代理无缝操作 macOS。

### 🌟 核心特性

- **100+ 卫星工具** - 全面的 macOS 自动化能力
- **四级安全系统** - 内置安全保护（安全/中等/危险/严重）
- **框架无关** - 支持 OpenAI、LangChain、Anthropic 和自定义代理
- **CLI 工具** - 方便的终端访问
- **双语文档** - 完整的中英文文档

### 🚀 快速开始

```bash
# 安装
pip install orbit-macos

# 基础用法
from orbit import MissionControl
from orbit.satellites import all_satellites

mission = MissionControl()
mission.register_constellation(all_satellites)
result = mission.launch("system_get_info", {})
```

### 📚 文档

#### 入门指南
- **[快速入门](docs/QUICKSTART_CN.md)** - 5 分钟上手教程
- **[API 参考文档](docs/API_REFERENCE_CN.md)** - 完整 API 文档
- **[CLI 参考文档](docs/CLI_REFERENCE.md)** - 命令行工具文档

#### 核心文档
- **[设计文档](docs/DESIGN_CN.md)** - 架构和技术细节
- **[安全模型](docs/SECURITY_CN.md)** - 安全系统和最佳实践
- **[卫星参考手册](docs/SATELLITES_CN.md)** - 104 个卫星完整列表

#### 指南
- **[术语表](docs/TERMINOLOGY_CN.md)** - Orbit 命名规范
- **[贡献指南](docs/CONTRIBUTING_CN.md)** - 如何贡献代码

#### 示例
- **[CLI 示例](examples/cli_examples.md)** - CLI 使用示例
- **[Python 示例](examples/)** - 各种框架的代码示例

### 📦 项目链接

- **[GitHub](https://github.com/xiaoxiath/orbit)** - 源代码
- **[更新日志](CHANGELOG.md)** - 版本历史
- **[许可证](LICENSE)** - MIT 许可证

---

## 🛰️ Satellite Constellation

Orbit provides 104 satellites across 12 categories:

| Category | Count | Satellites |
|----------|-------|-----------|
| **System** | 24 | System info, clipboard, notifications, screenshots... |
| **Files** | 10 | File operations: read, write, delete, search... |
| **Notes** | 7 | Create, read, update, delete, search notes |
| **Reminders** | 6 | Manage reminders and lists |
| **Calendar** | 4 | Create and manage events |
| **Mail** | 6 | Send and read emails |
| **Safari** | 12 | Browser automation, tabs, search |
| **Music** | 11 | Playback control and library |
| **Finder** | 6 | File manager operations |
| **Contacts** | 4 | Search and retrieve contacts |
| **WiFi** | 6 | Network management |
| **Apps** | 8 | Application lifecycle |

[View complete satellite list →](docs/SATELLITES.md) | [查看完整卫星列表 →](docs/SATELLITES_CN.md)

---

## 🛡️ Safety System

Orbit implements a 4-tier safety system:

| Level | Description | Examples | Action |
|-------|-------------|----------|--------|
| **SAFE** | Read-only operations | Get info, list files | ✅ Allow |
| **MODERATE** | Create/modify | Write file, create note | ⚠️ Confirm |
| **DANGEROUS** | Delete operations | Delete file, empty trash | ⚠️ Confirm |
| **CRITICAL** | System-level | System file modification | 🚫 Deny |

[Learn more about security →](docs/SECURITY.md) | [了解安全详情 →](docs/SECURITY_CN.md)

---

## 🔗 Framework Integration

Orbit integrates seamlessly with popular AI frameworks:

### OpenAI Functions
```python
from orbit import MissionControl
from orbit.satellites import all_satellites

mission = MissionControl()
mission.register_constellation(all_satellites)
functions = mission.export_openai_functions()

# Use with OpenAI API
response = openai.chat.completions.create(
    model="gpt-4",
    messages=[{"role": "user", "content": "What's my macOS version?"}],
    functions=functions
)
```

### LangChain
```python
from langchain.agents import initialize_agent, AgentType
from langchain.tools import StructuredTool
from orbit import MissionControl

mission = MissionControl()
mission.register_constellation(all_satellites)

tools = [
    StructuredTool.from_function(
        func=lambda **kwargs: mission.launch(sat.name, kwargs),
        name=sat.name,
        description=sat.description
    )
    for sat in mission.constellation.list_all()
]

agent = initialize_agent(tools, llm, agent=AgentType.OPENAI_FUNCTIONS)
```

[More integration examples →](examples/) | [更多集成示例 →](examples/)

---

## 📖 Documentation Index

### By Language / 按语言

#### English / 英文
- **[Quick Start](docs/QUICKSTART.md)** - 5-minute tutorial
- **[API Reference](docs/API_REFERENCE.md)** - Complete API docs
- **[CLI Reference](docs/CLI_REFERENCE.md)** - CLI tool guide
- **[Design Doc](docs/DESIGN.md)** - Technical architecture
- **[Security Model](docs/SECURITY.md)** - Safety system
- **[Contributing](docs/CONTRIBUTING.md)** - Contribution guide

#### 中文 / Chinese
- **[快速入门](docs/QUICKSTART_CN.md)** - 5分钟上手
- **[API 参考](docs/API_REFERENCE_CN.md)** - 完整API文档
- **[设计文档](docs/DESIGN_CN.md)** - 技术架构
- **[安全模型](docs/SECURITY_CN.md)** - 安全系统
- **[贡献指南](docs/CONTRIBUTING_CN.md)** - 贡献指南

### By Topic / 按主题

#### Getting Started / 入门
- [Quick Start Guide](docs/QUICKSTART.md) | [快速入门](docs/QUICKSTART_CN.md)
- [CLI Quick Start](docs/CLI_QUICKSTART.md) | [CLI 快速入门](docs/CLI_QUICKSTART.md)
- [API Reference](docs/API_REFERENCE.md) | [API 参考文档](docs/API_REFERENCE_CN.md)

#### Reference / 参考
- [Satellites Reference](docs/SATELLITES.md) | [卫星参考手册](docs/SATELLITES_CN.md)
- [Terminology](docs/TERMINOLOGY.md) | [术语表](docs/TERMINOLOGY_CN.md)
- [Test Coverage](docs/TEST_COVERAGE.md) | [测试覆盖率](docs/TEST_COVERAGE.md)

#### Development / 开发
- [Design Document](docs/DESIGN.md) | [设计文档](docs/DESIGN_CN.md)
- [Security Model](docs/SECURITY.md) | [安全模型](docs/SECURITY_CN.md)
- [Contributing Guide](docs/CONTRIBUTING.md) | [贡献指南](docs/CONTRIBUTING_CN.md)
- [Release Checklist](docs/RELEASE_CHECKLIST.md) | [发布检查清单](docs/RELEASE_CHECKLIST.md)

[View all documentation →](docs/INDEX.md) | [查看所有文档 →](docs/INDEX_CN.md)

---

## 📊 Project Statistics

- **Version:** 1.0.0
- **Release Date:** January 27, 2026
- **Total Satellites:** 104
- **Categories:** 12
- **Python Code:** 5,069 lines
- **Test Cases:** 272
- **Test Coverage:** 65% code / 95% functionality
- **Documentation Files:** 23 markdown files (bilingual)

---

## 🤝 Contributing

Contributions are welcome! Please read our [Contributing Guide](docs/CONTRIBUTING.md) | [贡献指南](docs/CONTRIBUTING_CN.md).

### Development Setup / 开发设置

```bash
# Clone repository
git clone https://github.com/xiaoxiath/orbit.git
cd orbit

# Install dependencies
pip install -e ".[dev]"

# Run tests
pytest

# Run with coverage
pytest --cov=orbit --cov-report=html
```

---

## 📄 License

MIT License - see [LICENSE](LICENSE) for details.

---

## 🙏 Acknowledgments

Built with ❤️ for the macOS automation community.

**Orbit: Your AI's Bridge to macOS** 🛸

---

## 🔗 Quick Links

### Documentation / 文档
- 📖 [All Documentation Index](docs/INDEX.md) | [文档索引](docs/INDEX_CN.md)
- 🚀 [Quick Start](docs/QUICKSTART.md) | [快速入门](docs/QUICKSTART_CN.md)
- 📚 [API Reference](docs/API_REFERENCE.md) | [API 参考](docs/API_REFERENCE_CN.md)
- 🛡️ [Security Model](docs/SECURITY.md) | [安全模型](docs/SECURITY_CN.md)

### Community / 社区
- 💻 [GitHub Repository](https://github.com/xiaoxiath/orbit)
- 🐛 [Issue Tracker](https://github.com/xiaoxiath/orbit/issues)
- 💬 [Discussions](https://github.com/xiaoxiath/orbit/discussions)

### Tools / 工具
- 🖥️ [CLI Tool](docs/CLI_REFERENCE.md) | [命令行工具](docs/CLI_REFERENCE.md)
- 📋 [Satellites List](docs/SATELLITES.md) | [卫星列表](docs/SATELLITES_CN.md)
- 🎯 [Test Coverage](docs/TEST_COVERAGE.md) | [测试覆盖率](docs/TEST_COVERAGE.md)

---

**Version:** 1.0.0 | **Last Updated:** 2026-01-27 | **Status:** ✅ Production Ready
