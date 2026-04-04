import re

from .translator import WrappedTranslator
from .iostream import ColoredTqdm
from .Cast import toCode
from .public import substack_opcodes, substack_opcodes_need_flush
import json
import warnings
from typing import cast


class Input(object):
    def __init__(self, _input: list, target, name: str):
        self.data = _input
        self.target = target
        self.name = name

    def toCode(self, translator: WrappedTranslator, func_name: str, procedures_prototypes):
        if isinstance(self.data[1], str):
            try:
                fieldBlock = self.target.blocks[self.data[1]]
                field = fieldBlock.fields[self.name]
                code = field.toCode(translator)
            except KeyError:
                try:
                    blockId = self.data[1]
                    code, _ = self.target.blocks[blockId].toCode(translator, 1, func_name, procedures_prototypes)
                except KeyError:
                    code = translator.data_variable_getter.format(value=self.data[1]) # 这种情况是为了兼容Scratch 2.0转换后的遗留问题
        elif self.data[1]:
            value = self.data[1][1]
            code = f"!!![SPECIAL_CODE_TO_GLOBAL][{value}]!!!"
        else:
            code = '""' # 任何我认识的语言应该都是""表示空字符串吧
        return code

class Field(object):
    def __init__(self, field: list, target):
        self.data = field
        self.target = target

    def toCode(self, translator: WrappedTranslator):
        return toCode(self.data[0])

