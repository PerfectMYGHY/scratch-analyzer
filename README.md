# scratch-analyzer

English version README.md: [README.english.md](docs/README.english.md)

Scratch 解析库。一个使用Python制作的能够分析Python代码的软件包。

## 介绍

### 历史

基础代码再2025年（发布仓库的1年前）编写，当时我有一个梦想，将Scratch翻译成一个Python上能够运行的程序，于是我写下了这个程序，原名`Scratch2Python`。

我~~凭借着我惊人的智慧~~写出了`Scratch2Python`的Scratch转换Python代码功能，虽然代码有一丢烂，但是转换相当成功。

然而，接下来的问题是，Scratch运行时阻挠了我。从代码历史你能看到，本项目最终使用`Scratch4Python`作为运行时库，但是很可惜，我跟他耗了几个月，最终失败。

### 那么此库为何而在

因为我的这个翻译器还是太好了，理论上还可以做到翻译成各种语言，虽然目前仅保证转换为Python是正常的。

我认为这个功能很不错，于是建立存储库并单独提取其代码转换功能。

### 那Scratch4Python呢

我不打算完全放弃他，但是请等我深造几年，吃透OpenGL后，再管它吧。我想到时候将他作为独立库发布，同时更名`python-scratch-vm`。到时候可以两个库结合使用。

### 目录结构

```folder
├── docs # 文档注释文件夹
│   ├── README.chinese.md # 中文文档
│   └── README.english.md # 英文文档
├── LICENSE # MIT
├── pyproject.toml # 项目配置
├── README.md -> docs/README.chinese.md # 自述文件符号链接
├── requirements.txt # 需求文件
└── src # 源代码
    └── ScratchAnalyzer # 软件包目录
```

## 使用

首先下载软件包后，注意软件包名为`ScratchAnalyzer`。

### 准备

首先，请准备好Scratch项目的`project.json`，将Scratch文件的后缀名更改为`.zip`，然后解压，即可得到素材文件和`project.json`。分析文件只需要`project.json`，但是如果需要运行等，请加上素材文件。

### 分析

假设已经准备好环境，使用方法如下：

```python
from ScratchAnalyzer import Project, Scratch
import json
from pathlib import Path

# 1.读取文件，需要解析为字典
with open("project.json", "r", encoding="utf-8") as file: # 使用UTF-8确保不会编码错误
    data = json.load(file)

# 2.创建Project对象，自动建立代码分析树，并存储项目元数据
project = Project(data)

# 3.创建Scratch对象，自动分析素材列表等元数据
scratch = Scratch(project) # 要传入project，这样就能得到所有数据

# 4.生产，由于生产的是多文件，所以要指定输出目录
scratch.generate(Path("output"), language="python") # 第一个参数为输出目录，language为可选参数，默认为"python"，暂不支持其他语言，在此留个TODO

# 5.output下即生产结果，对象析构安全，不需要手动管理
```

## 注意

目前我还没有修改软件包接口，因此用起来有些困难。请等待我重构接口，以让这个软件包更好使用。
