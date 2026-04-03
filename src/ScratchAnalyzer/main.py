import zipfile
import os
import sys
import argparse
import json
import shutil
import traceback
from pathlib import Path

from .iostream import ForeLightRed, ForeLightGreen, StartLightRed, Reset, ColoredTqdm
from .Project import Project
from .Scratch import Scratch
from .public import supported_languages


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", "-i", type=str, required=True, help="输入文件（必须是Scratch3.0文件）")
    parser.add_argument("--output", "-o", type=str, required=True, help="输出目录")
    parser.add_argument("--language", "-l", default="python-pcode", choices=supported_languages, type=str, required=False, help="转换成的语言")
    args = parser.parse_args()

    if os.path.isfile(args.output):
        print(ForeLightRed("输出路径指向了文件！"))
        return -1

    if not os.path.exists(args.input) or not os.path.isfile(args.input):
        print(ForeLightRed("输入文件不存在或不是文件！"))
        return -1

    if not args.input.endswith(".sb3"):
        if args.input.endswith(".sb2") or args.input.endswith(".sb1"):
            print(ForeLightRed("仅支持 Scratch 3.0 项目文件！"))
            return -1
        print(ForeLightRed("输入文件不是 Scratch 项目文件！"))
        return -1

    print(ForeLightGreen("正在初始化输出目录..."))
    if os.path.exists(args.output) and os.path.isdir(args.output):
        shutil.rmtree(args.output)
    os.makedirs(args.output)

    # 步骤1：解压数据
    out = os.path.join(args.output, "assets") # 全部解压至输出目录
    with zipfile.ZipFile(args.input, "r") as zip_ref:
        try:
            for member in ColoredTqdm(zip_ref.infolist(), desc="正在解压中", unit="文件"):
                zip_ref.extract(member, out)
        except:
            StartLightRed()
            print("解压时出错：")
            traceback.print_exc()
            Reset()
            return -1

    # 步骤2：解析project.json
    print(f"正在解析项目数据...")
    project_json = os.path.join(out, "project.json")
    with open(project_json, "r", encoding="utf-8") as f:
        data = json.load(f)

    # 步骤3：解析数据
    project = Project(data)

    # 步骤4：生成数据
    scratch = Scratch(project)
    scratch.generate(Path(args.output), language=args.language)

    return 0

if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception as e:
        StartLightRed()
        print("主程序遇到未捕获错误：")
        traceback.print_exc()
        Reset()
        sys.exit(-1)
