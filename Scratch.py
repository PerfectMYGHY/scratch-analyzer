from errors import UnsupportedError
from iostream import ColoredTqdm, ForeLightYellow
from public import supported_languages, head_block_opcodes, entries_block_opcodes
from translator import load_translator
import json
from typing import Dict, List
import re
from Cast import toCode
import shutil
from pathlib import Path


root_path = Path(__file__).parent


def replaceName(name: str):
    result = ""
    allowed_chars = "abcdefghijklmnopqrstuvwxyz_1234567890"
    for idx, char in enumerate(name):
        if idx == 0 and char in "1234567890":
            result += "n"
        if char.lower() not in allowed_chars:
            result += "_"
        else:
            result += char
    return result

class Scratch2OtherFile(object):
    def __init__(self, language, name, target, isStage=False):
        self.language = language
        self.variables = [] # 本文件的变量
        self.funcs = [] # 本文件的函数（Scratch帽子积木）
        self.entries = [] # 本文件的入口函数（Scratch当绿旗被点击）
        self.isStage = isStage
        self.name = name
        self.counts = {}
        self.translator = load_translator(language)
        self.target = target
        self.blockToFuncName = {}
        self.assets = {
            "sounds": {

            },
            "costumes": {

            }
        }
        self.procedures_prototypes = {}
        self.getAssets()

    def getAssets(self):
        for costume in self.target.costumes:
            self.assets["costumes"][costume["name"]] = {
                "path": costume["assetId"]+"."+costume["dataFormat"],
                "rotationCenterX": costume["rotationCenterX"],
                "rotationCenterY": costume["rotationCenterY"]
            }
        for sound in self.target.sounds:
            self.assets["sounds"][sound["name"]] = sound["md5ext"]

    def getSpecialName(self, head):
        if head.opcode == "procedures_definition":
            custom_block = self.target.blocks[head.inputs["custom_block"].data[1]]
            return "_"+custom_block.data["mutation"]["proccode"].replace(" ", "_").replace("%", "_"), custom_block.data["mutation"]
        return "", {}

    def toCodeFrom(self, head):
        func_name = f"opcode_{head.opcode}_"
        if func_name not in self.counts:
            self.counts[func_name] = 1
        else:
            self.counts[func_name] += 1
        func_name += str(self.counts[func_name])
        special, option = self.getSpecialName(head)
        func_name += special
        func_name = replaceName(func_name)
        self.blockToFuncName[head] = func_name
        code = f"async def {func_name}(instance, task_id):\n"
        # 添加记录
        if head.opcode == "procedures_definition":
            self.procedures_prototypes[func_name] = {
                "arg_ids": json.loads(option["argumentids"]),
                "arg_names": json.loads(option["argumentnames"]),
                "arg_defaults": json.loads(option["argumentdefaults"]),
                "warp": json.loads(f'[{option["warp"]}]')[0] if isinstance(option["warp"], str) else option["warp"],
                "proccode": option["proccode"]
            }
        indent = 1
        if not head.next:
            code += "    ...\n"
            return code
        block = head
        while block.next:
            block = block.next
            cd, indent = block.toCode(self.translator, indent, func_name, self.procedures_prototypes)
            code += ("    " * indent) + cd + block.getComment(indent) + "\n"
        return code

    def getProceduresPrototypes(self):
        code = "{"
        code += ", ".join([f'{name}: {option}' for name, option in self.procedures_prototypes.items()])
        code += "}"
        return code

    def getVariablesDict(self):
        code = "{"
        code += ", ".join([f'"{variable["type"]}_{variable["real_name"]}": {variable["name"]}' for variable in self.variables])
        code += "}"
        return code

    def getFuncList(self):
        code = "["
        code += ", ".join([self.blockToFuncName[head] for head in self.funcs])
        code += "]"
        return code

    def getEntryList(self):
        code = "["
        code += ", ".join([self.blockToFuncName[entry] for entry in self.entries])
        code += "]"
        return code

    def getClickFuncs(self):
        code = "["
        click_funcs = [func for func in self.funcs if func.opcode == "event_whenthisspriteclicked"]
        code += ", ".join([self.blockToFuncName[entry] for entry in click_funcs])
        code += "]"
        return code

    def getKeyFuncMap(self):
        code = "{"
        keyFuncs = [item for item in self.funcs if item.opcode == "event_whenkeypressed"]  # 获取所有“当按下”入口
        key_to_func: dict[str, list[str]] = {}
        for func in keyFuncs:
            name: str = func.fields["KEY_OPTION"].data[0]
            if name not in key_to_func:
                key_to_func[name] = [self.blockToFuncName[func]]
            else:
                key_to_func[name].append(self.blockToFuncName[func])
        code += ", ".join([f'"{name}": [{", ".join(bs)}]' for name, bs in key_to_func.items()])
        code += "}"
        return code
    
    def getBroadcastParams(self):
        code = "{"
        broadcasts = [item for item in self.funcs if item.opcode == "event_whenbroadcastreceived"] # 获取所有“当接收到”入口
        name_to_head: dict[str, list[str]] = {}
        for broadcast in broadcasts:
            name: str = broadcast.fields["BROADCAST_OPTION"].data[0]
            if name not in name_to_head:
                name_to_head[name] = [self.blockToFuncName[broadcast]]
            else:
                name_to_head[name].append(self.blockToFuncName[broadcast])
        code += ", ".join([f'"{name.lower()}": [{", ".join(bs)}]' for name, bs in name_to_head.items()])
        code += "}"
        return code

    def getBCFM(self):
        code = "{"
        changers = [item for item in self.funcs if item.opcode == "event_whenbackdropswitchesto"]  # 获取所有“当背景换为”入口
        name_to_changers: dict[str, list[str]] = {}
        for changer in changers:
            name: str = changer.fields["BACKDROP"].data[0]
            if name not in name_to_changers:
                name_to_changers[name] = [self.blockToFuncName[changer]]
            else:
                name_to_changers[name].append(self.blockToFuncName[changer])
        code += ", ".join([f'"{name}": [{", ".join(bs)}]' for name, bs in name_to_changers.items()])
        code += "}"
        return code

    def getCheckerMap(self):
        code = "{"
        checkers = [item for item in self.funcs if item.opcode == "event_whengreaterthan"]  # 获取所有“当背景换为”入口
        name_to_checkers: dict[str, dict[str, str]] = {}
        for checker in checkers:
            menu: str = checker.fields["WHENGREATERTHANMENU"].data[0]
            computer: str = checker.inputs["VALUE"].toCode(self.translator, "", {})
            name = self.blockToFuncName[checker]
            if name not in name_to_checkers:
                name_to_checkers[name] = {
                    "menu": menu,
                    "computer": computer
                }
            else:
                raise ValueError("重复注册！")
        code += ", ".join(['{name}: |-"menu": "{menu}", "computer": lambda instance: {computer}-|'.format(name=name, menu=bs["menu"],
                                                                                                computer=bs["computer"])
                           .replace("|-", "{").replace("-|", "}")
                           for name, bs in name_to_checkers.items()])
        code += "}"
        return code

    def getSACFuncs(self):
        code = "["
        SAC_funcs = [func for func in self.funcs if func.opcode == "control_start_as_clone"]
        code += ", ".join([self.blockToFuncName[entry] for entry in SAC_funcs])
        code += "]"
        return code

    def getArgMap(self, args):
        code = "{"
        code += ", ".join([f'"{name}": ({code})' for name, code in args.items()])
        code += "}"
        return code

    def generate(self, output, stage = None):
        data = f'''"""
Scratch2Python库生成
注意：由于是机器翻译代码，本文件会有多处地方出现冗余的括号、多余的代码等。请不要以此文件来学习Python。
"""
import Scratch4Python as Scratch # 专用Scratch功能封装库
{"import target_Stage as Stage # 引入舞台以使用公共变量" if not self.isStage else ""}

# 变量

'''

        # 生成变量
        for variable in ColoredTqdm(self.variables, desc="正在生成变量代码"):
            if variable["type"] == "v":
                if isinstance(variable["default"], int):
                    data += f"{variable['name']} = {variable['default']} # Scratch变量——原名:{variable['real_name']}\n"
                else:
                    data += f"{variable['name']} = '{variable['default']}' # Scratch变量——原名:{variable['real_name']}\n"
            else:
                data += f"{variable['name']} = {variable['default']} # Scratch列表——原名:{variable['real_name']}\n"

        data += "\n# 函数\n\n"
        # 生成函数代码
        for func in ColoredTqdm(self.funcs, desc="正在生成函数"):
            data += self.toCodeFrom(func) + "\n"

        # 添加主程序
        with open(root_path / "codeMain.tpl", "r", encoding="utf-8") as file:
            codeMain = file.read().replace("""import Scratch4Python as Scratch
""", "")
        data += codeMain.format(name=self.name, variables=self.getVariablesDict(), x=self.target.x, y=self.target.y,
                                direction=self.target.direction, visible=self.target.visible, size=self.target.size,
                                currentCostume=self.target.currentCostume, funcs=self.getFuncList(), entries=self.getEntryList(),
                                assets=json.dumps(self.assets, ensure_ascii=False, indent=4), broadcast_params=self.getBroadcastParams(),
                                layer_order=self.target.layerOrder, volume=self.target.volume, click_funcs=self.getClickFuncs(),
                                key_map=self.getKeyFuncMap(), backdrop_change_func_map=self.getBCFM(), checker_map=self.getCheckerMap(),
                                start_as_clone_funcs=self.getSACFuncs(), procedures_prototypes=self.getProceduresPrototypes())

        # 代码函数引用替换
        global_tasks = []
        first_prcesses = []
        # 使用更精确的匹配模式，确保不跨标记匹配
        pattern_for_code = r'!!!\[(SPECIAL_CODE_TO_GLOBAL)\]\[(.*?)\]!!!'
        pattern = r'!!!\[([^\[\]]+?)\]\[(.*?)\]!!!'

        # 先处理变量请求
        for match in ColoredTqdm(re.finditer(pattern_for_code, data, re.DOTALL), desc="正在查找全局替换变量请求"):
            name = match.group(1).strip()
            value = match.group(2)
            if name == "SPECIAL_CODE_TO_GLOBAL":
                first_prcesses.append((name, value))

        for key, value in first_prcesses:
            hasVariable = False
            code = None
            for vid, variable in self.target.variables.items():
                if variable[0] == value:
                    code = f'Scratch.getVariable(instance, "{value}")'
                    hasVariable = True
                    break
            if not hasVariable:
                if stage:
                    for vid, variable in stage.variables.items():
                        if variable[0] == value:
                            code = f'Scratch.getVariable(instance, "{value}")'
                            hasVariable = True
                            break
                if not hasVariable:
                    code = toCode(value)
            if code is None:
                raise ValueError(f"无法处理的特殊全局替换请求！value=`{value}`")
            data = data.replace(f'!!![{key}][{value}]!!!', code)  # 替换

        # 其次检查其他请求
        for match in ColoredTqdm(re.finditer(pattern, data, re.DOTALL), desc="正在查找全局替换普通请求"):
            name = match.group(1).strip()
            value = match.group(2).strip()
            if name == "SPECIAL_CODE_TO_GLOBAL":
                continue
            global_tasks.append((name, value))

        last_func_name = None
        for key, value in ColoredTqdm(global_tasks, "正在进行全局替换"):
            match key:
                case "FUNC_NAME_TO_GLOBAL":
                    found = False
                    for name, option in self.procedures_prototypes.items():
                        if option["proccode"] == value:
                            data = data.replace(f'!!![{key}][{value}]!!!', name) # 替换为函数名
                            found = True
                            last_func_name = name
                            break
                    if not found:
                        raise ValueError("未找到proccode对应的自定义函数！")
                case "ARGS_TO_GLOBAL":
                    pattern = r'Scratch\.getVariable\(instance,\s*"([^"]*)"\)'
                    replacement = r'Scratch.getVariable(instance, \\"\1\\")'
                    value2 = re.sub(pattern, replacement, value)
                    value2 = re.sub(r'""(.+?)""', r'"\\"\1\\""', value2)
                    try:
                        _args = json.loads(value2)
                    except json.JSONDecodeError:
                        pattern = r'\((?!\\")(")([^"\\]*(?:\\.[^"\\]*)*)(")(?<!\\)\)'
                        # value2 = value2.replace('("', '(\\"').replace('")', '\\")')
                        value2 = re.sub(pattern, r'(\\"\2\\")', value2)
                        value2 = value2.replace('("', '(\\"').replace('", error=False)', '\\", error=False)')
                        try:
                            _args = json.loads(value2)
                        except json.JSONDecodeError:
                            raise ValueError(f"错误的值数据：{value}\n修复后：{value2}")
                    if not last_func_name:
                        raise ValueError("意外出现的参数全局替换请求，通常是先请求替换函数名！")
                    option = self.procedures_prototypes[last_func_name]
                    args = {}
                    for arg_id, code in _args.items():
                        arg_idx = option["arg_ids"].index(arg_id)
                        arg_name = option["arg_names"][arg_idx]
                        args[arg_name] = code
                    data = data.replace(f'!!![{key}][{value}]!!!', self.getArgMap(args))  # 替换为参数列表
                case _:
                    raise ValueError(f"意外的全局替换请求！key=`{key}`,value=`{value}`")

        # 写入文件
        path = output / f"target_{self.name}.py"
        with open(path, "w", encoding="utf-8") as file:
            file.write(data)

