"""
本代码有Scratch2Python生成
"""
# 引入各个角色
{imports}
# 引入核心库
import Scratch4Python as Scratch
# 参数解析
import argparse

# 主程序
def main():
    # 初始化参数
    parser = argparse.ArgumentParser()
    parser.add_argument("--username", "-u", type=str, required=False, default="Scratch VM PE 用户", help="运行时使用的用户名")
    parser.add_argument("--fps", "-f", type=int, required=False, default=30, help="运行帧率")
    args = parser.parse_args()
    # 初始化虚拟机
    vm = Scratch.ScratchVM(args.username)
    Scratch.setVM(vm)
    # 初始化各个角色
    inits = {inits}
    for init in inits:
        init()
    # 启动！
    exit(Scratch.main())

if __name__ == "__main__":
    main()