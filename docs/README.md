# scratch-analyzer

English version README.md: [README.english.md](README.english.md)

![Version](https://img.shields.io/badge/version-0.1.5-blue)
![Status](https://img.shields.io/badge/status-alpha-orange)

Scratch 解析库。一个使用Python制作的能够分析Python代码的软件包。

## 介绍

### 历史

基础代码在2025年（发布仓库的1年前）编写，当时我有一个梦想，将Scratch翻译成一个Python上能够运行的程序，于是我写下了这个程序，原名`Scratch2Python`。

我~~凭借着我惊人的智慧~~写出了`Scratch2Python`的Scratch转换Python代码功能，虽然代码有一丢烂，但是转换相当成功。

然而，接下来的问题是，Scratch运行时阻挠了我。从代码历史你能看到，本项目最终使用`Scratch4Python`作为运行时库，但是很可惜，我跟他耗了几个月，最终失败。

### 那么此库为何而在

因为我的这个翻译器还是太好了，理论上还可以做到翻译成各种语言，虽然目前仅保证转换为Python是正常的。

我认为这个功能很不错，于是建立存储库并单独提取其代码转换功能。

### 那Scratch4Python呢

我不打算完全放弃他，但是请等我仔细学习相关知识再说。我想到时候将他作为独立库发布，同时更名`ScratchRuntime`。到时候可以两个库结合使用。

### 目录结构

```folder
├── docs # 文档注释文件夹
│   ├── README.md # 中文文档
│   └── README.english.md # 英文文档
├── LICENSE # MIT
├── pyproject.toml # 项目配置
├── requirements.txt # 需求文件
└── src # 源代码
    └── ScratchAnalyzer # 软件包目录
```

## 环境要求

- Python >= 3.10（因为使用了联合类型语法）

## 使用

首先下载软件包。注意使用时软件包名为`ScratchAnalyzer`。

### 安装

你可以选择从Github的Releases里现在最新的版本，使用whl文件，然后：

```bash
pip install scratchanalyzer-x.x.x-xxx-xxxxx-xxx.whl
```

即可。

### 命令行使用

本库提供一个命令行CLI来直接帮你转换分析。在安装好本软件包后，可以使用`analyze-scratch`命令。

如果要查看帮助，可以：

```bash
analyze-scratch -h
```

以下是命令的参数列表：

| 参数名 | 调用名 | 类型 | 说明 |
| - | - | - | - |
| input | `--input`或`-i` | 文件路径字符串 | 要解析的Scratch文件，可以是原`.sb3`文件 |
| output | `--output`或`-o` | 目录路径字符串 | 要分析转换生成到的目录名，可以不存在 |
| language | `--language`或`-l` | 字符串 | 目标语言 |
| disable-print-progress | `--disable-print-progress`或`-dp` | 不需要值 | 是否禁用打印进度信息 |
| no-comments | `--no-comments`或`-nc` | 不需要值 | 是否禁用翻译Scratch注释 |
| no-variables | `--no-variables`或`-nv` | 不需要值 | 是否禁用翻译Scratch变量/列表内容 |

示例命令：

```bash
analyze-scratch -i test2.sb3 -o out -l python-pcode # 将test2.sb3分析转换为python伪代码，并输出到out目录中
```

如果不需要打印进度信息且不需要Scratch注释：

```bash
analyze-scratch -i test2.sb3 -o out -l python-pcode -dp -nc -nv # 将test2.sb3分析转换为python伪代码，并输出到out目录中，不打印进度信息，不转换注释，不转换Scratch变量/列表
```

- 注意：在输出的`out`目录里，还会有`assets`文件夹，其中是将Scratch项目（如`test2.sb3`）解压后的内容，包含素材和`project.json`

### 在代码中使用

#### 准备

首先，请准备好Scratch项目的`project.json`，将Scratch文件的后缀名更改为`.zip`，然后解压，即可得到素材文件和`project.json`。分析文件只需要`project.json`，但是如果需要运行等，请加上素材文件。

#### 分析

假设已经准备好环境，使用方法如下：

##### 将分析结果直接生成进目录

```python
from ScratchAnalyzer import Project, Scratch
import json

# 1.读取文件，需要解析为字典
with open("project.json", "r", encoding="utf-8") as file: # 使用UTF-8确保不会编码错误
    data = json.load(file)

# 2.创建Project对象，自动建立代码分析树，并存储项目元数据
project = Project(data)

# 3.创建Scratch对象，自动分析素材列表等元数据
scratch = Scratch(project) # 要传入project，这样就能得到所有数据

# 4.生产，由于生产的是多文件，所以要指定输出目录
scratch.generate("output", language="python", print_progress=True) # 第一个参数为输出目录，language为可选参数，默认为"python"，要查看最新的支持语言列表请看后面

# 5.output下即生产结果，对象析构安全，不需要手动管理
```

##### 分析代码并获得生成结果

```python
from ScratchAnalyzer import Project, Scratch
import json

# 1.读取文件，需要解析为字典
with open("project.json", "r", encoding="utf-8") as file: # 使用UTF-8确保不会编码错误
    data = json.load(file)

# 2.创建Project对象，自动建立代码分析树，并存储项目元数据
project = Project(data)

# 3.创建Scratch对象，自动分析素材列表等元数据
scratch = Scratch(project) # 要传入project，这样就能得到所有数据

# 4.分析，得到结果，一定要按照示例方式进行分解。此方式通常更用于生成伪代码，在相应语言后面加上"-pcode"即可（需要确保在支持列表中）
contents, (_, _) = scratch.analyze(language="python-pcode", print_progress=True) # 详细请看解释

# 5.contents为分析生成的代码，类型为字典，键为角色名称，值为(推荐文件名, 生成的代码内容)
```

## 支持的语言

目前支持并且测试正常的语言：

| 语言 | 描述 | 支持程度 |
| - | - | - |
| python | 翻译成理论上可运行的python代码，但是目前缺少运行时 | 完全正常，暂未发现问题 |
| python-pcode | 翻译成python伪代码，不依赖运行时，但不能直接以python运行 | 完全正常，暂未发现问题 |

## 调用接口

### Project 类

`Project`类没有对外方法，仅有构造函数。其存根文件中的定义：

```python
class Project(object):
    project: ProjectDict
    targets: Dict[str, Target]
    monitors: Dict[str, Monitor]
    extensions: Dict[str, Extension]
    meta: Meta

    def __init__(self, project: ProjectDict, print_progress: bool=True):
        ...
```

你可以从project对象获取已经解析好的作品数据

#### Project-构造函数

参数说明：

| 参数名 | 说明 |
| - | - |
| project | Scratch项目的作品信息，应来自于project.json，需要解析成字典 |
| print_progress | 是否打印进度信息，默认为`True` |

说明：

自动解析作品信息，从中提取作品元数据，并且创建目标列表且对每个目标的积木块进行解析和树的构建。

### Scratch 类

`Scratch`类有构造函数、`analyze`、`generate`这几个方法对外。其定义：

```python
class Scratch(object):
    project: Project
    public_id_to_variable_name: Dict[str, str]

    def __init__(self, project: Project):
        ...

    def analyze(self, language: Language="python", print_progress: bool=True, with_comments: bool = True) -> tuple[dict[str, tuple[str, str]], tuple[str, str]]:
        ...

    def generate(self, output: Path | str, language: Language="python", print_progress: bool=True, with_comments: bool = True) -> None:
        ...
```

属性是对外的，可以随便修改，作用如下：

| 属性名 | 用途 |
| - | - |
| project | Project 对象，用于提取项目数据，如果修改相当于切换项目 |
| public_id_to_variable_name | 一个遗留的无用属性，但是每次analyze（或generate）后都会向其中计入全局变量和全局列表 |

#### Scratch-构造函数

仅传入`Project`对象即可。内部仅存储数据和初始化，不进行任何操作

#### analyze函数

参数列表：

| 参数名 | 介绍 |
| - | - |
| language | 目标语言，默认为`python` |
| print_progress | 是否打印进度信息，默认为`True` |
| with_comments | 是否转换Scratch注释，默认为`True` |
| with_variables | 是否转换Scratch变量/列表，默认为`True` |

返回值格式：

```python
contents, (imports_code, inits) = scratch.analyze(...)
```

其中`contents`为分析结果，类型为字典，键为角色名，值为`(推荐文件名, 角色代码)`，如：

```python
{"Stage": ("target_Stage", "\"\"\"\nScr..."), "Player": ("target_Player", "\"\"\"\nScr..."), ...}
```

剩下的`(imports_code, inits)`为`generate`函数所使用，将用于生成主入口文件。一般单独使用时忽略这个结果，像示例一样用`contents, (_, _)`接收即可。

#### generate函数

参数列表：

| 参数名 | 类型 | 介绍 |
| - | - | - |
| output | Path 或 str | 输出目录 |
| language | str | 目标语言，默认为`python` |
| print_progress | bool | 是否打印进度信息，默认为`True` |
| with_comments | bool | 是否转换Scratch注释，默认为`True` |
| with_variables | bool | 是否转换Scratch变量/列表，默认为`True` |

没有返回值，内部调用analyze并将结果写入文件，同时生成入口文件`main.py`

## Issues

我目前很忙碌，所以并不经常登录GitHub，因此如果有Issues我可能无法及时看到。但是，由于我的代码核心逻辑复杂（为了应对Scratch 2.0转换为3.0后的兼容性），且曾出过错（我已解决），所以我不能保证代码总是正常运行。如果有什么问题，完全欢迎创建Issues，我会尽快处理。

## 其他语言

我目前暂不打算添加其他语言的翻译。如果你感兴趣，我当然乐意您提供其他语言的翻译。
