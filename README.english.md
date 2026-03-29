# scratch-analyzer

中文版 README.md: [README.md](README.md)

A Scratch parsing library. This is a Python package for analyzing and processing code related to Scratch projects.

## History

The core code was written in 2025 (one year before this repository was published). At the time I had a dream: to translate Scratch projects into programs that can run on Python. I therefore wrote this project, originally named `Scratch2Python`.

I ~~(with what I like to call my astonishing brilliance)~~ implemented Scratch-to-Python translation in `Scratch2Python`. Although the code was a little rough around the edges, the translation worked quite well.

However, the next challenge was the Scratch runtime. As you can see from the project history, this repository eventually tried to use `Scratch4Python` as the runtime library, but after several months of effort I was unable to make it work.

## Why this project exists

Because the translator itself was still very useful: in theory it can be adapted to produce code for multiple target languages, although currently only translation to Python is fully supported.

I thought this functionality was worth preserving, so I created this repository and extracted the code translation functionality into a standalone package.

## What about Scratch4Python?

I don't plan to abandon it completely, but please give me a few years to study OpenGL more deeply. When I'm ready I'll release it as a separate library and rename it to `python-scratch-vm`. At that time the two projects can be used together.
