# scratch-analyzer

中文版 README.md: [README.chinese.md](README.chinese.md)

A Scratch parsing library. A Python package capable of analyzing Scratch code.

## Introduction

### History

The core code was written in 2025 (1 year before the repository was published). At that time, I had a dream: to translate Scratch into a runnable Python program. So I wrote this program, originally named `Scratch2Python`.

I ~~with my astonishing wisdom~~ implemented the Scratch-to-Python code conversion feature. Although the code is a bit messy, the conversion was quite successful.

However, the next problem was the Scratch runtime. From the code history you can see that this project ultimately used `Scratch4Python` as the runtime library. Unfortunately, after spending several months on it, I ultimately failed.

### Why does this library exist?

Because my translator is still very good. Theoretically, it can be extended to translate into various languages, although currently only Python conversion is guaranteed to work.

I think this feature is quite valuable, so I created this repository and extracted the code conversion functionality separately.

### What about Scratch4Python?

I don't plan to abandon it completely, but please wait for me to study for a few more years and fully understand OpenGL before I revisit it. I plan to release it as an independent library at that time, renamed to `python-scratch-vm`. At that point, the two libraries can be used together.

### Directory Structure

```folder
├── docs # Documentation folder
│   ├── README.chinese.md # Chinese documentation
│   └── README.english.md # English documentation
├── LICENSE # MIT
├── pyproject.toml # Project configuration
├── README.md -> docs/README.chinese.md # README symlink
├── requirements.txt # Requirements file
└── src # Source code
    └── ScratchAnalyzer # Package directory
```

## Usage

After downloading the package, the package name is `ScratchAnalyzer`.

### Preparation

First, prepare the `project.json` of the Scratch project. Change the Scratch file extension to `.zip`, then unzip it to get the asset files and `project.json`. For analysis, you only need `project.json`, but if you need to run it, please also include the asset files.

### Analysis

Assuming the environment is ready, use the following method:

```python
from ScratchAnalyzer import Project, Scratch
import json
from pathlib import Path

# 1. Read the file, need to parse it as a dictionary
with open("project.json", "r", encoding="utf-8") as file: # Use UTF-8 to ensure no encoding errors
    data = json.load(file)

# 2. Create a Project object, automatically build the code analysis tree, and store project metadata
project = Project(data)

# 3. Create a Scratch object, automatically analyze metadata such as asset lists
scratch = Scratch(project) # Pass in project to get all data

# 4. Generate output (multiple files), so specify an output directory
scratch.generate(Path("output"), language="python") # The first parameter is the output directory, language is optional (default "python"), other languages not yet supported (TODO)

# 5. The output directory contains the generated results. Object destruction is safe and does not require manual management
```

## Note

I haven't refactored the package interface yet, so it's a bit difficult to use. Please wait for me to refactor the interface to make this package more user-friendly.