class Scratch(object):
    def __init__(self, project):
        self.project = project
        self.public_id_to_variable_name = {}

    def generate(self, output, language="python"):
        language = language.lower()
        if language not in supported_languages:
            raise UnsupportedError(f"暂不支持转换为{language}语言")
        print(ForeLightYellow("开始将Scratch项目转换为", language, "语言！"))
        # 首先处理舞台
        stage = self.project.targets["Stage"]
        if not stage.isStage:
            raise ValueError("Stage角色不是舞台！舞台角色检测失败！")
        stage_file = Scratch2OtherFile(language, stage.name, stage, True)
        # 收集公共变量
        for vid, variable in ColoredTqdm(stage.variables.items(), desc="正在收集公共变量"):
            name = replaceName(f"public_variable_{variable[0]}")
            stage_file.variables.append({
                "name": name,
                "default": variable[1],
                "real_name": variable[0],
                "type": "v"
            })
            self.public_id_to_variable_name[vid] = name
        # 收集公共列表
        for vid, li in ColoredTqdm(stage.lists.items(), desc="正在收集公共列表"):
            name = replaceName(f"public_list_{li[0]}")
            stage_file.variables.append({
                "name": name,
                "default": li[1],
                "real_name": li[0],
                "type": "l"
            })
            self.public_id_to_variable_name[vid] = name
        # 收集函数入口点
        for bid, block in ColoredTqdm(stage.blocks.items(), desc="正在收集函数入口点"):
            if block.opcode in head_block_opcodes:
                stage_file.funcs.append(block)
            if block.opcode in entries_block_opcodes:
                stage_file.entries.append(block)
        # 开始生成舞台文件
        stage_file.generate(output)

        # 生成剩余标准角色
        for name, target in ColoredTqdm(self.project.targets.items(), desc="正在处理角色"):
            if name == "Stage":
                continue

            target_file = Scratch2OtherFile(language, replaceName(target.name), target, False)
            # 收集公共变量
            for vid, variable in ColoredTqdm(target.variables.items(), desc="正在收集变量"):
                name = replaceName(f"{target.name}_variable_{variable[0]}")
                target_file.variables.append({
                    "name": name,
                    "default": variable[1],
                    "real_name": variable[0],
                    "type": "v"
                })
            # 收集公共列表
            for vid, li in ColoredTqdm(target.lists.items(), desc="正在收集列表"):
                name = replaceName(f"{target.name}_list_{li[0]}")
                target_file.variables.append({
                    "name": name,
                    "default": li[1],
                    "real_name": li[0],
                    "type": "l"
                })
            # 收集函数入口点
            for bid, block in ColoredTqdm(target.blocks.items(), desc="正在收集函数入口点"):
                if block.opcode in head_block_opcodes:
                    target_file.funcs.append(block)
                if block.opcode in entries_block_opcodes:
                    target_file.entries.append(block)
            # 开始生成舞台文件
            target_file.generate(output, stage=stage)
        # 复制标准库
        shutil.copytree(root_path / "Scratch4Python", output / "Scratch4Python")
        with open("audio_ui.html", "r", encoding="utf-8") as ifile, open(output / "audio_ui.html", "w", encoding="utf-8") as ofile:
            ofile.write(ifile.read())
        # 生成数据
        imports_code = ""
        inits = "["
        for name, target in self.project.targets.items():
            name = replaceName(name)
            name = "target_{name}".format(name=name)
            imports_code += "from {name} import init as {name}_init\n".format(name=name)
            inits += "{name}_init, ".format(name=name)
        inits += "]"
        # 生成并复制主程序
        with open(root_path / "progMain.tpl", "r", encoding="utf-8") as ifile, open(output / "main.py", "w", encoding="utf-8") as ofile:
            ofile.write(ifile.read().format(imports=imports_code, inits=inits))