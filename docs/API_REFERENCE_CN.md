# Orbit API 参考文档

> **版本：** 1.0.0
> **最后更新：** 2026-01-27

---

## 目录

1. [核心类](#核心类)
   - [MissionControl](#missioncontrol)
   - [Satellite](#satellite)
   - [Constellation](#constellation)
   - [Launcher](#launcher)
   - [SafetyShield](#safetyshield)
2. [数据结构](#数据结构)
   - [SafetyLevel](#safetylevel)
   - [ShieldAction](#shieldaction)
   - [SatelliteParameter](#satelliteparameter)
3. [异常类](#异常类)
4. [结果解析器](#结果解析器)
5. [工具函数](#工具函数)

---

## 核心类

### MissionControl

Orbit 的主入口类。管理卫星星座和任务执行。

```python
from orbit import MissionControl

mission = MissionControl()
mission.register_constellation(all_satellites)
result = mission.launch("system_get_info", {})
```

#### 构造函数

```python
MissionControl(
    safety_shield: Optional[SafetyShield] = None,
    launcher: Optional[Launcher] = None
) -> None
```

**参数：**
- `safety_shield` - 可选的安全防护罩。默认使用默认规则的防护罩。
- `launcher` - 可选的发射器实例。默认创建新的发射器实例。

**示例：**
```python
from orbit import MissionControl, SafetyShield, SafetyLevel

# 使用自定义防护罩创建
shield = SafetyShield(rules={
    SafetyLevel.SAFE: "allow",
    SafetyLevel.MODERATE: "allow"
})
mission = MissionControl(safety_shield=shield)
```

#### 方法

##### register

```python
register(satellite: Satellite) -> None
```

注册单个卫星。

**参数：**
- `satellite` - 要注册的卫星实例

**抛出：**
- `ValueError` - 如果卫星已注册

**示例：**
```python
from orbit.satellites.system import info
mission.register(info.system_get_info)
```

##### register_constellation

```python
register_constellation(satellites: List[Satellite]) -> None
```

一次性注册多个卫星。

**参数：**
- `satellites` - 要注册的卫星列表

**示例：**
```python
from orbit.satellites import all_satellites
mission.register_constellation(all_satellites)
```

##### launch

```python
launch(
    satellite_name: str,
    parameters: dict,
    bypass_shield: bool = False
) -> Any
```

发射任务（执行卫星）。

**参数：**
- `satellite_name` - 要发射的卫星名称
- `parameters` - 任务参数字典
- `bypass_shield` - 跳过安全检查（不推荐）

**返回：**
- 任务结果（类型取决于卫星）

**抛出：**
- `SatelliteNotFoundError` - 如果卫星未找到
- `ShieldError` - 如果安全检查失败
- `AppleScriptError` - 如果脚本执行失败

**示例：**
```python
result = mission.launch(
    "system_get_info",
    parameters={}
)
print(result["version"])
```

##### export_openai_functions

```python
export_openai_functions() -> List[dict]
```

将所有已注册卫星导出为 OpenAI Functions 格式。

**返回：**
- OpenAI Functions 格式的字典列表

**示例：**
```python
functions = mission.export_openai_functions()

import openai
response = openai.chat.completions.create(
    model="gpt-4",
    messages=[{"role": "user", "content": "我的 macOS 版本是多少？"}],
    functions=functions
)
```

##### execute_function_call

```python
execute_function_call(function_call: dict) -> Any
```

执行 OpenAI 函数调用响应。

**参数：**
- `function_call` - 来自响应的 OpenAI function_call 字典

**返回：**
- 任务结果

**示例：**
```python
response = openai.chat.completions.create(...)
if response.choices[0].message.function_call:
    result = mission.execute_function_call(
        response.choices[0].message.function_call
    )
```

#### 属性

##### constellation

```python
mission.constellation: Constellation
```

访问星座注册表。

**示例：**
```python
all_satellites = mission.constellation.list_all()
system_satellites = mission.constellation.list_by_category("system")
```

---

### Satellite

表示单个自动化工具（卫星）。

```python
from orbit.core import Satellite, SatelliteParameter, SafetyLevel

satellite = Satellite(
    name="example_tool",
    description="示例卫星",
    category="system",
    parameters=[...],
    safety_level=SafetyLevel.SAFE,
    applescript_template='return "hello"'
)
```

#### 构造函数

```python
Satellite(
    name: str,
    description: str,
    category: str,
    parameters: List[SatelliteParameter],
    safety_level: SafetyLevel,
    applescript_template: str,
    result_parser: Optional[Callable] = None,
    examples: List[dict] = None,
    version: str = "1.0.0",
    author: str = ""
)
```

**参数：**
- `name` - 唯一标识符（snake_case 格式）
- `description` - LLM 可读的描述
- `category` - 类别（system、files、notes 等）
- `parameters` - 参数定义列表
- `safety_level` - 安全分类
- `applescript_template` - AppleScript 的 Jinja2 模板
- `result_parser` - 可选的结果解析函数
- `examples` - 可选的使用示例列表
- `version` - 卫星版本
- `author` - 卫星作者

#### 方法

##### to_openai_function

```python
to_openai_function() -> dict
```

将卫星转换为 OpenAI Function 格式。

**返回：**
- OpenAI Function 格式字典

##### to_dict

```python
to_dict() -> dict
```

将卫星转换为字典格式。

**返回：**
- 卫星数据字典

---

### Constellation

卫星星座管理注册表。

```python
from orbit.core import Constellation

constellation = Constellation()
constellation.register(satellite)
all_satellites = constellation.list_all()
```

#### 方法

##### register

```python
register(satellite: Satellite) -> None
```

注册卫星。

**参数：**
- `satellite` - 要注册的卫星

**抛出：**
- `ValueError` - 如果卫星已存在

##### unregister

```python
unregister(name: str) -> None
```

注销卫星。

**参数：**
- `name` - 卫星名称

**抛出：**
- `ValueError` - 如果卫星未找到

##### get

```python
get(name: str) -> Optional[Satellite]
```

按名称获取卫星。

**参数：**
- `name` - 卫星名称

**返回：**
- 卫星实例或 None

##### list_all

```python
list_all() -> List[Satellite]
```

获取所有已注册的卫星。

**返回：**
- 所有卫星的列表

##### list_by_category

```python
list_by_category(category: str) -> List[Satellite]
```

按类别获取卫星。

**参数：**
- `category` - 类别名称

**返回：**
- 该类别中的卫星列表

##### list_by_safety

```python
list_by_safety(safety_level: SafetyLevel) -> List[Satellite]
```

按安全等级获取卫星。

**参数：**
- `safety_level` - 安全等级

**返回：**
- 具有给定安全等级的卫星列表

##### search

```python
search(query: str) -> List[Satellite]
```

按名称或描述搜索卫星。

**参数：**
- `query` - 搜索查询

**返回：**
- 匹配的卫星列表

##### to_openai_functions

```python
to_openai_functions() -> List[dict]
```

将所有卫星导出为 OpenAI Functions 格式。

**返回：**
- OpenAI Functions 字典列表

##### to_json_schema

```python
to_json_schema() -> str
```

将所有卫星导出为 JSON Schema 字符串。

**返回：**
- JSON Schema 字符串

##### get_categories

```python
get_categories() -> List[str]
```

获取所有类别名称。

**返回：**
- 类别名称列表

##### get_stats

```python
get_stats() -> dict
```

获取星座统计信息。

**返回：**
- 包含 total_satellites、categories、by_safety 的字典

---

### Launcher

为卫星执行 AppleScript。

```python
from orbit.core import Launcher, SafetyShield

shield = SafetyShield()
launcher = Launcher(safety_shield=shield)
result = launcher.launch(satellite, parameters)
```

#### 构造函数

```python
Launcher(
    safety_shield: Optional[SafetyShield] = None,
    timeout: int = 30,
    retry_on_failure: bool = False,
    max_retries: int = 3
)
```

**参数：**
- `safety_shield` - 可选的安全防护罩
- `timeout` - 脚本执行超时时间（秒）
- `retry_on_failure` - 失败时是否重试
- `max_retries` - 最大重试次数

#### 方法

##### launch

```python
launch(
    satellite: Satellite,
    parameters: dict,
    bypass_shield: bool = False
) -> Any
```

执行卫星。

**参数：**
- `satellite` - 要执行的卫星
- `parameters` - 执行参数
- `bypass_shield` - 跳过安全检查

**返回：**
- 执行结果

**抛出：**
- `ShieldError` - 如果安全检查失败
- `AppleScriptError` - 如果执行失败

##### launch_async

```python
async launch_async(
    satellite: Satellite,
    parameters: dict
) -> Any
```

异步执行卫星。

**参数：**
- `satellite` - 要执行的卫星
- `parameters` - 执行参数

**返回：**
- 执行结果

**示例：**
```python
import asyncio

result = await launcher.launch_async(satellite, parameters)
```

---

### SafetyShield

验证和控制任务执行。

```python
from orbit.core import SafetyShield, SafetyLevel

shield = SafetyShield(
    rules={
        SafetyLevel.SAFE: "allow",
        SafetyLevel.MODERATE: "confirm"
    }
)
```

#### 构造函数

```python
SafetyShield(
    rules: Optional[Dict[SafetyLevel, ShieldAction]] = None,
    confirmation_callback: Optional[Callable] = None,
    protected_paths: Optional[List[Path]] = None,
    dangerous_commands: Optional[List[str]] = None
)
```

**参数：**
- `rules` - 安全等级到动作的映射
- `confirmation_callback` - 用户确认函数
- `protected_paths` - 受保护的系统路径列表
- `dangerous_commands` - 危险命令模式列表

#### 方法

##### validate

```python
validate(satellite: Satellite, parameters: dict) -> bool
```

验证任务安全性。

**参数：**
- `satellite` - 要验证的卫星
- `parameters` - 任务参数

**返回：**
- 如果安全返回 True

**抛出：**
- `ShieldError` - 如果验证失败

##### add_protected_path

```python
add_protected_path(path: str) -> None
```

添加受保护路径。

**参数：**
- `path` - 要保护的路径字符串

##### remove_protected_path

```python
remove_protected_path(path: str) -> None
```

移除受保护路径。

**参数：**
- `path` - 要取消保护的路径字符串

---

## 数据结构

### SafetyLevel

卫星安全等级枚举。

```python
from orbit.core import SafetyLevel

SafetyLevel.SAFE       # 只读，无副作用
SafetyLevel.MODERATE   # 创建/修改操作
SafetyLevel.DANGEROUS  # 删除操作
SafetyLevel.CRITICAL   # 系统级操作
```

**值：**
- `SAFE` - 安全操作（只读）
- `MODERATE` - 中等风险（创建/修改）
- `DANGEROUS` - 危险操作（删除）
- `CRITICAL` - 严重操作（系统级）

### ShieldAction

防护罩动作枚举。

```python
from orbit.core import ShieldAction

ShieldAction.ALLOW                   # 允许操作
ShieldAction.DENY                    # 阻止操作
ShieldAction.REQUIRE_CONFIRMATION    # 需要用户确认
```

### SatelliteParameter

卫星参数定义。

```python
from orbit.core import SatelliteParameter

param = SatelliteParameter(
    name="file_path",
    type="string",
    description="文件路径",
    required=True,
    default=None
)
```

#### 构造函数

```python
SatelliteParameter(
    name: str,
    type: str,
    description: str,
    required: bool = True,
    default: Any = None,
    enum: Optional[list] = None
)
```

**参数：**
- `name` - 参数名称
- `type` - 参数类型（string、integer、boolean、object、array）
- `description` - 参数描述
- `required` - 参数是否必需
- `default` - 默认值
- `enum` - 可选的允许值列表

---

## 异常类

### OrbitError

所有 Orbit 错误的基础异常。

```python
from orbit.core.exceptions import OrbitError
```

### ShieldError

安全检查失败时抛出。

```python
from orbit.core.exceptions import ShieldError

try:
    mission.launch("dangerous_operation", {...})
except ShieldError as e:
    print(f"安全阻止：{e}")
```

### AppleScriptError

AppleScript 执行失败时抛出。

```python
from orbit.core.exceptions import AppleScriptError

try:
    mission.launch("notes_create", {...})
except AppleScriptError as e:
    print(f"脚本错误：{e}")
    print(f"返回码：{e.return_code}")
    print(f"脚本：{e.script}")
```

**属性：**
- `script` - 失败的脚本
- `return_code` - AppleScript 返回码

### AppleScriptTimeoutError

脚本执行超时时抛出。

```python
from orbit.core.exceptions import AppleScriptTimeoutError
```

### AppleScriptPermissionError

AppleScript 权限不足时抛出。

```python
from orbit.core.exceptions import AppleScriptPermissionError
```

### AppleScriptSyntaxError

AppleScript 语法错误时抛出。

```python
from orbit.core.exceptions import AppleScriptSyntaxError
```

### SatelliteNotFoundError

星座中未找到卫星时抛出。

```python
from orbit.core.exceptions import SatelliteNotFoundError

try:
    mission.launch("nonexistent_satellite", {})
except SatelliteNotFoundError as e:
    print(f"卫星未找到：{e}")
```

### ParameterValidationError

参数验证失败时抛出。

```python
from orbit.core.exceptions import ParameterValidationError
```

### TemplateRenderingError

模板渲染失败时抛出。

```python
from orbit.core.exceptions import TemplateRenderingError
```

---

## 结果解析器

### JSONResultParser

解析 AppleScript 的 JSON 输出。

```python
from orbit.parsers import JSONResultParser

parser = JSONResultParser()
result = parser.parse('{"key": "value"}')
# result = {"key": "value"}
```

### DelimitedResultParser

解析分隔符输出。

```python
from orbit.parsers import DelimitedResultParser

parser = DelimitedResultParser(delimiter="|", field_names=["name", "age"])
result = parser.parse("张三|30")
# result = {"name": "张三", "age": "30"}
```

### RegexResultParser

使用正则表达式解析输出。

```python
from orbit.parsers import RegexResultParser

parser = RegexResultParser(
    pattern=r"姓名：(\w+)，年龄：(\d+)",
    group_names=["name", "age"]
)
result = parser.parse("姓名：张三，年龄：30")
# result = {"name": "张三", "age": "30"}
```

### BooleanResultParser

解析布尔值输出。

```python
from orbit.parsers import BooleanResultParser

parser = BooleanResultParser()
result = parser.parse("true")
# result = True
```

---

## 工具函数

### check_permissions

检查 Orbit 的 macOS 权限。

```python
from orbit.utils import check_permissions

permissions = check_permissions()
for perm, granted in permissions.items():
    print(f"{perm}: {'✅ 已授予' if granted else '❌ 缺失'}")
```

**返回：**
- 权限名称到授予状态的映射字典

### get_system_info

获取 Orbit 和系统信息。

```python
from orbit.utils import get_system_info

info = get_system_info()
print(f"Orbit 版本：{info['orbit_version']}")
print(f"macOS 版本：{info['macos_version']}")
```

**返回：**
- 包含 Orbit 和系统信息的字典

---

## 完整示例

### 基础用法

```python
from orbit import MissionControl
from orbit.satellites import all_satellites

# 初始化
mission = MissionControl()
mission.register_constellation(all_satellites)

# 发射任务
result = mission.launch("system_get_info", {})
print(f"macOS {result['version']}")
```

### 自定义安全

```python
from orbit import MissionControl, SafetyShield, SafetyLevel

def confirm(satellite, params):
    return input(f"允许 {satellite.name}? (y/n): ") == "y"

shield = SafetyShield(
    rules={SafetyLevel.MODERATE: "confirm"},
    confirmation_callback=confirm
)

mission = MissionControl(safety_shield=shield)
```

### 自定义卫星

```python
from orbit.core import Satellite, SatelliteParameter, SafetyLevel
from orbit.parsers import DelimitedResultParser

my_satellite = Satellite(
    name="get_current_time",
    description="从 macOS 获取当前时间",
    category="system",
    parameters=[],
    safety_level=SafetyLevel.SAFE,
    applescript_template="""
    tell application "System Events"
        set currentTime to current date
        set timeString to time string of currentTime
    end tell
    return timeString
    """,
    result_parser=lambda x: {"time": x}
)

mission.register(my_satellite)
```

### 异步执行

```python
import asyncio
from orbit import MissionControl

async def main():
    mission = MissionControl()
    mission.register_constellation(all_satellites)

    # 并发发射多个任务
    results = await asyncio.gather(
        mission.launcher.launch_async(sat1, params1),
        mission.launcher.launch_async(sat2, params2),
        mission.launcher.launch_async(sat3, params3)
    )

    return results

asyncio.run(main())
```

### OpenAI 集成

```python
import openai
from orbit import MissionControl
from orbit.satellites import all_satellites

# 初始化
mission = MissionControl()
mission.register_constellation(all_satellites)

# 导出函数
functions = mission.export_openai_functions()

# 调用 OpenAI
response = openai.chat.completions.create(
    model="gpt-4",
    messages=[
        {"role": "system", "content": "你是一个有帮助的助手。"},
        {"role": "user", "content": "创建一个关于会议的笔记"}
    ],
    functions=functions,
    function_call="auto"
)

# 执行函数
msg = response.choices[0].message
if msg.function_call:
    result = mission.execute_function_call(msg.function_call)
    print(f"操作结果：{result}")
```

### LangChain 集成

```python
from langchain.agents import initialize_agent, AgentType
from langchain_openai import ChatOpenAI
from langchain.tools import StructuredTool
from orbit import MissionControl
from orbit.satellites import all_satellites

# 初始化
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
llm = ChatOpenAI(model="gpt-4", temperature=0)
agent = initialize_agent(
    langchain_tools,
    llm,
    agent=AgentType.OPENAI_FUNCTIONS,
    verbose=True
)

# 运行代理
result = agent.run("创建一个提醒：明天下午3点开会")
```

---

**API 版本：** 1.0.0
**最后更新：** 2026-01-27
