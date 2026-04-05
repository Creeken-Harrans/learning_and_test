# run.py
import sys
from cli_test.src.demo_cli_noted import main

if __name__ == "__main__":
    # sys.argv 形如:
    # ['run.py', 'train', '--fold', '0', '--device', 'cuda']
    #
    # sys.argv[0] 是脚本名 run.py
    # sys.argv[1:] 才是真正的命令行参数
    argv = sys.argv[1:]

    # 如果用户什么都没写，就默认显示帮助信息
    if not argv:
        argv = ["--help"]

    # 把参数交给真正的 CLI 入口
    exit_code = main(argv)
    raise SystemExit(exit_code)
