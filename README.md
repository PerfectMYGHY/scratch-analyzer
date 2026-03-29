# scratch-analyzer

English version README.md: [README.english.md](README.english.md)

Scratch 解析库。一个使用Python制作的能够分析Python代码的软件包。

## 历史

基础代码再2025年（发布仓库的1年前）编写，当时我有一个梦想，将Scratch翻译成一个Python上能够运行的程序，于是我写下了这个程序，原名`Scratch2Python`。

我~~凭借着我惊人的智慧~~写出了`Scratch2Python`的Scratch转换Python代码功能，虽然代码有一丢烂，但是转换相当成功。

然而，接下来的问题是，Scratch运行时阻挠了我。从代码历史你能看到，本项目最终使用`Scratch4Python`作为运行时库，但是很可惜，我跟他耗了几个月，最终失败。

## 那么此库为何而在

因为我的这个翻译器还是太好了，理论上还可以做到翻译成各种语言，虽然目前仅保证转换为Python是正常的。

我认为这个功能很不错，于是建立存储库并单独提取其代码转换功能。

## 那Scratch4Python呢

我不打算完全放弃他，但是请等我深造几年，吃透OpenGL后，再管它吧。我想到时候将他作为独立库发布，同时更名`python-scratch-vm`。到时候可以两个库结合使用。