class Block(object):
    def __init__(self, block, target):
        # 获取数据
        try:
            self.opcode = block["opcode"]
        except TypeError:
            raise TypeError(f"非法block，没有opcode！: {block}\n\n{target._blocks}")
        self._next = block["next"]
        self.next = None
        self._parent = block.get("parent")
        self.parent = None
        self._inputs = block["inputs"]
        self.inputs = {}
        self._fields = block["fields"]
        self.fields = {}
        self.shadow = block["shadow"]
        self.topLevel = block["topLevel"]
        self.target = target
        self.computed = False
        self.comment = block.get("comment")
        self.data = block

    def getComment(self, indent: int, translator: WrappedTranslator, uniqueEnv: bool = False) -> str:
        """
        获取本积木块的注释

        :param indent: 注释若换行采用的缩进数
        :param translator: 翻译器，用于获取注释标志
        :param uniqueEnv: 是否在特殊环境，默认False，若为False，则在当前积木为带子块积木时返回无注释，否则获取注释
        :return: 注释代码
        """
        if self.comment and (not uniqueEnv and self.opcode not in substack_opcodes):
            text = self.target.comments[self.comment]["text"]
            return f" {translator.one_line_comment} {text}".replace("\n", "    " * indent + f"{translator.one_line_comment} ") # 保证多行注释正常
        return ""
    
    def compute_relation(self):
        # 计算关联
        self.target = self.target
        self.next = self.target.blocks[self._next] if self._next else None
        self.parent = self.target.blocks[self._parent] if self._parent else None
        self.inputs = {k: Input(v, self.target, k) for k, v in self._inputs.items()}
        self.fields = {k: Field(v, self.target) for k, v in self._fields.items()}
        self.computed = True

    def generateArgs(self, arg_ids: list[str], args: dict[str, Input], translator: WrappedTranslator, func_name: str, procedures_prototypes: dict[str, dict]) -> str:
        result = {}
        for arg_id in arg_ids:
            if arg_id not in args: # 没有传入参数则跳过，内部会使用默认值
                continue
            value = args[arg_id].toCode(translator, func_name, procedures_prototypes)
            result[arg_id] = value
        ret = "{"
        ret += ", ".join([f'"{key}": {value}' for key, value in result.items()])
        ret += "}"
        return ret

    def toCode(self, translator: WrappedTranslator, indent: int, func_name: str, procedures_prototypes: dict[str, dict]) -> tuple[str, int]:
        if self.opcode not in substack_opcodes: # shadow指的是是否有SUBSTACK（子积木，就比如“如果”里包着的积木）
            try:
                code = getattr(translator, self.opcode)
            except AttributeError:
                warnings.warn("不支持的积木操作代码： %s，若警告不会停止则默认继续转换（无法翻译的代码将以注释替代！）" % self.opcode)
                code = translator.error_throw.format(content=f'"未成功翻译的代码，操作代码：{self.opcode}，请手动翻译！"', comment=f"!!!不支持的积木操作代码： {self.opcode}，请手动翻译!!!")
            # 添加注释: 外部调用toCode后自动添加注释
            # 自定义函数执行的特殊处理
            if self.opcode == "procedures_call":
                code = (code.replace("%[FUNC_NAME]%", "!!![FUNC_NAME_TO_GLOBAL][{proccode}]!!!".format(proccode=self.data["mutation"]["proccode"]))
                        .replace("%[ARGS]%", "!!![ARGS_TO_GLOBAL][{args}]!!!").format(args=self.generateArgs(
                    json.loads(self.data["mutation"]["argumentids"]),
                    self.inputs,
                    translator, func_name, procedures_prototypes
                )))
            for name, inp in self.inputs.items():
                code = code.replace(f'%[{name}]%', inp.toCode(translator, func_name, procedures_prototypes))
            for name, field in self.fields.items():
                code = code.replace(f'%[{name}]%', field.toCode(translator))
            pattern = r'%\[.*?\]%'  # 非贪婪匹配
            code = re.sub(pattern, 'None', code)
            if self.opcode == "control_stop" and self.fields["STOP_OPTION"].data[0] != "other scripts in sprite":
                code += "\n" + "    " * indent + translator.exit_function
            if self.opcode == "control_delete_this_clone":
                code += "\n" + "    " * indent + translator.is_current_clone
                code += "\n" + "    " * (indent + 1) + translator.exit_function
        else:
            try:
                code = getattr(translator, self.opcode)  # 获取主体代码
            except AttributeError:
                warnings.warn("不支持的积木操作代码： %s，若警告不会停止则默认继续转换（无法翻译的代码将以注释替代！）" % self.opcode)
                code = translator.error_throw.format(content=f'"未成功翻译的代码，操作代码：{self.opcode}，请手动翻译！"', comment=f"!!!不支持的积木操作代码： {self.opcode}，请手动翻译!!!")
            # 添加注释: 特殊代码需要特殊处理，原因请见Scratch.py或下方
            code += self.getComment(indent + 1, translator, uniqueEnv=True)
            # 将参数格式化进去
            for name, inp in self.inputs.items():
                if name in ("SUBSTACK", "SUBSTACK2"):
                    continue
                code = code.replace(f'%[{name}]%', inp.toCode(translator, func_name, procedures_prototypes))
            for name, field in self.fields.items():
                code = code.replace(f'%[{name}]%', field.toCode(translator))
            pattern = r'%\[.*?\]%'  # 非贪婪匹配
            code = re.sub(pattern, 'None', code)
            indent += 1
            code += "\n"
            if self.inputs["SUBSTACK"].data[1]:
                head = cast(Block, self.target.blocks[self.inputs["SUBSTACK"].data[1]])
                block = head
                while True:
                    cd, indent = block.toCode(translator, indent, func_name, procedures_prototypes)
                    code += ("    " * indent) + cd + block.getComment(indent, translator) + "\n" # 此处注释获取为普通调用，因此对于有自己木块，这里不加注释，在内部添加
                    block = cast(Block | None, block.next)
                    if not block:
                        break
                if substack_opcodes_need_flush[self.opcode]:
                    if func_name in procedures_prototypes and procedures_prototypes[func_name]["warp"]: # 如果时自定义积木且使用了warp
                        suffix = ""
                    else:
                        suffix = translator.frame_wait
                else:
                    suffix = ""
                code += ("    " * indent) + suffix + "\n"
            else:
                code += ("    " * indent) + f"{translator.blank_substack}\n"
            if "SUBSTACK2" in self.inputs:
                code += "{indent}{before}\n".format(indent="    " * (indent-1),before=getattr(translator, self.opcode+"_before_2"))
                if self.inputs["SUBSTACK2"].data[1]:
                    head = cast(Block, self.target.blocks[self.inputs["SUBSTACK2"].data[1]])
                    block = head
                    while True:
                        cd, indent = block.toCode(translator, indent, func_name, procedures_prototypes)
                        code += ("    " * indent) + cd + block.getComment(indent, translator) + "\n" # 此处注释获取为普通调用，因此对于有自己木块，这里不加注释，在内部添加
                        block = cast(Block | None, block.next)
                        if not block:
                            break
                    if substack_opcodes_need_flush[self.opcode]:
                        if func_name in procedures_prototypes and procedures_prototypes[func_name]["warp"]: # 如果时自定义积木且使用了warp
                            suffix = ""
                        else:
                            suffix = translator.frame_wait
                    else:
                        suffix = ""
                    code += ("    " * indent) + suffix + "\n"
                else:
                    code += ("    " * indent) + f"{translator.blank_substack}\n"
            indent -= 1
        return code, indent

