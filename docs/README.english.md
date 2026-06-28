# scratch-analyzer

中文版 README.md: [README.md](README.md)

![Version](https://img.shields.io/badge/version-0.1.7-blue)
![Status](https://img.shields.io/badge/status-alpha-orange)

A Scratch parsing library. A Python package capable of analyzing Scratch code.

## Introduction

### History

The core code was written in 2025 (one year before the repository was published). At that time, I had a dream: to translate Scratch into a runnable Python program. So I wrote this program, originally named `Scratch2Python`.

I ~~with my astonishing wisdom~~ implemented the Scratch-to-Python code conversion feature. Although the code is a bit messy, the conversion was quite successful.

However, the next problem was the Scratch runtime. From the code history you can see that this project ultimately used `Scratch4Python` as the runtime library. Unfortunately, after spending several months on it, I ultimately failed.

### Why does this library exist?

Because my translator is still very good. Theoretically, it can be extended to translate into various languages, although currently only Python conversion is guaranteed to work.

I think this feature is quite valuable, so I created this repository and extracted the code conversion functionality separately.

### What about Scratch4Python?

I don't plan to abandon it completely, but please wait for me to study the relevant knowledge carefully first. I plan to release it as an independent library at that time, renamed to `ScratchRuntime`. At that point, the two libraries can be used together.

### Directory Structure

```folder
├── docs # Documentation folder
│   ├── README.md # Chinese documentation
│   └── README.english.md # English documentation
├── LICENSE # MIT
├── pyproject.toml # Project configuration
├── requirements.txt # Requirements file
└── src # Source code
    └── ScratchAnalyzer # Package directory
```

## Requirements

- Python >= 3.10 (due to the use of union type syntax)

## Usage

First, download the package. Note that when using it, the package name is `ScratchAnalyzer`.

### Installation

You can download the latest version from GitHub Releases and use the wheel file:

```bash
pip install scratchanalyzer-x.x.x-xxx-xxxxx-xxx.whl
```

### Command Line Usage

This library provides a command-line CLI to help you convert and analyze directly. After installing the package, you can use the `analyze-scratch` command.

To view help:

```bash
analyze-scratch -h
```

Here is the list of command parameters:

| Parameter | Flag | Type | Description |
| - | - | - | - |
| input | `--input` or `-i` | File path string | The Scratch file to parse, can be the original `.sb3` file |
| output | `--output` or `-o` | Directory path string | The directory to output the analysis/conversion results to, can be non-existent |
| language | `--language` or `-l` | String | Target language |
| disable-print-progress | `--disable-print-progress` or `-dp` | No value needed | Whether to disable printing progress information |
| no-comments | `--no-comments` or `-nc` | No value needed | Whether to disable translating Scratch comments |
| no-variables | `--no-variables` or `-nv` | No value needed | Whether to disable translating Scratch variable/list contents |

Example command:

```bash
analyze-scratch -i test2.sb3 -o out -l python-pcode # Analyze and convert test2.sb3 to Python pseudocode, output to the out directory
```

If you don't want to print progress information, disable comments, and disable variables:

```bash
analyze-scratch -i test2.sb3 -o out -l python-pcode -dp -nc -nv # Same as above, without progress info, without comments, without variable/list contents
```

- Note: In the output `out` directory, there will also be an `assets` folder containing the extracted contents of the Scratch project (e.g., `test2.sb3`), including assets and `project.json`.

### Usage in Code

#### Preparation

First, prepare the `project.json` of the Scratch project. Change the Scratch file extension to `.zip`, then unzip it to get the asset files and `project.json`. For analysis, you only need `project.json`, but if you need to run the code, please also include the asset files.

#### Analysis

Assuming the environment is ready, use the following method:

##### Generate results directly into a directory

```python
from ScratchAnalyzer import Project, Scratch
import json

# 1. Read the file, need to parse it as a dictionary
with open("project.json", "r", encoding="utf-8") as file: # Use UTF-8 to ensure no encoding errors
    data = json.load(file)

# 2. Create a Project object, automatically build the code analysis tree, and store project metadata
project = Project(data)

# 3. Create a Scratch object, automatically analyze metadata such as asset lists
scratch = Scratch(project) # Pass in project to get all data

# 4. Generate output (multiple files), so specify an output directory
scratch.generate("output", language="python", print_progress=True) # The first parameter is the output directory, language is optional (default "python"), see below for the latest list of supported languages

# 5. The output directory contains the generated results. Object destruction is safe and does not require manual management
```

##### Analyze code and get the generation result

```python
from ScratchAnalyzer import Project, Scratch
import json

# 1. Read the file, need to parse it as a dictionary
with open("project.json", "r", encoding="utf-8") as file: # Use UTF-8 to ensure no encoding errors
    data = json.load(file)

# 2. Create a Project object, automatically build the code analysis tree, and store project metadata
project = Project(data)

# 3. Create a Scratch object, automatically analyze metadata such as asset lists
scratch = Scratch(project) # Pass in project to get all data

# 4. Analyze and get the result. Decompose according to the example. This method is usually used to generate pseudo-code. Add "-pcode" after the corresponding language (must be in the support list)
contents, (_, _) = scratch.analyze(language="python-pcode", print_progress=True) # See explanation for details

# 5. contents is the generated code for analysis, type is dict, key is the role name, value is (recommended filename, generated code content)
```

## Supported Languages

Currently supported and tested languages:

| Language | Description | Support Level |
| - | - | - |
| python | Translates to theoretically runnable python code, but currently lacks a runtime | Fully functional, no issues found yet |
| python-pcode | Translates to Python pseudo-code, does not depend on a runtime, but cannot be run directly as Python | Fully functional, no issues found yet |

## API Reference

### Project Class

The `Project` class has no public methods, only a constructor. Its definition in the stub file:

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

You can get the parsed project data from the project object.

#### Project Constructor

Parameter description:

| Parameter | Description |
| - | - |
| project | Scratch project information, should come from project.json, needs to be parsed into a dictionary |
| print_progress | Whether to print progress information, defaults to `True` |

Description:

Automatically parses the project information, extracts project metadata, creates a target list, and parses and builds the block tree for each target.

### Scratch Class

The `Scratch` class has a constructor, `analyze`, and `generate` methods. Its definition:

```python
class Scratch(object):
    project: Project
    public_id_to_variable_name: Dict[str, str]

    def __init__(self, project: Project):
        ...

    def analyze(self, language: Language="python", print_progress: bool=True, with_comments: bool = True, with_variables: bool = True) -> tuple[dict[str, tuple[str, str]], tuple[str, str]]:
        ...

    def generate(self, output: Path | str, language: Language="python", print_progress: bool=True, with_comments: bool = True, with_variables: bool = True) -> None:
        ...
```

Properties are public and can be modified. Their purpose is as follows:

| Property | Purpose |
| - | - |
| project | The Project object, used to extract project data. Modifying it is equivalent to switching projects. |
| public_id_to_variable_name | A legacy unused property, but after each analyze (or generate), global variables and global lists are recorded into it. |

#### Scratch Constructor

Just pass in the `Project` object. It only stores data and initializes, no operations are performed.

#### analyze function

Parameter list:

| Parameter | Description |
| - | - |
| language | Target language, defaults to `python` |
| print_progress | Whether to print progress information, defaults to `True` |
| with_comments | Whether to translate Scratch comments, defaults to `True` |
| with_variables | Whether to translate Scratch variable/list contents, defaults to `True` |

Return value format:

```python
contents, (imports_code, inits) = scratch.analyze(...)
```

`contents` is the analysis result, a dictionary with role names as keys and `(recommended filename, role code)` as values, e.g.:

```python
{"Stage": ("target_Stage", "\"\"\"\nScr..."), "Player": ("target_Player", "\"\"\"\nScr..."), ...}
```

The remaining `(imports_code, inits)` are used by the `generate` function to generate the main entry file. Ignore this result when using it alone, just use `contents, (_, _)` as in the example.

#### generate function

Parameter list:

| Parameter | Type | Description |
| - | - | - |
| output | Path or str | Output directory |
| language | str | Target language, defaults to `python` |
| print_progress | bool | Whether to print progress information, defaults to `True` |
| with_comments | bool | Whether to translate Scratch comments, defaults to `True` |
| with_variables | bool | Whether to translate Scratch variable/list contents, defaults to `True` |

No return value. Internally calls analyze and writes the results to files, also generates the entry file `main.py`.

## Issues

I am currently very busy, so I don't log into GitHub often. Therefore, I may not see Issues promptly. However, because the core logic of my code is complex (to ensure compatibility with Scratch 2.0 projects converted to 3.0), and there have been errors before (which I have resolved), I cannot guarantee that the code will always run correctly. If you have any problems, you are very welcome to create an Issue, and I will handle it as soon as possible.

## Other Languages

I don't plan to add translations to other languages at the moment. If you are interested, I would certainly welcome you to provide translations for other languages.
