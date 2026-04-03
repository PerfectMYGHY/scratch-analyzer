# scratch-analyzer

Chinese version README.md: [README.md](README.md)

A Scratch parsing library — a Python package for analyzing and processing Scratch project data.

## Introduction

### History

The core code was written in 2025 (one year before this repository was published). Back then I wanted to translate Scratch projects into programs runnable on Python, so I started this project originally named `Scratch2Python`.

I implemented Scratch-to-Python translation in `Scratch2Python`. The code was a bit rough, but the translation worked well.

The main challenge after that was the Scratch runtime. As the project history shows, I attempted to use `Scratch4Python` as the runtime library, but after several months of work I couldn't make it reliably work.

### Why this project exists

The translator itself remains useful: in theory it could be adapted to target multiple languages, although currently only Python output is fully supported.

I decided to extract and preserve the translation functionality as a standalone package and publish it in this repository.

### What about Scratch4Python?

I don't plan to abandon it entirely, but I need more time to study OpenGL. When I'm ready I'll release it as a separate library under the name `python-scratch-vm`. At that point the two projects can be used together.

## Usage

After downloading the package, the import name is not finalized; examples below use `ScratchAnalyzer`.

### Prepare

Prepare the Scratch project's `project.json`: rename the `.sb3` file to `.zip` and unzip it to obtain the asset files and `project.json`. Analysis only requires `project.json`, but if you want to run the project you should also include the asset files.

### Analyze

Assuming your environment is ready, use the library as follows:

```python
from ScratchAnalyzer import Project, Scratch
import json
from pathlib import Path

# 1. Load the project.json as a dictionary
with open("project.json", "r", encoding="utf-8") as f:
    data = json.load(f)

# 2. Create a Project object — this builds the code analysis tree and stores project metadata
project = Project(data)

# 3. Create a Scratch object — this analyzes assets and other metadata
scratch = Scratch(project)

# 4. Generate output. Because generation produces multiple files, provide an output directory
scratch.generate(Path("output"), language="python")  # `language` defaults to "python"; other targets are TODO

# 5. Results are written to the `output` directory. Objects are safe to let go out of scope.
```