class Target(object):
    def __init__(self, target, print_progress: bool=True):
        progress_generator = ColoredTqdm if print_progress else lambda x, **kwargs: x
        # 获取数据
        self.isStage = target["isStage"]
        self.name = target["name"]
        self.variables = target["variables"]
        self.lists = target["lists"]
        self.broadcasts = target["broadcasts"]
        self._blocks = target["blocks"]
        self.comments = target["comments"]
        self.currentCostume = target["currentCostume"]
        self.costumes = target["costumes"]
        self.sounds = target["sounds"]
        self.volume = target["volume"]
        self.layerOrder = target["layerOrder"]
        self.visible = target.get("visible", True)
        self.x = target.get("x", 0)
        self.y = target.get("y", 0)
        self.size = target.get("size", 100)
        self.direction = target.get("direction", 90)
        self.draggable = target.get("draggable", False)
        self.rotationStyle = target.get("rotationStyle", "all around")
        self.tempo = target.get("tempo")
        # 解析剩余参数
        self.args = {k: v for k, v in target.items() if k not in {
            'isStage',
            'name',
            'variables',
            'lists',
            'broadcasts',
            'blocks',
            'comments',
            'currentCostume',
            'costumes',
            'sounds',
            'volume',
            'layerOrder',
            'visible',
            'x',
            'y',
            'size',
            'direction',
            'draggable',
            'rotationStyle',
            'tempo'
        }}
        if self._blocks:
            # 计算blocks
            self.blocks = {k: Block(v, self) for k, v in progress_generator(self._blocks.items(), desc="创建积木块中", unit="积木块") if isinstance(v, dict)}
            # 计算关联
            for block in progress_generator(self.blocks.values(), desc="计算块关联中", unit="积木块"):
                block.compute_relation()
        else:
            self.blocks = {}

class Monitor(object):
    def __init__(self, monitor):
        self.id = monitor["id"]
        self.mode = monitor["mode"]
        self.opcode = monitor["opcode"]
        self.params = monitor["params"]
        self.spriteName = monitor["spriteName"]
        self.value = monitor["value"]
        self.width = monitor["width"]
        self.height = monitor["height"]
        self.x = monitor["x"]
        self.y = monitor["y"]
        self.visible = monitor["visible"]
        self.sliderMin = monitor.get("sliderMin")
        self.sliderMax = monitor.get("sliderMax")
        self.isDiscrete = monitor.get("isDiscrete")

class Extension(object):
    def __init__(self, extension):
        if extension not in ("pen", ):
            warnings.warn("暂不支持扩展：%s，若警告不会停止则默认继续转换" % extension)

class Meta(object):
    def __init__(self, meta):
        self.semver = meta["semver"]
        self.agent = meta["agent"]
        self.vm = meta["vm"]

class Project(object):
    def __init__(self, project, print_progress=True):
        self.project = project
        self._parse(print_progress=print_progress)

    def _parse(self, print_progress=True):
        progress_generator = ColoredTqdm if print_progress else lambda x, **kwargs: x
        if self.project.get("extensionURLs"):
            warnings.warn("项目中包含自定义URL扩展，可能来自TurboWarp，当前版本不支持解析这些扩展，相关积木将无法转换！")
        self.meta = Meta(self.project["meta"])
        self.extensions = {}
        if self.project["extensions"]:
            for name in progress_generator(self.project["extensions"], desc="处理扩展中", unit="个"):
                self.extensions[name] = Extension(name)
        self.monitors = {}
        if self.project["monitors"]:
            for monitor in progress_generator(self.project["monitors"], desc="处理变量监视器中", unit="个"):
                self.monitors[monitor["id"]] = Monitor(monitor)
        self.targets = {}
        if self.project["targets"]:
            for target in progress_generator(self.project["targets"], desc="处理角色中", unit="个"):
                self.targets[target["name"]] = Target(target, print_progress=print_progress)

